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
            "content":  "다음은 시장에 위치한 한 가게의 일별 매출액(만원)을 나타낸 것이다.\n\n"
                        + "가게 이름, 식품의 가격, 날짜, 요일, 음식 카테고리, 날씨, 공휴일 여부"
                        + "'모녀김밥', 2000, '2023-11-10 00:00:00', 'Friday', '분식', '맑음', 0\n"
                        + "예측 판매량: 138.39618\n"
                        + "입력예시:\n"
                        + "'60년 전통떡집', 3000, '2023-05-19 00:00:00', 'Friday', '떡류', '흐림', 0\n"
                        + "예측 판매량: 138.703\n"
                        + "입력예시:\n"
                        + "'창신육회 본점', 9500, '2023-01-17 00:00:00', 'Tuesday', '육회', '눈', 0\n"
                        + "예측 판매량: 138.34218\n"
                        + data
            # "위 데이터를 기반으로 주간 리포트를 작성해주는데 밑에 항목에 관해 작성해줘, 1.판매량 동향 및 수치 분석 / 주간 판매량의 평균과 최대, 최소, 주간 판매량 차이 추이도 그래프로 보여줘, 2. 날씨별 판매량 차이 날씨별로 어떤 판매량 차이를 보였는지 / 3. 요일별 판매량 차이 요일별로 판매량 차이가 나는 부분을 설명, 4.공휴일 평일 비교 특정 공휴일 말고 전체적인 공휴일과 평일의 비교, 5. 기타 사항 / 주어진 데이터로 가게 영업 방식이나 마케팅 전략 등"
        }],
        temperature=0.5
    ).choices[0].message.content

    return CommonResponseModel(success=True, code=ResponseCode.SUCCESS, data=response)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
