import boto3
import uuid
from shared_utils import put_item, build_success_response, build_failure_response

boto3_client = boto3.client('dynamodb')
table_name = 'Operator'


# sample invocation:
# http://127.0.0.1:3000/operator?name=SOME_VALUE


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
        return build_failure_response(repr(e))
    return build_success_response(return_data)
