import re
from typing import List, Dict, Tuple
CONTAINER_NAME_PATTERN = r'^[a-z0-9]([-a-z0-9]*[a-z0-9])?$'
LOCAL_FILE_PATH_PATTERN = r'^(?:\/|\.\.?(?:\/|$))([^/ ]+\/)*([^/ ]+)?\/?$'
MOUNT_FILE_PATH_PATTERN = r'^\/([^/ ]+\/)*([^/ ]+)?\/?$'
TAG_PATTERN= r'^[a-zA-Z0-9_][a-zA-Z0-9_.-]{0,127}$'
IMAGE_NAME_PATTERN = r'^[a-z0-9]+([._-][a-z0-9]+)*$'
supported_kinds = ["vkube"]
supported_image_registries = ["docker","ghcr"]
def validate_string_by_regexp(pattern:str,validate_str:str)-> bool:
    """
    validate string by regexp pattern
    """
    try:
        return bool(re.match(pattern, validate_str))
    except re.error:
        return False
   
def get_real_resource_unit(resource_unit_str:str)-> int:
    try:
        if resource_unit_str == "":
            return 0
        if "-" in resource_unit_str:
            number_str = resource_unit_str.split('-')[0]
            return int(number_str)
        else:
            return 0
    except ValueError:
        return 0
class VkubefileValidator:

    def __init__(self):
        self.supported_kinds = supported_kinds
        self.supported_image_registries = supported_image_registries
    def validate_base_fields(self,documents:Dict):
        errors = []
        kind = documents.get('Kind')
        if kind is None:
            errors.append("Kind field is required")
        if isinstance(kind,str):
            if kind.strip() == "":
                errors.append("Kind field can't be empty")
            if kind not in self.supported_kinds:
                errors.append(f"Kind must be one of {self.supported_kinds}")
        else:
            errors.append("Kind must be string type")
        token = documents.get("token")
        if token is None:
            errors.append("token field is required")
        if isinstance(token,str):
            if token.strip() == "":
                errors.append("token field can't be empty")
        else:
            errors.append("token must be string type")
        image_registry = documents.get("imageRegistry")
        if image_registry is None:
            errors.append("imageRegistry field is required")
        if isinstance(image_registry,str):
            if image_registry.strip() == "":
                errors.append("imageRegistry field can't be empty")
            if image_registry not in self.supported_image_registries:
                errors.append(f"imageRegistry must be one of {self.supported_kinds}")
        else:
            errors.append("imageRegistry must be string type")

        return len(errors) == 0,errors
    def validate_vkubefile(self, documents:Dict):
        all_errors = []
        # validate base fields
        print("------  start validate configurations ------")
        is_valid,base_errors = self.validate_base_fields(documents)
        if not is_valid:
            all_errors.extend(base_errors)
        
        container_docs = documents.get("containers") 
        if container_docs:
            container_validator = ContainerValidator(container_docs)
            containers_valid, container_errors = container_validator.validate_containers()
            if not containers_valid:
                all_errors.extend(container_errors)
        else:
            all_errors.append("containers configuration not exist")
        return len(all_errors) == 0,all_errors


