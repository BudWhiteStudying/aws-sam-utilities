import json
import boto3
from datetime import datetime, timedelta
import traceback

lambda_client = boto3.client('lambda')


# sample invocation:
# http://127.0.0.1:3000/notification_rule?notification-rule-id=SOME_CONFIG

def get_shift_by_date(client, reference_date):
    return_data = client.invoke(
        FunctionName='arn:aws:lambda:us-east-1:725885754378:function:shift-manager-cf-stack-GetNamedShiftFunction-aTb2PqG8t2hZ',
        InvocationType='RequestResponse',
        Payload=json.dumps({
            "queryStringParameters": {
                "reference-date": reference_date
            }})
    )
    if 'Payload' in return_data:
        print('Lambda returned {data}'.format(data=json.load(return_data['Payload'])))
    return return_data['Item'] if 'Item' in return_data else None


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
        current_shift_date = datetime.today()
        next_shift_date = current_shift_date+timedelta(days=1)

        current_shift = get_shift_by_date(lambda_client, current_shift_date.strftime('%Y-%m-%d'))
        next_shift = get_shift_by_date(lambda_client, next_shift_date.strftime('%Y-%m-%d'))
    except Exception as e:
        tb = traceback.format_exc()
        print('we failed: ' + repr(tb))
        return build_failure_response('Lambda', repr(tb))
    return build_success_response('Lambda', {'current_shift': current_shift, 'next_shift': next_shift})
