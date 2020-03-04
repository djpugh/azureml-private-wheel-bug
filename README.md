# Reproduction steps for AzureML Private Wheel Error


1. Configure an AzureML workspace with storage vNet
2. Set environment variables as appropriate:
    * *AML_SUBSCRIPTION_ID*
    * *AML_RESOURCE_GROUP*
    * *AML_WORKSPACE_NAME*
    * *AML_COMPUTE_NAME*

3. Make sure that you have local authentication for accessing the workspace

4. Run: `python submit.py`
    This will output a portal run link, and that run is expected to pass

5. Run: `python submit.py --private-wheel`
    This will output a portal run link, and that run is expected to fail
    The expected error message is a 500 error after a long time (10+ minutes), with an error message that resembles:
    ```
    {
     "error": {
        "code": "ServiceError",
        "message": "InternalServerError",
        "detailsUri": null,
        "target": null,
        "details": [],
        "innerError": null,
        "debugInfo": {
            "type": "Microsoft.Azure.Storage.StorageException",
            "message": "This request is not authorized to perform this operation.",
            "stackTrace": " at Microsoft.Azure.Storage.Core.Executor.Executor.ExecuteAsync[T](RESTCommand`1 cmd, IRetryPolicy policy, OperationContext operationContext, CancellationToken token)\
                            at Microsoft.MachineLearning.EnvironmentManagement.Services.CondaFileMutator.GetBlobContainer(String packageUri, WorkspaceResources workspaceResources) in /home/vsts/work/1/s/src/azureml-api/src/EnvironmentManagement/Services/CondaFileMutator.cs:line 325\
                            at Microsoft.MachineLearning.EnvironmentManagement.Services.CondaFileMutator.RenewBlobSasToken(String packageUri, WorkspaceResources workspaceResources) in /home/vsts/work/1/s/src/azureml-api/src/EnvironmentManagement/Services/CondaFileMutator.cs:line 232\
                            at Microsoft.MachineLearning.EnvironmentManagement.Services.CondaFileMutator.RenewPrivatePackageSasUrls(WorkspaceResources workspaceResources) in /home/vsts/work/1/s/src/azureml-api/src/EnvironmentManagement/Services/CondaFileMutator.cs:line 218\
                            at Microsoft.MachineLearning.EnvironmentManagement.Services.CondaFileMutator.GetSerializedCondaFileWithSas(WorkspaceResources workspaceResources) in /home/vsts/work/1/s/src/azureml-api/src/EnvironmentManagement/Services/CondaFileMutator.cs:line 132\
                            at Microsoft.MachineLearning.EnvironmentManagement.EntryPoints.Api.Controllers.CloudMaterializationController.StartImageBuild(Guid subscriptionId, String resourceGroupName, String workspaceName, String environmentName, String environmentVersion) in /home/vsts/work/1/s/src/azureml-api/src/EnvironmentManagement/EntryPoints/Api/Controllers/CloudMaterializationController.cs:line 131\
                            at lambda_method(Closure , Object )\
                            at Microsoft.AspNetCore.Mvc.Internal.ActionMethodExecutor.AwaitableObjectResultExecutor.Execute(IActionResultTypeMapper mapper, ObjectMethodExecutor executor, Object controller, Object[] arguments)\
                            at Microsoft.AspNetCore.Mvc.Internal.ControllerActionInvoker.InvokeActionMethodAsync()\
                            at Microsoft.AspNetCore.Mvc.Internal.ControllerActionInvoker.InvokeNextActionFilterAsync()\
                            at Microsoft.AspNetCore.Mvc.Internal.ControllerActionInvoker.Rethrow(ActionExecutedContext context)\
                            at Microsoft.AspNetCore.Mvc.Internal.ControllerActionInvoker.Next(State& next, Scope& scope, Object& state, Boolean& isCompleted)\
                            at Microsoft.AspNetCore.Mvc.Internal.ControllerActionInvoker.InvokeInnerFilterAsync()\
                            at Microsoft.AspNetCore.Mvc.Internal.ResourceInvoker.InvokeNextExceptionFilterAsync()",
            "innerException": null,
            "data": {},
            "errorResponse": null
            }
        }
    }
    ```