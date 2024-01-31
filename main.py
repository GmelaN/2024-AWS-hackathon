from fastapi import FastAPI
from base.base_model import CommonResponseModel
from base.response_code import ResponseCode
from base.service import Service
from base.repository import Repository
from base.dto import GoodsDataDTO, PredictionDTO

from dotenv import load_dotenv

from starlette.middleware.cors import CORSMiddleware

import os


# ENV 설정
load_dotenv("./.env")

DB_ENDPOINT_URL = os.getenv("DB_ENDPOINT_URL")
DB_REGION_NAME = os.getenv("DB_REGION_NAME")
DB_ACCESS_KEY_ID = os.getenv("DB_ACCESS_KEY_ID")
DB_SECRET_ACCESS_KEY = os.getenv("DB_SECRET_ACCESS_KEY")

# 서비스 인스턴스
service = Service(repo=Repository(envs=(DB_ENDPOINT_URL, DB_REGION_NAME, DB_ACCESS_KEY_ID, DB_SECRET_ACCESS_KEY)))

app = FastAPI()

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_model=CommonResponseModel)
async def root():
    return CommonResponseModel(success=True, data=f"hello world!", code=ResponseCode.SUCCESS)

"""
특정 가게의 재고 목록 조회
"""
@app.get("/stores/{store_id}/inventories", response_model=CommonResponseModel)
async def create_inventory(store_id: int):
    data: list[GoodsDataDTO] = service.get_inventories_list(store_id)
    # data = [i.dict() for i in data]
    return CommonResponseModel(success=True, code=ResponseCode.SUCCESS, data=data)


@app.post("/stores/inventories")
async def create_inventory(data: GoodsDataDTO):
    service.append_inventory(data)
    return CommonResponseModel(success=True, code=ResponseCode.SUCCESS, data="")


"""
특정 가게의 머신러닝 예측값 조회
"""
@app.get("/stores/{store_id}/predictions", response_model=CommonResponseModel)
async def get_sales_rate_predictions(store_id: int):
    data: list[PredictionDTO] = service.get_sales_rate_predictions(store_id)
    data = [i.dict() for i in data]
    return CommonResponseModel(success=True, code=ResponseCode.SUCCESS, data=data)


"""
특정 가게의 물품 구매
"""
@app.post("/stores/inventories/buy", response_model=CommonResponseModel)
async def buy_product(data: GoodsDataDTO):
    result: bool = service.buy_inventory(data)
    return CommonResponseModel(success=True, code=ResponseCode.SUCCESS, data=result)

"""
Chat GPT
"""
@app.post("/chat/{data}", response_model=CommonResponseModel)
async def chat(data: str):
    import openai

    OPENAI_API_KEY=""
    openai.api_key = OPENAI_API_KEY
    model = "gpt-3.5-turbo"

    response = openai.chat.completions.create(
        model=model,
        messages=[{
            "role": "user",
            "content": data
        }],
        temperature=0.5
    ).choices[0].message.content

    return CommonResponseModel(success=True, code=ResponseCode.SUCCESS, data=response)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
