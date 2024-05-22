from azure.ai.ml.entities import Workspace
from azure.ai.ml import MLClient
from azure.identity import DefaultAzureCredential
import os

subscription_id = os.getenv("SUBSCRIPTION_ID")  # preferably using env variable
resource_group = os.getenv("RESOURCE_GROUP")  # preferably using env variable
ml_client = MLClient(DefaultAzureCredential(), subscription_id, resource_group)
workspace_name = "mlw-dp100-sdk"

ws_basic = Workspace(
    name=workspace_name,
    location="eastus",
    display_name="Basic workspace-example",
    description="This example shows how to create a basic workspace"
)

ml_client.workspaces.begin_create(ws_basic).result()
