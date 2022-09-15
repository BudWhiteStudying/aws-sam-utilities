import json
import boto3
import traceback

boto3_client = boto3.client('dynamodb')
shift_table_name = 'Shift'
operator_table_name = 'Operator'


# sample invocation:
# http://127.0.0.1:3000/shift?id=SOME_ID

def get_item(dynamodb_client, table_name, key):
    return_data = dynamodb_client.get_item(
        TableName=table_name,
        Key=key
    )
    return return_data['Item'] if 'Item' in return_data else None


def get_item_around_date(dynamodb_client, table_name, reference_date):
    return_data = dynamodb_client.scan(
        TableName=table_name,
        ScanFilter={
            'start_time': {
                'AttributeValueList': [
                    {'S': reference_date}
                ],
                'ComparisonOperator': 'LE'
            },
            'end_time': {
                'AttributeValueList': [
                    {'S': reference_date}
                ],
                'ComparisonOperator': 'GE'
            }
        }
    )
    return return_data['Items'][0] if 'Items' in return_data and len(return_data['Items']) > 0 else None


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
        shift_id = event['queryStringParameters']['id'] \
            if 'id' in event['queryStringParameters'] \
            else None
        shift_reference_date = event['queryStringParameters']['reference-date'] \
            if 'reference-date' in event['queryStringParameters'] \
            else None

        if shift_id is None and shift_reference_date is None:
            print('Provide either the "id" parameter or the "reference-date" parameter')
            raise Exception('Provide either the "id" parameter or the "reference-date" parameter')

        shift = get_item(
            boto3_client,
            shift_table_name,
            {'id': {'S': shift_id}}
        ) if shift_id is not None else get_item_around_date(
            boto3_client,
            shift_table_name,
            shift_reference_date
        )

        operator = get_item(
            boto3_client,
            operator_table_name,
            {'id': {'S': shift['operator_id']['S']}}
        ) if shift is not None else None

        # TODO: manage None data
        if shift is not None:
            shift['operator_name'] = {'S': operator['name']['S']}
    except Exception as e:
        print('we failed: ' + repr(e))
        return build_failure_response(shift_table_name, repr(e))
    return build_success_response(shift_table_name, shift)
