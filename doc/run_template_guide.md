# How to Add a New RunTemplate

This guide explains step-by-step how to add a new RunTemplate to the Build My Calculator Solution.

## Overview

Adding a RunTemplate requires changes in three places:

1. **`project/Solution.yaml`** — Declare the template, its parameters, and parameter groups.
2. **`RunTemplates/<YourTemplateName>/`** — Create the folder with `run.json` (orchestration) and `main.py` (logic).
3. **`requirements.txt`** — Add any new Python dependencies your template needs.

---

## Step 1 — Declare the RunTemplate in `Solution.yaml`

Open `project/Solution.yaml` and add your template under `spec.payload.runTemplates`:

```yaml
runTemplates:
  # ... existing templates ...
  - id: MyNewTemplate            # Unique identifier (must match the folder name)
    name: My New Template
    labels:
      en: My new template description
      fr: Description de mon nouveau template
    parameterGroups:
      - my_param_group           # Reference to a parameter group defined below
    runSizing:
      requests:
        cpu: '1'
        memory: 4Gi
      limits:
        cpu: '1'
        memory: 4Gi
    tags:
      - ETL                      # Free-form tags for categorization
```

### Define parameters

If your template needs input parameters, add them under `spec.payload.parameters`:

```yaml
parameters:
  # ... existing parameters ...
  - id: my_parameter
    labels:
      en: My parameter
      fr: Mon paramètre
    varType: string               # string, int, float, bool, enum, or %DATASET_PART_ID_FILE% for file uploads
    additionalData:
      description: A short description of the parameter
```

For a **file upload** parameter (CSV), use:

```yaml
  - id: my_file_parameter
    labels:
      en: My CSV file
      fr: Mon fichier CSV
    varType: '%DATASET_PART_ID_FILE%'
    additionalData:
      defaultFileTypeFilter: '.csv'
      shouldRenameFileOnUpload: true
```

### Define parameter groups

Group your parameters under `spec.payload.parameterGroups`:

```yaml
parameterGroups:
  # ... existing groups ...
  - id: my_param_group
    labels:
      en: My parameter group
      fr: Mon groupe de paramètres
    parameters:
      - my_parameter
```

---

## Step 2 — Create the RunTemplate folder

Create a new directory: `RunTemplates/MyNewTemplate/`

### 2.1 — `run.json` (orchestration pipeline)

This file defines the execution steps. There are two common patterns:

#### Pattern A: ETL (data processing only)

Use this when your template processes data and uploads results to a dataset.

```json
{
  "steps": [
    {
      "id": "fetch_parameters",
      "command": "csm-data",
      "arguments": [
        "api",
        "run-load-data"
      ],
      "useSystemEnvironment": true
    },
    {
      "id": "my_new_template",
      "command": "python",
      "arguments": [
        "code/run_templates/MyNewTemplate/main.py"
      ],
      "precedents": [
        "fetch_parameters"
      ],
      "useSystemEnvironment": true
    }
  ]
}
```

#### Pattern B: Simulation (processing + result output to store)

Use this when your template produces result CSVs that should be sent to the result store (e.g., for visualization in the webapp).

```json
{
  "steps": [
    {
      "id": "fetch_parameters",
      "command": "csm-data",
      "arguments": [
        "api",
        "run-load-data"
      ],
      "useSystemEnvironment": true
    },
    {
      "id": "my_new_template",
      "command": "python",
      "arguments": [
        "code/run_templates/MyNewTemplate/main.py"
      ],
      "precedents": [
        "fetch_parameters"
      ],
      "useSystemEnvironment": true
    },
    {
      "id": "load-store",
      "command": "csm-data",
      "arguments": [
        "store",
        "load-csv-folder",
        "--csv-folder",
        "/mnt/scenariorun-parameters"
      ],
      "useSystemEnvironment": true,
      "precedents": [
        "my_new_template"
      ]
    },
    {
      "id": "send-results-store",
      "command": "csm-data",
      "arguments": [
        "store",
        "output"
      ],
      "useSystemEnvironment": true,
      "precedents": [
        "load-store"
      ]
    }
  ]
}
```

