from vkube_cli.utils.create_docker_client import create_client
from vkube_cli.docker_config.credentials import is_docker_opened
def test_create_client():
    client = create_client()
    assert client is not None
    assert client.ping() is True
def test_is_docker_opened():
    if not is_docker_opened():
        print("not opened")
if __name__ == "__main__":
    test_create_client()