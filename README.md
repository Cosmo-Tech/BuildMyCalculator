# Build My Calculator

## Getting started
Clone the repository and navigate to the project directory:

```bash
git clone git@github.com:Cosmo-Tech/BuildMyCalculator.git
cd BuildMyCalculator
```

Installation Babylon CLI

```bash
python3 -m venv ~/.babylonenv
source ~/.babylonenv/bin/activate
pip install git+https://github.com/Cosmo-Tech/Babylon.git@5.1.0
echo 'alias babylonenv="source ~/.babylonenv/bin/activate"' >> ~/.bashrc
```

## Update and deploy solution

After adding a new RunTemplate or modifying an existing one, you need to rebuild the Docker image and apply the changes with Babylon.

```bash
babylon namespace use -c tenant-bmc -t tenant-bmc -s tenant-bmc
```

```bash
babylon apply --exclude webapp project/
```

Build the Docker image with a new tag (e.g., `0.1.0-dev`):

```bash
docker login aks-bmc.azure.platform.cosmotech.com -u tenant-bmc -p <harbor_password>
docker build -t aks-bmc.azure.platform.cosmotech.com/tenant-bmc/simulator:0.1.0-dev .
docker push aks-bmc.azure.platform.cosmotech.com/tenant-bmc/simulator:0.1.0-dev
```
