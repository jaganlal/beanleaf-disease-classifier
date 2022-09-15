## Use Python 3.x
Display name `Use Python 3.x`

<br/>

## Install python dependencies
> **Task type**: Bash

**Script Path**:
```
$(System.DefaultWorkingDirectory)/_beanleaf-disease-classifier-CI/beanleaf_disease_classifier/a/environment_setup/install-requirements.sh
```
<br/>

## Azure CLI Installation
> **Task type**: Azure CLI

**Inline Script**:
```
az extension add -n azure-cli-ml
```
<br/>

## Create AKS cluster
> **Task type**: Azure CLI

> **Set Working Directory**: $(System.DefaultWorkingDirectory)/_beanleaf-disease-classifier-CI/beanleaf_disease_classifier/a/5_deployment

**Inline Script**:
```
az ml computetarget create aks
                    -g $(ml.resourceGroup)
                    -w $(ml.workspace)
                    -n $(ml.aksClusterName)
                    -l $(ml.region)
                    -s $(ml.aksComputeVMSize)
                    --verbose -a 1
                    --cluster-purpose DevTest
```
<br/>

## Deploy bean leaf disease classification model

> **Task type**: Azure CLI

> **Set Working Directory**: $(System.DefaultWorkingDirectory)/_beanleaf-disease-classifier-CI/beanleaf_disease_classifier/a/5_deployment

### Azure Kubernetes Service
**Inline Script**:
```
az ml model deploy
            -g $(ml.resourceGroup)
            -w $(ml.workspace)
            -n cv-clsifier-deploy-service
            --ct $(ml.aksClusterName)
            -f ../metadata/model.json
            --dc aksDeploymentConfig.yml
            --ic inferenceConfig.yml
            --description "Bean leaf disease classifier deployed in ACI" --overwrite
```

### Azure Container Instances
**Inline Script**:
```
az ml model deploy
            -g $(ml.resourceGroup)
            -w $(ml.workspace)
            -n cv-clsifier-deploy-service
            -f ../metadata/model.json
            --dc aciDeploymentConfig.yml
            --ic inferenceConfig.yml
            --description "Bean leaf disease classifier deployed in ACI" --overwrite
```
<br/>

## Smoke Test
> **Task type**: Azure CLI

> **Set Working Directory**: $(System.DefaultWorkingDirectory)/_beanleaf-disease-classifier-CI/beanleaf_disease_classifier/a

**Inline Script**:
```
pytest tests/smoke/smoke_tests.py
            --log-cli-level=info
            --doctest-modules
            --junitxml=junit/test-results.xml
            --cov=integration_test
            --cov-report=xml
            --cov-report=html
            --scoreurl $(
                            az ml service show
                                    -g $(ml.resourceGroup)
                                    -w $(ml.workspace)
                                    -n cv-clsifier-deploy-service
                                    --query scoringUri -o tsv
                        )
```

## Publish Test Results