> **Important:** The Python path in `run.json` must follow the pattern `code/run_templates/<FolderName>/main.py`. This maps to `RunTemplates/<FolderName>/main.py` in the repository, because the `Dockerfile` copies `RunTemplates/` into `/pkg/share/code/run_templates/`.

### 2.2 — `main.py` (business logic)

Create the Python entry point. Here is a minimal skeleton:

```python
from pathlib import Path

from cosmotech.coal.utils.configuration import Configuration
from cosmotech.coal.utils.logger import get_logger
from cosmotech.coal.utils.input_collector import ENVIRONMENT_INPUT_COLLECTOR as InputCollector

LOGGER = get_logger("MY_NEW_TEMPLATE")
CSM_CONFIG = Configuration()

RUNNER_ID = CSM_CONFIG.cosmotech.runner_id
PARAMETERS_PATH = CSM_CONFIG.cosmotech.parameters_absolute_path
DATASET_PATH = CSM_CONFIG.cosmotech.dataset_absolute_path


def main():
    # Fetch a parameter value
    my_param_value = InputCollector.fetch("my_parameter")
    LOGGER.info(f"Received parameter: {my_param_value}")

    # --- Your processing logic here ---

    # (Optional) Write output CSV to PARAMETERS_PATH for store output
    output_path = Path(PARAMETERS_PATH) / "output.csv"
    # result_df.to_csv(output_path, index=False)

    LOGGER.info("MyNewTemplate run completed successfully.")


if __name__ == "__main__":
    main()
```

#### Useful SDK utilities

| Import | Purpose |
|---|---|
| `InputCollector.fetch("param_id")` | Retrieve a parameter value (string, file path, etc.) |
| `Configuration()` | Access runner ID, paths, and environment config |
| `get_logger("NAME")` | Create a named logger |
| `DatasetApi().upload_dataset_parts(dataset_id, files, ...)` | Upload files to a dataset (ETL pattern) |
| `RunnerApi().get_runner_metadata(runner_id=...)` | Get runner metadata including linked dataset IDs |

To use `DatasetApi` or `RunnerApi`, add these imports:

```python
from cosmotech.coal.cosmotech_api.apis.dataset import DatasetApi
from cosmotech.coal.cosmotech_api.apis.runner import RunnerApi
```

---

## Step 3 — Update `requirements.txt` (if needed)

If your template uses Python packages not already listed in `requirements.txt`, add them at the end of the file.

Example — adding `scikit-learn`:

```text
# My new template dependencies
scikit-learn~=1.5
```

## Step 4 — Build and update solution

After making changes, rebuild the Docker image and update the solution

```bash
docker login aks-bmc.azure.platform.cosmotech.com -u tenant-bmc -p <harbor_password>
docker build -t aks-bmc.azure.platform.cosmotech.com/tenant-bmc/simulator:0.1.0-dev .
docker push aks-bmc.azure.platform.cosmotech.com/tenant-bmc/simulator:0.1.0-dev
```

Apply changes with Babylon

```bash
babylon namespace use -c tenant-bmc -t tenant-bmc -s tenant-bmc
babylon apply --exclude webapp project/
```

---

## Checklist

- [ ] RunTemplate declared in `project/Solution.yaml` with a unique `id`
- [ ] Parameters and parameter groups defined in `Solution.yaml`
- [ ] `RunTemplates/<Name>/run.json` created with the correct step pipeline
- [ ] `RunTemplates/<Name>/main.py` created with the business logic
- [ ] Python path in `run.json` matches `code/run_templates/<Name>/main.py`
- [ ] New dependencies added to `requirements.txt` (if any)
- [ ] Docker image builds successfully
