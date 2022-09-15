import boto3
import uuid
from shared_utils import put_item, build_success_response, build_failure_response

boto3_client = boto3.client('dynamodb')
table_name = 'Shift'


# sample invocation:
# http://127.0.0.1:3000/shift?start_time=SOME_VALUE&end_time=SOME_VALUE&operator_id=SOME_VALUE


def lambda_handler(event, context):
    try:
        shift_start_time = event['queryStringParameters']['start-time']
        shift_end_time = event['queryStringParameters']['end-time']
        shift_operator_id = event['queryStringParameters']['operator-id']

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
        return build_failure_response(repr(e))
    return build_success_response(return_data)
