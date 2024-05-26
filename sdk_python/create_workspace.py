
from azure.ai.ml.entities import Workspace
from connect_to_workspace import ml_client

workspace_name = "riskanalyzers-mlw"

ws_basic = Workspace(
    name=workspace_name,
    location="eastus",
    display_name="Basic workspace-example",
    description="This example shows how to create a basic workspace",
)
ml_client.workspaces.begin_create(ws_basic)
