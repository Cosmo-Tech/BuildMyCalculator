# Babylon CLI v5 — Quick Reference Guide

## Installation

```bash
python3 -m venv ~/.babylonenv
source ~/.babylonenv/bin/activate
pip install git+https://github.com/Cosmo-Tech/Babylon.git@5.1.0
echo 'alias babylonenv="source ~/.babylonenv/bin/activate"' >> ~/.bashrc
```

Verify installation:

```bash
babylon --version
```

## Global Options

Every command supports these flags:

| Flag | Description |
|---|---|
| `-v, --verbosity` | Log level: `CRITICAL`, `ERROR`, `WARNING`, `INFO`, `DEBUG` |
| `-n, --dry-run` | Simulate without applying changes |
| `--log-path <dir>` | Directory for log files |
| `--version` | Print version |


## 1. Namespace Management

A **namespace** is a combination of context + tenant + state that tells Babylon which environment to target.

### Switch / create namespace

```bash
babylon namespace use -c <context> -t <tenant> -s <state_id>
```

Example for this project:

```bash
babylon namespace use -c tenant-bmc -t tenant-bmc -s tenant-bmc
```

### View active namespace

```bash
babylon namespace get-contexts
```

### List available states

```bash
babylon namespace get-states local    # From local machine
babylon namespace get-states remote   # From Azure remote storage
```

---

## 2. Project Initialization

Scaffold a new Babylon project structure:

```bash
babylon init
babylon init --project-folder my_project --variables-file my_vars.yaml
```

This creates the `project/` folder with YAML templates (`Organization.yaml`, `Solution.yaml`, `Workspace.yaml`, etc.) and a `variables.yaml` file.

---

## 3. Apply (Deploy Resources)

The `apply` command deploys resources defined in YAML files from a directory.

### Deploy everything

```bash
babylon apply project/
```

### Deploy specific resources with `--include`

Deploy only selected resource types:

```bash
babylon apply --include organization project/
babylon apply --include solution project/
babylon apply --include workspace project/
babylon apply --include dataset project/
```

Multiple includes:

```bash
babylon apply --include organization --include solution project/
```

### Skip resources with `--exclude`

Deploy all except certain resources:

```bash
babylon apply --exclude webapp project/
```

### Use a custom variables file

```bash
babylon apply --var-file ./my_variables.yaml project/
```

### Override namespace inline

```bash
babylon apply -c tenant-bmc -t tenant-bmc -s tenant-bmc project/
```

### Dry run (preview without applying)

```bash
babylon -n apply project/
```

---

## 4. Destroy (Remove Resources)

Remove deployed resources:

```bash
babylon destroy
babylon destroy --include solution
babylon destroy --exclude workspace
```

---

## 5. API Commands

Direct interactions with the CosmoTech API. All API commands support:

| Flag | Description |
|---|---|
| `-c, --context` | Context name |
| `-t, --tenant` | Tenant ID |
| `-s, --state-id` | State ID |
| `-o, --output` | Output format: `json`, `yaml`, `wide` |
| `-f, --file` | Save response to a file |

### Organizations

```bash
babylon api organizations list
babylon api organizations get --oid o-lp2zy1jlr8kw
babylon api organizations create project/Organization.yaml
babylon api organizations update project/Organization.yaml --oid o-lp2zy1jlr8kw
babylon api organizations delete --oid o-lp2zy1jlr8kw
```

### Solutions

```bash
babylon api solutions list --oid o-lp2zy1jlr8kw
babylon api solutions get --oid o-lp2zy1jlr8kw --sid sol-veqgv47ejl1j
babylon api solutions create project/Solution.yaml --oid o-lp2zy1jlr8kw
babylon api solutions update project/Solution.yaml --oid o-lp2zy1jlr8kw --sid sol-veqgv47ejl1j
babylon api solutions delete --oid o-lp2zy1jlr8kw --sid sol-veqgv47ejl1j
```

### Workspaces

