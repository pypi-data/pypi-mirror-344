import click
import yaml
import requests
import os
import docker
import json
from requests.exceptions import SSLError
from docker.errors import DockerException

from typing import List, Dict, Any
from pathlib import Path

import vkube_cli.docker_config.credentials as credential
from vkube_cli.utils.decode import decode_token
from vkube_cli.utils.create_docker_client import create_client
from vkube_cli.utils.validate_vkubefile import ContainerValidator
from vkube_cli.utils.validate_vkubefile import VkubefileValidator
from vkube_cli.utils.validate_vkubefile import get_real_resource_unit
from vkube_cli.utils.file_io import read_file_to_string, read_yaml
from vkube_cli.utils.version import version_check
from vkube_cli.constants import VKUBE_CONFIG_PATH


def create_docker_client():
    try:
        # 尝试通过环境变量创建 Docker 客户端
        client = create_client()
        if client is not None:
            return client
    except ConnectionError as e:
        # 捕获连接相关异常并处理
        print(f"Error: Unable to connect to Docker. {e}")
        return None
    except RuntimeError as e:
        # 捕获其他运行时异常并处理
        print(f"Error: Unexpected runtime error. {e}")
        return None
client = create_docker_client()
if client is None:
    print("Error: Docker client initialization failed. Please make sure Docker is running and try again.")
    exit(1)
@click.command(help="Deploy a containerized application using VKubefile configuration.")
@click.option('-f','--file',default="./VKubefile.yaml",type=click.Path(exists=True),help='Path to the build configuration file. Default is VKubefile.yaml in the current directory.')
@version_check
def deploy(file):
    documents = read_yaml(file)
    if not documents:
        click.echo("VKubefile not exist in current directory")
        return
    vkubefile_validator = VkubefileValidator()
    result, all_errors = vkubefile_validator.validate_vkubefile(documents)
    if not result:
        for error in all_errors:
            print(f"{error}")
        return
    else:
        print("All configurations successfully verified")
    print("start------")
    deploy_cntr_params = []
    token = documents.get("token", "")
    if not token:
        click.echo("Error: token is empty")
        return
    imageRegistry = documents.get("imageRegistry", "docker")
    if imageRegistry not in ["docker", "ghcr"]:
        click.echo("Error: support Docker and GHCR registries only!")
        return
    containers_configs = documents.get("containers", [])
    if len(containers_configs) == 0:
        click.echo("Error: No containers to deploy.")
        return
    # Read the vkube cli configuration file
    config = read_yaml(VKUBE_CONFIG_PATH)
    if not config:
        click.echo("config is empty")
        return
    """Deploy using a VKubefile configuration."""
    registry_user_name = credential.check_and_login(imageRegistry)
    if not registry_user_name:
        click.echo("Login registry failed")
        return
    auth = {
        "username": registry_user_name,
    }
    if imageRegistry == "docker":
        auth["password"] = config.get("DockerhubToken", "")
    elif imageRegistry == "ghcr":
        auth["password"] = config.get("GHCRToken", "")
    if not auth["password"]:
        click.echo(f"Please configure the {imageRegistry} pulling image token first")
        return
    pvtLogin = []
    api_address,secret = decode_token(token)
    us_info = user_service_info(api_address + "/api/v1/k8s/userService",secret)
    if us_info == None or us_info.get("status") not in ["ServicePending", "ServiceRunning", "ServiceStopped"]:
        print("Error: get user service info failed or user service is not available")
        return
    service_options = us_info.get("serviceOptions",{})
    real_resource_unit_str = service_options.get("resourceUnit")
    real_resource_unit = 0
    if real_resource_unit_str:
        real_resource_unit = get_real_resource_unit(real_resource_unit_str)
    else:
        print("Error: resourceUnit not found in serviceOptions")
        return
    container_validator = ContainerValidator(containers_configs)
    configured_resource_unit = container_validator.get_total_containers_resource_unit()
    if configured_resource_unit > real_resource_unit:
        print("Error: total resource unit is excessive,real_buy:{real_resource_unit},used:{configured_resource_unit}")
        return
    if container_validator.get_containers_num() > real_resource_unit:
        print("Error: the number of configured container is greater than real resource unit")
        return
    deploy_request_url = api_address+"/api/v1/k8s/deployment"
    if us_info.get("status") != "ServicePending":
        deploy_request_url = api_address+"/api/v1/k8s/deployment/update"

    for doc in containers_configs:  # 遍历文档
        # by default, every container using private image should appen auth info in cntr deploy parameter
        pvtLogin.append(auth)
        if doc["tag"] == "":
            doc["tag"] = "latest"
        # for vkube deploy api parameter
        full_img_ref =get_full_img_ref(imageRegistry,registry_user_name,doc["imageName"],doc["tag"])
        if not full_img_ref:
            click.echo("Error: get  image name failed")
            return
        doc["deploy"]["imageName"] = full_img_ref
        deploy_cntr_params.append(doc["deploy"])
        # Validate Dockerfile path
        build_info = doc.get("build", None)
        if build_info is None:
            continue
        dockerfile_path = build_info.get("dockerfilePath")
        dockerfiled, build_context = check_file_is_dockerfile(dockerfile_path)
        if dockerfiled:
            build_args = get_build_args_dict(build_info)
            ok = build_docker_image(full_img_ref, build_args,dockerfile_path=dockerfile_path)
            if not ok:
                return
            # push image to image repository
            docker_push(full_img_ref)
        else:
            click.echo("Info: Dockerfile path is invalid. deploy continue")
    # not exist dockerfile can also deploy
    deploy_http_request(deploy_cntr_params, pvtLogin,secret,deploy_request_url)

