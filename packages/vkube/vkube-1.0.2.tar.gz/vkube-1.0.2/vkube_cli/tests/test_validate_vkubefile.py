import json
from vkube_cli.utils.validate_vkubefile import VkubefileValidator
from vkube_cli.utils.validate_vkubefile import ContainerValidator
from vkube_cli.utils.validate_vkubefile import get_real_resource_unit
from vkube_cli.command.vkube_deploy import read_vkube_file
config_file_path = "./local-vkubefile.yaml"
json_file_path = "./test-service.json"

json_data = read_vkube_file(json_file_path)
print("......")
print(json_data)
real_resource_unit_str = ""
if json_data:
    real_resource_unit_str = json_data["serviceOptions"]["resourceUnit"]
else:
    print("read json file failed")

config = read_vkube_file(config_file_path)
if config is None:
    print(f"read config failed or the {config_file_path} content is empty")
else:
    container_docs = config.get("containers",{})
    print("...... test start ......")
    vkubefile_validator = VkubefileValidator()
    container_validator = ContainerValidator(container_docs)
    configured_resource_unit = container_validator.get_total_containers_resource_unit()
    result,errors = vkubefile_validator.validate_vkubefile(config)
    real_resource_unit = get_real_resource_unit(real_resource_unit_str)
    if real_resource_unit < configured_resource_unit:
        print("the total resourceUnit of all containers can not over than you buy ")
    # result, message = validator.validate_containers(containers_config)
    if not result:
        for error in errors:
            print(f"{error}")
    else:
        print("all configuration successfully verified")
