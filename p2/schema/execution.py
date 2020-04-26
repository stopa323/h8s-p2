from pydantic import BaseModel, Field


class CreateBlueprintExecution(BaseModel):
    blueprint_id: str = Field(..., alias="blueprintId",
                              title="Id of the blueprint to excute")

    class Config:
        orm_mode = True

        schema_extra = {
            "description": "TBD",
            "example": {"blueprintId": "00000000-0000-0000-0000-000000000001"}}
