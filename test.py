import boto3


# goods 테이블 연결
client = boto3.resource("dynamodb")
client = client.Table("goods-TEAM-004")

print(client.scan()["Items"])
