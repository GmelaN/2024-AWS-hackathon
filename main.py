from fastapi import FastAPI
from base.base_model import CommonResponseModel
from base.response_code import ResponseCode
from service.service import Service
from repository.repository import Repository
from dto.dto import DataDTO, PredictionDTO

service = Service(repo=Repository())


app = FastAPI()

@app.get("/", response_model=CommonResponseModel)
async def root():
    return CommonResponseModel(success=True, data=f"hello world!", code=ResponseCode.SUCCESS)

"""
가게 재고 목록 조회
"""
@app.get("/stores/{store_id}/inventories", response_model=CommonResponseModel)
async def create_inventory(store_id: int):
    data: list[DataDTO] = service.get_inventories_list(store_id)
    data = [i.dict() for i in data]
    return CommonResponseModel(success=True, code=ResponseCode.SUCCESS, data=data)


@app.get("/stores/{store_id}/predictions", response_model=CommonResponseModel)
async def get_sales_rate_predictions(store_id: int):
    data: list[PredictionDTO] = service.get_sales_rate_predictions(store_id)
    data = [i.dict() for i in data]
    return CommonResponseModel(success=True, code=ResponseCode.SUCCESS, data=data)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
