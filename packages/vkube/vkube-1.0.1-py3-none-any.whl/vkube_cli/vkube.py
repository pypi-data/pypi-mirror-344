import click
from pathlib import Path
from vkube_cli.command.config import config
from vkube_cli.command.vkube_deploy import deploy
from vkube_cli.command.version import version
from vkube_cli.constants import VKUBE_CONFIG_PATH

def init_config():
    """Initialize vkube configuration."""
    try:
        config_path = Path(VKUBE_CONFIG_PATH)
        config_path.parent.mkdir(parents=True, exist_ok=True)
        if not config_path.exists():
            print(f"[INFO] Created default config file: {config_path}")
    except Exception as e:
        pass



@click.group()
def vkube():
    """vkube CLI: A Kubernetes-like CLI tool."""
init_config()
vkube.add_command(config)
vkube.add_command(deploy)
vkube.add_command(version)
if __name__ == "__main__":
    vkube()