```bash
babylon api workspaces list --oid o-lp2zy1jlr8kw
babylon api workspaces get --oid o-lp2zy1jlr8kw --wid w-q4n5oomrm6ml
babylon api workspaces create project/Workspace.yaml --oid o-lp2zy1jlr8kw --sid sol-veqgv47ejl1j
babylon api workspaces update project/Workspace.yaml --oid o-lp2zy1jlr8kw --wid w-q4n5oomrm6ml
babylon api workspaces delete --oid o-lp2zy1jlr8kw --wid w-q4n5oomrm6ml
```

### Datasets

```bash
babylon api datasets list --oid o-lp2zy1jlr8kw --wid w-q4n5oomrm6ml
babylon api datasets get --oid o-lp2zy1jlr8kw --wid w-q4n5oomrm6ml --did <dataset_id>
babylon api datasets create payload.yaml --oid o-lp2zy1jlr8kw --wid w-q4n5oomrm6ml
babylon api datasets delete --oid o-lp2zy1jlr8kw --wid w-q4n5oomrm6ml --did <dataset_id>

# Dataset parts
babylon api datasets list-parts --oid o-lp2zy1jlr8kw --wid w-q4n5oomrm6ml --did <dataset_id>
babylon api datasets create-part payload.yaml --oid o-lp2zy1jlr8kw --wid w-q4n5oomrm6ml --did <dataset_id>
babylon api datasets download-part --oid o-lp2zy1jlr8kw --wid w-q4n5oomrm6ml --did <dataset_id> --dpid <part_id>
babylon api datasets delete-part --oid o-lp2zy1jlr8kw --wid w-q4n5oomrm6ml --did <dataset_id> --dpid <part_id>

# Query data from a dataset part
babylon api datasets query-data --oid o-lp2zy1jlr8kw --wid w-q4n5oomrm6ml --did <dataset_id> --dpid <part_id> \
  --selects "col1,col2" --group-bys "col1" --limit 100
```

### API About

```bash
babylon api about
```

---

## 6. Output Formatting

Add `-o` to any API command to change the output:

```bash
babylon api solutions list --oid o-lp2zy1jlr8kw -o json
babylon api solutions list --oid o-lp2zy1jlr8kw -o yaml
babylon api solutions list --oid o-lp2zy1jlr8kw -o wide
```

Save to file:

```bash
babylon api solutions get --oid o-lp2zy1jlr8kw --sid sol-veqgv47ejl1j -o json -f solution_backup.json
```

---

## 7. Common Workflows

### Full deployment from scratch

```bash
babylon namespace use -c tenant-bmc -t tenant-bmc -s tenant-bmc
babylon apply project/
```

### Deploy only the solution (e.g., after updating run templates)

```bash
babylon apply --include Solution project/
```

### Deploy everything except the webapp

```bash
babylon apply --exclude Webapp project/
```

### Debug with verbose logging

```bash
babylon -v DEBUG apply project/
babylon -v DEBUG api solutions get --oid o-lp2zy1jlr8kw --sid sol-veqgv47ejl1j
```

---

## 8. Project File Structure

```
project/
├── Organization.yaml    # Organization definition
├── Solution.yaml        # Solution + run templates + parameters
├── Workspace.yaml       # Workspace configuration
└── Webapp.yaml          # Web application settings
state.yaml               # Current namespace state (context, tenant, IDs)
variables.yaml           # Template variables used by Babylon
```

### Key IDs for this project (from `state.yaml`)

| Resource | ID |
|---|---|
| Organization | `o-lp2zy1jlr8kw` |
| Solution | `sol-veqgv47ejl1j` |
| Workspace | `w-q4n5oomrm6ml` |

---

## Quick Reference Card

| Task | Command |
|---|---|
| Set namespace | `babylon namespace use -c <ctx> -t <tenant> -s <state>` |
| Show namespace | `babylon namespace get-contexts` |
| Init project | `babylon init` |
| Deploy all | `babylon apply project/` |
| Deploy only solution | `babylon apply --include solution project/` |
| Deploy excluding webapp | `babylon apply --exclude webapp project/` |
| Dry run | `babylon -n apply project/` |
| Destroy all | `babylon destroy` |
| List solutions | `babylon api solutions list --oid <oid>` |
| Get solution | `babylon api solutions get --oid <oid> --sid <sid>` |
| Verbose mode | `babylon -v DEBUG <command>` |