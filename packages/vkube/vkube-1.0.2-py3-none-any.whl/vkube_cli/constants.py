import os

PACKAGE_NAME = "vkube"
VERSION_CHECK_INTERVAL = 24 * 3600  # 24 hours

VKUBE_CONFIG_PATH = os.path.expanduser("~/.vkube/config.yaml")
DOCKER_CONFIG_PATH = os.path.expanduser("~/.docker/config.json")

DOCKER_URL = "https://index.docker.io/v1/"
GHCR_URL = "https://ghcr.io"
