import json


def get_item(dynamodb_client, table_name, key):
    return_data = dynamodb_client.get_item(
        TableName=table_name,
        Key=key
    )
    return return_data['Item'] if 'Item' in return_data else None


def put_item(dynamodb_client, table_name, item):
    return_data = dynamodb_client.put_item(
        TableName=table_name,
        Item=item
    )
    return return_data


def delete_item(dynamodb_client, table_name, key):
    return_data = dynamodb_client.delete_item(
        TableName=table_name,
        Key=key
    )
    return return_data


def get_items(dynamodb_client, table_name):
    return_data = dynamodb_client.scan(
        TableName=table_name
    )
    return return_data['Items'] if 'Items' in return_data else None


def build_success_response(success_data):
    return {
        "statusCode": 200,
        "body": {
            "message": "Operation executed successfully",
            "data": success_data
        }
    }


def build_failure_response(failure_data):
    return {
        "statusCode": 500,
        "body": {
            "message": "Problems executing the operation",
            "data": failure_data
        }
    }
