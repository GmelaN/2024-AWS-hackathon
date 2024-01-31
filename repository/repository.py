from dto.dto import GoodsDataDTO
import boto3


class Repository:
    def __init__(self, envs: list):
        # goods 테이블 연결
        self.goods_resource = boto3.resource("dynamodb")
        self.goods_table = self.goods_resource.Table("goods-TEAM-004")

    def get_inventories_list(self, store_id: int) -> list[GoodsDataDTO]:
        result = self.goods_table.scan()["Items"]
        return result
        # return [
        #     GoodsDataDTO(
        #                 id_=1,
        #                 amount=10,
        #                 discount_time="00:00~24:00",
        #                 original_price=10000,
        #                 discounted_price=8000,
        #                 goods_name="상품명",
        #                 location="서울시 땡떙구",
        #                 date=20240101,
        #                 store_name="상호명",
        #                 category="카테고리",
        #                 photo_url="https://naver.com"
        #     )
        # ]
    

