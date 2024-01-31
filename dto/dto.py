from pydantic import BaseModel


class DataDTO(BaseModel):
        sales: int          # 판매량
        inventory: int      # 재고
        price: int          # 가격
        date: int           # 날짜
        category: str       # 카테고리


class PredictionDTO(BaseModel):
        predictions: float  # 예측값
