# Bean leaf disease classifier
MLOps demo for classifying bean leaf diseases

## 1. Model development
Data scientists/engineers can begin their ML journey from this folder to train, test and evaluate model(s)
> **Folder name**: 1_model_development

<br/>

## 2. Cloud setup
Code to provision basic resources - workspace, compute, dataset
> **Folder name**: 2_cloud_setup

<br/>

## 3. Training locally using Azure dataset
Notebook to train, test & evaludate model using azure dataset. This notebook comes handy if various datasources needs to be tested
> **Folder name**: 3_azure_training

<br/>

## 4. Scripts to use for CI, CT & CD
This contains sequence of pipeline tasks (for both model building & deployment) that gets triggered everytime when new code is checked in and approved.
> **Folder name**: 4_devops_pipeline

<br/>

## 5. Training code that creates the model
Once the local training is completed, create `train.py` file to create the model and save it in azure
> **Folder name**: 5_model_training_from_azure_pipeline

<br/>

## 6. Deployment
Once model is ready for deployment, create `score.py` for inference and follow `inferenceConfig.yml` file.
* For AKS deployment use `aksDeploymentConfig.yml`
* For ACI deployment use `aciDeploymentConfig.yml`
> **Folder name**: 6_deployment
