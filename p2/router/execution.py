from fastapi import APIRouter, BackgroundTasks
from asyncio import sleep

from p2.schema import execution


router = APIRouter()


async def f(payload: dict):
    print(payload)
    await sleep(10)
    print("im done")


@router.post("/executions/executeBlueprint",
             name="Create blueprint execution",
             tags=["Execution"])
async def create_execution(exec: execution.CreateBlueprintExecution,
                           bg_task: BackgroundTasks):
    bg_task.add_task(f, exec)
    return {"msg": "All good"}
