# Vkube Command Tool For User

## Install

```shell
pip install vkube-cli-user
```

## Run CLI Locally

Install `virtualenv` to run the CLI tool locally:

```shell
pip3 install virtualenv
```

Create virtual environment:

```shell
virtualenv venv
```

Activate virtual environment:

```shell
source venv/bin/activate
```

Deactivate virtual environment:

```shell
deactivate
```

## Install CLI Globally from Source Code

Navigate to the repository root:

```shell
cd /path_to_project #directory containing setup.py
pip3 install -e . # may need to manually create ~/.vkube/config.yaml
```
or
```shell
pip3 install . # auto generates ~/.vkube/config.yaml
```

Install CLI with isolated dependencies:
```
pip3 install --user pipx
export PATH="$HOME/.local/bin:$PATH"
pipx install ~/path_to_project
pipx install --editable ~/path_to_project
```

## Using vkube-cli

After installing locally, from the root path ("xxx/vkube-cli"):

1. Add DockerhubToken or GHCRToken:

```shell
vkube config -w DockerhubToken=dckr_pat_xxxx
vkube config -w GHCRToken=ghcr_xxx
```

2. Configure VKubefile.yaml

3. Deploy using:

```shell
vkube deploy -f ./VKubefile.yaml #can deploy from any directory by specifying VKubefile.yaml path
```

## Export Dependencies

```bash
pip freeze > requirements.txt
```

## Notes

When configuring VKubefile.yaml, the build image context is "." (current directory where command is executed):

```shell
vkube deploy -f .VKubefile.yaml
```

For example, if running from vkube_cli directory, the build context is vkube_cli. Using COPY app.py /app in Dockerfile will fail if app.py doesn't exist in vkube_cli.

## Known Issues

### 1. Docker Not Running

If Docker isn't running, you'll see:

```sh
Error: Unable to connect to Docker. Error while fetching server API version: ('Connection aborted.', FileNotFoundError(2, 'No such file or directory'))
```

### 2. Image Push Failures

Network issues may prevent image pushing:

```sh
Pushing image encountering error: [{'status': 'The push refers to repository [docker.io/yourusername/myapp]'}, {'errorDetail': {'message': 'Get "https://registry-1.docker.io/v2/": net/http: TLS handshake timeout'}, 'error': 'Get "https://registry-1.docker.io/v2/": net/http: TLS handshake timeout'}]
```

## Release CLI to PyPI

### Build Package

Ensure setuptools, wheel and twine are installed:
```
pip install setuptools wheel twine
```

Build package from project root:
```
python setup.py sdist bdist_wheel
```
This creates a dist/ directory containing .tar.gz and .whl files for PyPI upload.

### Generate Version Number from Git Tags
Install:
```
pip install setuptools_scm
```

### 
Use specific tag to release 
```
git fetch --tags
git checkout v1.0.0  # switch to v1.0.0 tag
```
### Upload to PyPI

```
twine upload dist/* -u __token__ -p <your-pypi-api-token>
```

### Test Installation
After uploading to PyPI, test if the tool can be successfully installed via pip:

```
pip install vkube
vkube
```