def build_docker_image(full_img_ref, build_args, context_path=".", dockerfile_path="Dockerfile"):
    try:
        # Convert paths to absolute paths
        context_path = str(Path(context_path).absolute())
        dockerfile_path = str(Path(dockerfile_path).absolute())
        repository = full_img_ref
        build_logs: List[Dict[str, Any]] = []
        print(f"Start building image-->{repository}")
         # Stream build logs
        for line in client.api.build(
            path=context_path,
            dockerfile=dockerfile_path,
            tag=repository,
            rm=True,
            decode=True,
            buildargs=build_args,
            platform='linux/amd64'
        ):
            if 'stream' in line:
                print(line['stream'].strip())
                build_logs.append(line['stream'].strip())
            elif 'status' in line:
                print(line['status'].strip())
                build_logs.append(line['status'].strip())
            elif 'progress' in line:
                print(line['progress'].strip())
            elif 'error' in line:
                build_logs.append(line['error'].strip())
                raise docker.errors.BuildError(reason=line['error'], build_log=build_logs)
            elif 'errorDetail' in line:
                print(f"Error detail: {line['errorDetail']}")
            else:
                print(line)
        print(f"\nSuccessfully built image: {repository}")
        return True
    except DockerException as e:
        print(f"Error while building the image: {str(e)}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        return False
def docker_push(full_img_ref):
    
    success = True
    # jsondata = json.dumps(push_response)
    push_logs = []
    try:
        push_response = client.images.push(repository=full_img_ref,stream= True,decode=True)
        for log_line in push_response:
            if 'status' in log_line:
                print(f"Status: {log_line['status'].strip()}")
                push_logs.append(log_line['status'].strip())
            elif 'progress' in log_line:
                print(log_line['progress'].strip())
            elif 'errorDetail' in log_line:
                error_detail = log_line['errorDetail']
                print(f"Error Detail: {error_detail['message']}")
            else:
                print(f"Log Entry: {log_line}")
            if "error" in log_line:
                push_logs.append(log_line['error'].strip())
                success = False  # 如果出现错误，推送失败
                break  # 终止处理，错误已发生
         
    except Exception as e:
        success = False
        print(f"Error pushing image: {e}")
    if success:
        print(f"Image {full_img_ref} pushed successfully!")
    else:
        print(f"Pushing image encounting error: {push_logs}")
def deploy_http_request(doc, pvtLogin, secret, deploy_request_url):

    converted_containers = [convert_container_config(container) for container in doc]
    data = {
        "containers": converted_containers,
        "pvtLogin":pvtLogin,
    }
    if secret == "":
        print("parameter invalid")
        return
    headers = {
        "secret":secret,
    }
    print("start deploy------")
    try: 
        resp = requests.post(deploy_request_url,data=json.dumps(data),headers=headers)
        if resp.status_code != 200:
            print(f"deploy failed,the concrete error is sending http request to {deploy_request_url} failed")
            print(f"Response Body: {resp.text}")
            return 
        else:
            print("deploy successfully")
    except SSLError as ssl_err:
        print(f"SSL Error: {ssl_err}")
        # 可以尝试显式设置 TLS 版本或更新 OpenSSL
        print("Please ensure your OpenSSL and Python versions are up-to-date.")
    except Exception as e:
        print(f"Unexpected Error: {e}")
        print("Please check your code or environment configuration.")

def check_file_is_dockerfile(file_path):
    # directory is none
    if not file_path:
        click.echo("Error: 'dockerfile' entry is missing in the configuration file.", err=True)
        return False, ""
    # file_path is not a file
    if not os.path.isfile(file_path):
        click.echo(f"{file_path} is not a file", err=True)
        return False, ""
    # file endwith Dockerfile
    if file_path.endswith("Dockerfile"):
        path_without_dockerfile = file_path[:-len("Dockerfile")]
        return True, path_without_dockerfile + "."

    else:
        return False,""
def convert_container_config(container):
    config = container.get("configurations",{})
    real_configuration = {}
    for file_path, mount_path in config.items():
        real_configuration[mount_path] = read_file_to_string(file_path)
    new_config = {
        "mountPath": container.get("persistStorage", ""),
        "name": container.get("containerName"),
        "imageName": container.get("imageName"), 
        "resourceUnit": container.get("resourceUnit"), 
        "ports": container.get("ports",[]),
        "envs": container.get("env",[]),
        "configMap": real_configuration,
        "command": container.get("command",[]),
        "args": container.get("args",[])
    }
    return new_config

def user_service_info(request_url,secret):
    headers = {
        "secret":secret,
    }
    try: 
        resp = requests.get(request_url,headers=headers)
        if resp.status_code != 200:
            print(f"Error: get user service info failed,the concrete error is sending http request to {request_url} failed")
            return None
        else:
            print("get user service info successfully")
            return resp.json()
    except SSLError as ssl_err:
        print(f"SSL Error: {ssl_err}")
        # 可以尝试显式设置 TLS 版本或更新 OpenSSL
        print("Please ensure your OpenSSL and Python versions are up-to-date.")
    except Exception as e:
        print(f"Unexpected Error: {e}")
        print("Please check your code or environment configuration.")


def get_build_args_dict(build_doc):
    build_args = {}
    if "buildArgs" in build_doc:
        for build_arg in build_doc["buildArgs"]:
            name = build_arg.get("name", None)
            value = build_arg.get("value", None)
            if name and value:
                build_args[name] = str(value)
    return build_args
def get_full_img_ref(registry_name, username, image_name, tage):
    if registry_name == "docker":
        return "docker.io/" + username + "/" + image_name + ":" + tage
    elif registry_name == "ghcr":
        return "ghcr.io/"  + username + "/" + image_name + ":" + tage
    else:
        click.echo("Error: support Docker and GHCR registries only!")
        return None
