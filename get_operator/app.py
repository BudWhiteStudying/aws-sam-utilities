import boto3
from shared_utils import get_item, build_success_response, build_failure_response

boto3_client = boto3.client('dynamodb')
table_name = 'Operator'


# sample invocation:
# http://127.0.0.1:3000/operator?id=SOME_ID


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
        return build_failure_response(repr(e))
    return build_success_response(return_data)
