import json
import boto3
import uuid

boto3_client = boto3.client('dynamodb')
table_name = 'Operator'


# sample invocation:
# http://127.0.0.1:3000/operator?name=SOME_VALUE

def put_item(dynamodb_client, table_name, item):
    return_data = dynamodb_client.put_item(
        TableName=table_name,
        Item=item
    )
    return return_data


def build_success_response(table_name, success_data):
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Created a new item on table {table}: {data}".format(table=table_name, data=success_data)
        })
    }


def build_failure_response(table_name, failure_data):
    return {
        "statusCode": 500,
        "body": json.dumps({
            "message": "Problems creating a new item on table {table}: {error}".format(
                table=table_name, error=failure_data)
        })
    }


def lambda_handler(event, context):
    try:
        operator_name = event['queryStringParameters']['name']
        print(
            'operator_name is {operator_name}'.format(operator_name=operator_name))

        if operator_name is None:
            print('Missing operator_name')
            raise Exception('Missing operator_id and/or operator_name')

        return_data = put_item(
            boto3_client,
            table_name,
            {
                'id': {'S': str(uuid.uuid4())},
                'name': {'S': operator_name}
            }
        )
    except Exception as e:
        print('we failed: ' + repr(e))
        return build_failure_response(table_name, repr(e))
    return build_success_response(table_name, return_data)
