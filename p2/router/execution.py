from fastapi import APIRouter, BackgroundTasks

from p2.schema import execution
from p2.provider import execution as provider


router = APIRouter()


@router.post("/executions/executeBlueprint",
             name="Create blueprint execution",
             tags=["Execution"])
async def create_execution(exec: execution.CreateBlueprintExecution,
                           bg_task: BackgroundTasks):
    bg_task.add_task(provider.create_execution, exec)
    return {"msg": "All good"}
