# AmazonConnectCallerContainment
This document describes the process to use AWS Lambda and Amazon DynamoDB to track customer progress and call containment.

Directions:

Before creating the stack with the cloudformation template, CF_CallContainment.yaml, perform the following steps:
1. Update line 25 of CF_CallContainment.yaml to reflect your bucket name
2. Upload CallContainmentCode.zip into newly created bucket


After CF_CallContainment.yaml is executed
1. Add the AmazonConnectCallContainment lambda function to connect
2. Import ContainmentTestFlow as a standard contact flow in connect.
3. Update the Lambda blocks in the contact flow and publish.
4. Assign DID to the ContainmentTestFlow

The rest application loops through a simple menu.  Options 1,2,3 are for various departments. Option 4 is to exit.  Option 0 will exit to agent and therefore me considered a call that was not contained.

A DynamopDB table will be created CallAuditTable.

Each call will generate and entry that can be used for reporting. Example Below.

{
  "callSequence": "SalesOption;SupportOption;BillingOption;Representative",
  "ContactID": "f6cc2ec7-b5db-49ae-a3cc-2237e35b9ca4",
  "contained": false
}

callSequence can also be used as an attribute for the CTR.
