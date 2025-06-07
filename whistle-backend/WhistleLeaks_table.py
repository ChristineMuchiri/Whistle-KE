import boto3
import os
# connecting to dynamodb local
dynamodb = boto3.resource(
    'dynamodb',
    region_name='us-east-1',
    endpoint_url='http://localhost:8000'
)

def whistle_leaks_table():
    table_name = "WhistleLeaks"
    
    existing_tables = dynamodb.meta.client.list_tables()["TableNames"]
    if table_name in existing_tables:
        print(f"Table '{table_name}' already exists.")
        return
    
    table = dynamodb.create_table(
        TableName=table_name,
        KeySchema=[
            {
                'AttributeName': 'leak_id',
                'KeyType': 'HASH'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'leak_id',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
            }
    )
    
    print("Creating table.....")
    table.wait_until_exists()
    print(f"Table '{table_name}' created successfully.")
    
if __name__ == "__main__":
    whistle_leaks_table()