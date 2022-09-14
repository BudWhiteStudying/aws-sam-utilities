import json
import boto3
import uuid

boto3_client = boto3.client('dynamodb')
table_name = 'Shift'


# sample invocation:
# http://127.0.0.1:3000/shift?start_time=SOME_VALUE&end_time=SOME_VALUE&operator_id=SOME_VALUE

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
        shift_start_time = event['queryStringParameters']['start_time']
        shift_end_time = event['queryStringParameters']['end_time']
        shift_operator_id = event['queryStringParameters']['operator_id']

        if None in [shift_start_time, shift_end_time, shift_operator_id]:
            print('Missing input data')
            raise Exception('Missing input data')

        return_data = put_item(
            boto3_client,
            table_name,
            {
                'id': {'S': str(uuid.uuid4())},
                'start_time': {'S': shift_start_time},
                'end_time': {'S': shift_end_time},
                'operator_id': {'S': shift_operator_id}
            }
        )
    except Exception as e:
        print('we failed: ' + repr(e))
        return build_failure_response(table_name, repr(e))
    return build_success_response(table_name, return_data)