class ContainerValidator:
    def __init__(self,container_docs:List[Dict]):
        # define required fields
        self.required_fields = ['tag','imageName']
        # define field types
        self.field_types = {
            'tag': str,
            'imageName':str,
            'deploy': dict,
            'build':dict
        }
        self.container_docs = container_docs
    def get_containers_num(self):
        return len(self.container_docs)
    def get_total_containers_resource_unit(self)-> int:
        resourceUnit = 0
        for container_doc in self.container_docs:
            if container_doc.get("deploy"):
                resourceUnit = resourceUnit + int(container_doc.get("deploy").get("resourceUnit",0))
        return resourceUnit
    def validate_containers(self) -> Tuple[bool,List[str]]:
        """validate containers list configuration"""  
        all_errors = []
        for index,container_doc in enumerate(self.container_docs):
            container_index = index + 1
            is_valid, error_msg = self.validate_single_container(container_index,container_doc)
            if not is_valid:
                all_errors.extend(error_msg)     
        return len(all_errors) == 0,all_errors
    def validate_single_container(self, index:int,container_doc: Dict) -> Tuple[bool, List[str]]:
        """validate single container configuration"""
        # check the required field
        all_errors = []
        for field in self.required_fields:
            if container_doc.get(field) is None:
                all_errors.append(f"field {field} in num.{index} container not exist")
        
        # validate the field type
        for field, expected_type in self.field_types.items():
            if field in container_doc and not isinstance(container_doc[field], expected_type):
               all_errors.append(f"field {field} in num.{index} container type error,should be {expected_type.__name__}")
        # validate imageName and tag,they can not be empty
        image_name = container_doc.get("imageName")
        if isinstance(image_name, str):
            if not validate_string_by_regexp(IMAGE_NAME_PATTERN,image_name):
                all_errors.append(f"imageName field in num.{index} container is invalid")
        else:
            all_errors.append(f"imageName field in num.{index} container is not a string type")
        tag = container_doc.get('tag') 
        if isinstance(tag, str):
            if tag == "":
                tag = "latest"
            if not validate_string_by_regexp(TAG_PATTERN,tag):
                all_errors.append(f"tag field in num.{index} container is invalid")
        else:
            all_errors.append(f"tag field in num.{index} container is not a string type")

        deploy_doc = container_doc.get("deploy")
        if deploy_doc is None:
            all_errors.append(f"deploy field in num.{index} container is required")
        if not isinstance(deploy_doc, dict):
            all_errors.append(f"deploy field in num.{index} container must be a dict")
        # validate resourceUnit
        resource_unit = deploy_doc.get('resourceUnit')
        if resource_unit is None:
            all_errors.append(f"resourceUnit field in num.{index} container is required")
        if not isinstance(resource_unit, int):
            all_errors.append(f"resourceUnit field in num.{index} container is not int type")
        if resource_unit < 1:
            all_errors.append(f"resourceUnit field in num.{index} container must greate than or equal to 1")
        # validate containerName
        container_name = deploy_doc.get('containerName')
        if container_name is None:
            all_errors.append(f"containerName field in num.{index} container is required")
        if isinstance(container_name, str):
            if container_name == "":
                all_errors.append(f"containerName field in num.{index} container is empty")
            if not validate_string_by_regexp(CONTAINER_NAME_PATTERN,container_name):
                all_errors.append(f"containerName field in num.{index} container is illegal")
        else:
             all_errors.append(f"containerName field in num.{index} container is not a string type")

        # validate port configuration
        if 'ports' in deploy_doc:
            is_valid, error_msgs = self.validate_ports(index,deploy_doc['ports'])
            if not is_valid:
                all_errors.extend(error_msgs)
        
        # validate envs
        if 'env' in deploy_doc:
            is_valid, error_msgs = self.validate_envs(index,deploy_doc['env'])
            if not is_valid:
                all_errors.extend(error_msgs)
        if "configurations" in deploy_doc:
            config_doc = deploy_doc.get("configurations")
            if config_doc and isinstance(config_doc, dict):
                for local_path,mount_path in config_doc.items():
                    local_path_is_valid = validate_string_by_regexp(LOCAL_FILE_PATH_PATTERN,local_path)
                    mountpath_is_valid = validate_string_by_regexp(MOUNT_FILE_PATH_PATTERN,mount_path)
                    if not local_path_is_valid or not mountpath_is_valid:
                        all_errors.append(f"localPath or mountPath in num.{index} container is illegal")
        build_doc = container_doc.get("build")
        if build_doc is None:
            all_errors.append(f"In num.{index} container, build field is required")
        if not isinstance(build_doc, dict):
            all_errors.append(f"In num.{index} container, build field must be a dict")
        res, error_msgs = self.validate_build(index,build_doc)
        if not res:
            all_errors.extend(error_msgs)
        return len(all_errors) == 0, all_errors
    
    def validate_ports(self, index:int,ports: List[Dict]) -> Tuple[bool, List[str]]:
        """validate ports"""
        all_errors = []
        if len(ports) != 1:
            all_errors.append(f"In num.{index} container,the number of containerPort or hostPort should more than one")

        for port in ports:
            if 'containerPort' not in port or 'hostPort' not in port:
                all_errors.append(f"In num.{index} container,missing containerPort or hostPort")
            
            if isinstance(port['containerPort'], int) and isinstance(port['hostPort'], int):
                if port['containerPort'] < 1 or port['containerPort'] > 65535 or \
                port['hostPort'] < 1 or port['hostPort'] > 65535:
                    all_errors.append(f"In num.{index} container,the range of containerPort and hostPort must be between 1 and 65535")
            else:
                all_errors.append(f"In num.{index} container,containerPort or hostPort is illegal")
        return len(all_errors) == 0, all_errors
    
    def validate_envs(self, index:int,envs: List[Dict]) -> Tuple[bool, List[str]]:
        """validate envs"""
        all_errors = []
        for env in envs:
            if 'name' not in env or 'value' not in env:
                all_errors.append(f"the envs in num.{index} container,missing required fields:name or value")
            
            if not isinstance(env['name'], str) or not isinstance(env['value'], str):
                all_errors.append(f"the envs in num.{index} container, the name or value is not a string")
                
            if not env['name']:
                all_errors.append(f"the name of envs in num.{index} container can not be empty")
        
        return len(all_errors) == 0,all_errors
    def validate_build(self,index:int,build_doc:Dict) -> Tuple[bool, List[str]]:
        all_errors = []
        docker_file_path = build_doc.get("dockerfilePath")
        if docker_file_path is None:
            all_errors.append(f"dockerfilePath field in num.{index} container must be set")
        if not isinstance(docker_file_path,str):
            all_errors.append(f"dockerfilePath field in num.{index} container must be string")
        return len(all_errors) == 0, all_errors
