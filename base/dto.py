from pydantic import BaseModel


class GoodsDataDTO(BaseModel):
        amount: int         # 재고
        discount_time: str  # 할인 시간 "HH:MM~HH:MM"
        original_price: int # 할인 전 가격
        discounted_price: int # 할인 후 가격
        goods_name: str     # 상품명
        store_name: str     # 상호명
        location: str       # 주소
        date: int           # 날짜
        category: str       # 카테고리
        photo_url: str      # 사진 URL


class PredictionDTO(BaseModel):
        predictions: float  # 예측값
