from base.repository import Repository
from base.dto import GoodsDataDTO, PredictionDTO


class Service:
    def __init__(self, repo: Repository):
        self.repo = repo

    def get_inventories_list(self, store_id) -> list[GoodsDataDTO]:
        return self.repo.get_inventories_list(store_id)
        
    def append_inventory(self, data: GoodsDataDTO):
        try:
            self.repo.append_inventories_list(data)
        except:
            raise Exception()

    def get_sales_rate_predictions(self, store_id) -> list[PredictionDTO]:
        return [].append(PredictionDTO(0.0))
    
    def buy_inventory(self, data: GoodsDataDTO) -> bool:
        self.repo.delete_inventory(data)
        data.amount = int(data.amount)

        if data.amount == 1:
            return True

        data.amount -= 1
        data.amount = str(data.amount)
        self.append_inventory(data)
        return True
