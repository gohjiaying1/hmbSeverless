## Function takes in user (str) and request (item(str), quantity(int))
import json
import boto3
import logging
import os

#define dynamodb request variables
hmb_request_table = os.environ['REQUEST_TABLE']
required_request_list_fields = ['user', 'items']
required_item_fields = ['item']

#define boto variables
dynamodb = boto3.client('dynamodb')


def is_valid_request (data) :
    for field in required_request_list_fields:
        print(field)
        if field not in data:
            logging.error("Validation Failed")
            raise Exception("Couldn't create the request items.")
            return
    else:
        return True


def is_valid_item (item):
    if "item" not in item :
            logging.error("Validation Failed")
            raise Exception("Couldn't create the request item.")
    else:
        return True


def update_items_bought (data):
    key = {}
    key['User'] = {"S": data['user']}
    items = data['items']
    for item in items:
        key['Item'] = {"S": item['item']}
        update_expression = "SET Quantity = :q"
        expression_attribute_values = {}
        expression_attribute_values[':q'] = {"N": str(0)}
        response = boto_update_item(hmb_request_table, key, update_expression, expression_attribute_values)
        if response["HTTPStatusCode"] != 200{
            logging.error(response)
        }
    return


def boto_update_item (table_name, key, update_expression,expression_attribute_values) :
    response = dynamodb.update_item(
        TableName = table_name,
        Key = key,
        UpdateExpression = update_expression,
        ExpressionAttributeValues = expression_attribute_values
    )

    return response


def lambda_handler (event, context):
    # TODO implement
    data = json.loads(event['body'])
    if is_valid_request(data):
        update_items_bought(data)
    
        to_return = {
            "statusCode": 200,
            "body": json.dumps(data)
        }

        return to_return
    else:
        raise Exception("Something went wrong")
        return