from base.dto import GoodsDataDTO
import boto3


class Repository:
    def __init__(self, envs: list):
        # goods 테이블 연결
        self.goods_resource = boto3.resource("dynamodb")
        self.goods_table = self.goods_resource.Table("goods-TEAM-004")
        self.id = 3

    def get_inventories_list(self, store_id: int) -> list[GoodsDataDTO]:
        result = self.goods_table.scan()["Items"]
        return result
    

    def append_inventories_list(self, goods_data: GoodsDataDTO) -> None:
        data = goods_data.dict()
        data["id"] = self.id
        self.id += 1
        
        result = self.goods_table.put_item(Item=data)

    def delete_inventory(self, goods_data: GoodsDataDTO) -> None:
        aa = self.goods_table.scan()["Items"]
        dict_data = goods_data.dict()

        for i in range(len(aa)):
            dict_data['id'] = aa[i]["id"]

            if aa[i] == dict_data:
                self.goods_table.delete_item(Key={"id": dict_data["id"]})
                break
