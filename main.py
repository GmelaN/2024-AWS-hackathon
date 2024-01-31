from fastapi import FastAPI
from base.base_model import CommonResponseModel
from base.response_code import ResponseCode
from service.service import Service
from repository.repository import Repository
from dto.dto import GoodsDataDTO, PredictionDTO

from dotenv import load_dotenv

import os


# ENV 설정
load_dotenv("./.env")

DB_ENDPOINT_URL = os.getenv("DB_ENDPOINT_URL")
DB_REGION_NAME = os.getenv("DB_REGION_NAME")
DB_ACCESS_KEY_ID = os.getenv("DB_ACCESS_KEY_ID")
DB_SECRET_ACCESS_KEY = os.getenv("DB_SECRET_ACCESS_KEY")

# 서비스 인스턴스
service = Service(repo=Repositroy(envs=(DB_ENDPOINT_URL, DB_REGION_NAME, DB_ACCESS_KEY_ID, DB_SECRET_ACCESS_KEY)))

app = FastAPI()

@app.get("/", response_model=CommonResponseModel)
async def root():
    return CommonResponseModel(success=True, data=f"hello world!", code=ResponseCode.SUCCESS)

"""
특정 가게의 재고 목록 조회
"""
@app.get("/stores/{store_id}/inventories", response_model=CommonResponseModel)
async def create_inventory(store_id: int):
    data: list[GoodsDataDTO] = service.get_inventories_list(store_id)
    data = [i.dict() for i in data]
    return CommonResponseModel(success=True, code=ResponseCode.SUCCESS, data=data)


"""
특정 가게의 머신러닝 예측값 조회
"""
@app.get("/stores/{store_id}/predictions", response_model=CommonResponseModel)
async def get_sales_rate_predictions(store_id: int):
    data: list[PredictionDTO] = service.get_sales_rate_predictions(store_id)
    data = [i.dict() for i in data]
    return CommonResponseModel(success=True, code=ResponseCode.SUCCESS, data=data)



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
