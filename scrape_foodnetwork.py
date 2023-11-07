import boto3

dynamodb = boto3.resource(service_name = 'dynamodb',region_name = 'us-east-2',
              aws_access_key_id = 'AKIAUQ5RSVGJSYOLOFNE',
              aws_secret_access_key = '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')

table = dynamodb.Table('recipe')

response = table.put_item(
    Item={
        "recipe_id": 1,
        "name": "Ham"
    },
)

print(response)