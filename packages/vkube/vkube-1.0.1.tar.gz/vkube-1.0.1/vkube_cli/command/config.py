import os
import click
import yaml

from vkube_cli.utils.version import version_check
from vkube_cli.utils.file_io import write_yaml, read_yaml
# 配置文件路径
VKUBE_HOME = os.path.expanduser("~/.vkube")
CONFIG_FILE = os.path.join(VKUBE_HOME, "config.yaml")

# 确保配置目录和文件存在
def ensure_vkube_home():
    """Ensure ~/.vkube directory and config file exist."""
    if not os.path.exists(VKUBE_HOME):
        os.makedirs(VKUBE_HOME)
        print(f"[INFO] Created directory: {VKUBE_HOME}")

    if not os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'w') as file:
            yaml.dump({}, file)  # 初始化为空的 YAML 文件
        print(f"[INFO] Created default config file: {CONFIG_FILE}")


@click.command(help="Manage vkube configuration.")
@click.option('-w','--write', metavar='KEY=VALUE', help="Write a key-value pair to the config file in the format 'GHCRToken=ghcr_XXXXXX'.")
@click.argument('key', type=str, required=False)
@version_check
def config(write, key):
    """
    Manage vkube configuration.

    Examples:
    - Read a key: vkube config GHCRToken
    - Write a key: vkube config -w GHCRToken=ghcr_XXXXXX
    """
    ensure_vkube_home()
    config = read_yaml(CONFIG_FILE)
    if write:
        # 验证格式为 'GHCRToken=ghcr_XXXXXX'
        if "=" not in write:
            click.echo("Error: Invalid format. Use KEY=VALUE.")
            return
        key, value = write.split("=", 1)
        # 提取 key 和 value
        if key and value:
            config[key] = value
            write_yaml(CONFIG_FILE, config)
            click.echo(f"[INFO] Updated '{key}' in config.yaml file.")
        else:
            click.echo("write failed")
    elif key:
        if not config:
            print("read_config function failed")
            return
        getValue = config.get(key)
        if getValue is not None:
            print(f"{getValue}")
        else:
            click.echo(f"{key} not found in {CONFIG_FILE}.")
    else:
        click.echo("Error: Please specify a key to read or use -w to write.")
        

