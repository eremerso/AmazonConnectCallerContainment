import boto3
import json
import os

#####
# INPUTS
# 'ContactID' - Taken from Amazon Connect event
# 'callerSelection' - (optional) This is useful to track a caller' path through the contact flow. it created a ';' seperated string in DynamoDB 
# 'contained' - BOOL By default set to true.  Pass into the Lambda as 'false' if the caller action fails to meet your definition on containment
# OUTPUTS
# 'callSequence - a ';' delimited list of caller events (customizable) "mainmemu;salesmenu;supportmenu;"            
# 'contained'- true or false
#####

def lambda_handler(event, context):
    dynamodb = boto3.client('dynamodb')
#DynamoDB table is set as an Environment Vairiable
    dynamodb_table = (os.environ['table_name'])  
#Grab Input Params
    event_params = event['Details']['Parameters']
    callSequence = [] #set to null
#default for contained id True unless declared other wise    
    contained = True
    
    if 'contained' in event['Details']['Parameters']:
        contained = False
    
#Checks to see if the contactID is already in Dynamo    
    try:
        response = dynamodb.get_item(
                TableName=dynamodb_table,
                Key={
                    'ContactID' : {'S': event['Details']['ContactData']['ContactId']}
                }
            )
               
    except Exception as e:
        return {'message': str(e)}
    else:
        if 'Item' in response:
            callSequence = response['Item']['callSequence']['S'].split(';')
        
    #Add to callSequence.
    callerSequence = ''
    if 'callerSelection' in event_params:
        callerSelection = event_params['callerSelection']
    else:
        callerSelection = event_params['callerSelection']
    callSequence.append(callerSelection)
    
    #Update callSequence in DynamoDB
    str_call_audit = ';'.join(callSequence)
    try:
        response = dynamodb.put_item(
                TableName=dynamodb_table,
                Item={
                    'ContactID': {'S': event['Details']['ContactData']['ContactId']},
                    'callSequence': {'S': str_call_audit},
                    'contained': {'BOOL': contained}
                }
            )
    except Exception as e:
        return {'message': str(e)}
        
#Return values        
        
    return  {
                'callSequence': str_call_audit,
                'contained': contained
            }