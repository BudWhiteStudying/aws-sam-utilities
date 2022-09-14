import json
import boto3

boto3_client = boto3.client('dynamodb')
table_name = 'Operator'


# sample invocation:
# http://127.0.0.1:3000/operator?id=SOME_ID

def get_item(dynamodb_client, table_name, key):
    return_data = dynamodb_client.get_item(
        TableName=table_name,
        Key=key
    )
    return return_data


def build_success_response(table_name, success_data):
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Got item on table {table}: {data}".format(table=table_name, data=success_data)
        })
    }


def build_failure_response(table_name, failure_data):
    return {
        "statusCode": 500,
        "body": json.dumps({
            "message": "Problems getting item on table {table}: {error}".format(
                table=table_name, error=failure_data)
        })
    }


def lambda_handler(event, context):
    try:
        operator_id = event['queryStringParameters']['id']

        if operator_id is None:
            print('Missing parameter id')
            raise Exception('Missing parameter id')

        return_data = get_item(
            boto3_client,
            table_name,
            {'id': {'S': operator_id}}
        )
    except Exception as e:
        print('we failed: ' + repr(e))
        return build_failure_response(table_name, repr(e))
    return build_success_response(table_name, return_data)
