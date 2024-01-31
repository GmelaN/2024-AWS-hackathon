from fastapi import FastAPI
from base.base_model import CommonResponseModel
from base.response_code import ResponseCode

from fastapi.responses import JSONResponse
from fastapi import HTTPException

# from models import InventoryItem


app = FastAPI()

@app.get("/", response_model=CommonResponseModel)
async def root():
    return CommonResponseModel(success=True, data=f"hello world!", code=ResponseCode.SUCCESS)


@app.get("/stores/inventories/{store_id}", response_model=CommonResponseModel)
async def create_inventory(store_id: int):
    return CommonResponseModel(success=True, data=f"hello world! {store_id}", code=ResponseCode.SUCCESS)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080)
