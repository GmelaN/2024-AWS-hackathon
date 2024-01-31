from dto.dto import DataDTO
# import boto3

# client = boto3.client('dynamodb')

# client.put_item(
#     Item={

#     }
# )

class Repository:
    def get_inventories_list(self, store_id: int) -> DataDTO:
        return [DataDTO(sales=100, inventory=50, price=20, date=20230101, category="Books")]
