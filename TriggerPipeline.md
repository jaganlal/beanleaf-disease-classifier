## Queue build pipeline
curl -u .:<pat> -X POST https://dev.azure.com/{organization}/{project_id}/_apis/build/builds\?api-version\=6.0 -H 'Content-Type: application/json' -d '{"definition": {"id": 3}}

## Trigger DevOps build pipeline using WebHooks
https://dev.azure.com/<ADO Organization>/_apis/public/distributedtask/webhooks/<WebHook Name>?api-version=6.0-preview

```
resources:
  webhooks:
    - webhook: RetrainBeanleafModelTrigger  ### Webhook alias
      connection: RetrainBeanleafModelSC    ### Incoming webhook service connection
      filters:
        - path: repositoryName      ### JSON path in the payload
          value: maven-releases     ### Expected value in the path provided
        - path: action
          value: CREATED
steps:
- task: PowerShell@2
  inputs:
    targetType: 'inline'
    ### JSON payload data is available in the form of ${{ parameters.<WebhookAlias>.<JSONPath>}}
    script: |
      Write-Host ${{ parameters.MyWebhookTrigger.repositoryName}}
      Write-Host ${{ parameters.MyWebhookTrigger.component.group}}
```

### Commands
Get Project IDs: `curl -u :<pat> https://dev.azure.com/{organization}/_apis/projects/`



### References
[Use personal access tokens](https://learn.microsoft.com/en-us/azure/devops/organizations/accounts/use-personal-access-tokens-to-authenticate?view=azure-devops&tabs=Windows)
[Builds - Queue](https://learn.microsoft.com/en-us/rest/api/azure/devops/build/builds/queue?view=azure-devops-rest-6.0)
[Definitions - List](https://learn.microsoft.com/en-us/rest/api/azure/devops/build/definitions/list?view=azure-devops-rest-6.0)
[Webhook Trigger using Azure DevOps and Jenkins](https://medium.com/globant/webhook-trigger-using-azure-devops-and-jenkins-75656c0c56c4)
[Step-by-step: trigger an Azure Pipeline when a task item is updated in Azure Boards](https://www.linkedin.com/pulse/step-by-step-trigger-azure-pipeline-when-task-item-lahiri-cristofori)
[Triggers in pipelines](https://github.com/microsoft/azure-pipelines-yaml/blob/master/design/pipeline-triggers.md)
[Trigger azure pipeline via webhook?](https://stackoverflow.com/questions/60555358/trigger-azure-pipeline-via-webhook)
    [Generic webhook based triggers for YAML pipelines](https://learn.microsoft.com/en-us/azure/devops/release-notes/2020/pipelines/sprint-172-update?WT.mc_id=DOP-MVP-21138#generic-webhook-based-triggers-for-yaml-pipelines)
    [Trigger a pipeline using a webhook](https://levelup.gitconnected.com/trigger-a-pipeline-using-webhook-586a664addd7)
    [Define resources in YAML](https://learn.microsoft.com/en-us/azure/devops/pipelines/process/resources?view=azure-devops&tabs=schema)
[Triggering a build from a webhook]