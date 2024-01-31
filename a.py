import boto3
import csv

csv_file_path = '/home/ec2-user/environment/server/generated_data_with_weather_season.csv'

# AWS DynamoDB 클라이언트 생성
dynamodb = boto3.resource('dynamodb')

# DynamoDB 테이블 선택 (본인의 테이블 이름으로 변경)
table_name = 'train-TEAM-004'
table = dynamodb.Table(table_name)

# CSV 파일에서 데이터 읽어오기
with open(csv_file_path, 'r') as csvfile:
    csvreader = csv.DictReader(csvfile)
    
    # batch_writer를 사용하여 여러 아이템을 한 번에 삽입
    with table.batch_writer() as batch:
        for id, row in enumerate(csvreader):
            row['item_id'] = id
            batch.put_item(Item=row)

print("CSV 데이터가 DynamoDB에 성공적으로 적재되었습니다.")