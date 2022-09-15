## Use Python
Display name `Use Python 3.8`

## Install basic python libs
> **Task type**: Bash

**Script Path**:
```
environment_setup/install-requirements.sh
```

## Install Azure CLI
> **Task type**: Azure CLI

**Inline Script**:
```
az extension add -n azure-cli-ml
```

## Create/Use ML Workspace
> **Task type**: Azure CLI

**Inline Script**:
```
az ml workspace create 
                -g $(ml.resourceGroup)
                -w $(ml.workspace)
                -l $(ml.region)
                --exist-ok --yes
```

## Create/Use Compute Target
> **Task type**: Azure CLI

**Inline Script**:
```
az ml computetarget create amlcompute
                    -g $(ml.resourceGroup)
                    -w $(ml.workspace)
                    -n $(ml.computeName)
                    -s $(ml.computeVMSize)
                    --min-nodes $(ml.computeMinNodes)
                    --max-nodes $(ml.computeMaxNodes)
                    --idle-seconds-before-scaledown $(ml.computeIdleSecs) 
```

## Upload Data to Blobstore
> **Task type**: Azure CLI

**Inline Script**:
```
az ml datastore upload
                -w $(ml.workspace)
                -g $(ml.resourceGroup)
                -n $(
                        az ml datastore show-default
                        -w $(ml.workspace)
                        -g $(ml.resourceGroup) --query name -o tsv
                    )
                -p data
                -u beanleaf_dataset
```

## Create Metadata & Model folders
> **Task type**: Bash

**Script**:
```
mkdir metadata && mkdir models
```

## Model Training
> **Task type**: Azure CLI

**Inline Script**
```
az ml run submit-script
            --source-directory ./4_model_training_from_azure_pipeline
            train.py
            --path environment_setup
            --run-configuration-name train
            --resource-group $(ml.resourceGroup)
            --workspace-name  $(ml.workspace)
            --experiment-name $(ml.experimentName)
            --ct $(ml.computeName)
            --output-metadata-file ./metadata/run.json
            --container_name beanleaf_dataset
            --model_path ./models/
            --artifact_loc ./outputs/models/
            --dataset_name beanleaf
            --dataset_desc "MLOps demo for classifying bean leaf diseases"
```
<br/>

## Register Model in to Model Registry
> **Task type**: Azure CLI

**Inline Script**:
```
az ml model register
            -g $(ml.resourceGroup)
            -w $(ml.workspace)
            -n beanleaf_disease_classifier
            --asset-path ./outputs/models/
            -d "Bean leaf diseases classifier"
            --tag "model"="Tensorflow"
            --model-framework Custom
            -f ./metadata/run.json
            -t ./metadata/model.json
```

## Copy File to Pipeline Artifact
> **Task type**: Copy files

**Contents**: 
```
            Source Folder : $(Build.SourcesDirectory)
            Target Folder : $(Build.ArtifactStagingDirectory)
            Contents :
            **/metadata/*
            **/4_model_training_from_azure_pipeline/environment_setup/environment_setup/*
            **/5_deployment/*
            **/inference/*
            **/tests/smoke/*
            **/outputs/*
```

## Publish Pipeline Artifact
> **Task type**: Publish Pipeline Artifacts
**Artifact name:**
```
beanleaf_disease_classifier
```