import click
from vkube_cli.command.config import config
from vkube_cli.command.vkube_deploy import deploy
from vkube_cli.command.version import version

@click.group()
def vkube():
    """vkube CLI: A Kubernetes-like CLI tool."""
vkube.add_command(config)
vkube.add_command(deploy)
vkube.add_command(version)
if __name__ == "__main__":
    vkube()