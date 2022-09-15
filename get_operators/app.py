import json
import boto3

boto3_client = boto3.client('dynamodb')
table_name = 'Operator'


# sample invocation:
# http://127.0.0.1:3000/operator?id=SOME_ID

def get_items(dynamodb_client, table_name):
    return_data = dynamodb_client.scan(
        TableName=table_name
    )
    return return_data['Items'] if 'Items' in return_data else None


def build_success_response(table_name, success_data):
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Got items on table {table}: {data}".format(table=table_name, data=success_data)
        })
    }


def build_failure_response(table_name, failure_data):
    return {
        "statusCode": 500,
        "body": json.dumps({
            "message": "Problems getting items on table {table}: {error}".format(
                table=table_name, error=failure_data)
        })
    }


def lambda_handler(event, context):
    try:

        return_data = get_items(
            boto3_client,
            table_name
        )
    except Exception as e:
        print('we failed: ' + repr(e))
        return build_failure_response(table_name, repr(e))
    return build_success_response(table_name, return_data)
