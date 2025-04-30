import os
from setuptools import setup, find_packages
from setuptools.command.install import install

def read_requirements(filename):
    with open(filename) as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]

with open("README.md", "r") as f:
    long_description = f.read()

class PostInstallCommand(install):
    """Custom post-install command to create ~/.vkube directory."""
    def run(self):
        install.run(self)
        vkube_home = os.path.expanduser("~/.vkube")
        config_file = os.path.join(vkube_home, "config.yaml")

        if not os.path.exists(vkube_home):
            os.makedirs(vkube_home)
            print(f"[INFO] Created directory: {vkube_home}")

        if not os.path.exists(config_file):
            with open(config_file, 'w') as file:
                file.write("# Default vkube configuration\n")
            print(f"[INFO] Created default config file: {config_file}")
setup(
    name = "vkube",
    description='VKube-CLI User-End',
    long_description=long_description,
    long_description_content_type="text/markdown",
    use_scm_version={
        "fallback_version": "0.0.1", # If no tag exists, use default version number
    },
    author='vcloud-team',
    author_email='v-cloud-team@v.systems',
    install_requires=read_requirements('requirements.txt'),
    setup_requires=["setuptools", "setuptools_scm"],
    license='Apache License 2.0',
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
    ],
    packages=find_packages(),
    python_requires='>=3.7',
    cmdclass={
        "install": PostInstallCommand,
    },
    entry_points={
        "console_scripts": [
            'vkube=vkube_cli.vkube:vkube',
        ],
    },
)
