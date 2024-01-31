from repository.repository import Repository
from dto.dto import GoodsDataDTO, PredictionDTO

class Service:
    def __init__(self, repo: Repository):
        self.repo = repo

    def get_inventories_list(self, store_id) -> list[GoodsDataDTO]:
        return self.repo.get_inventories_list(store_id)

    def get_sales_rate_predictions(self, store_id) -> list[PredictionDTO]:
        return [].append(PredictionDTO(0.0))
