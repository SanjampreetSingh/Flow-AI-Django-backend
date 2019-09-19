import boto3
from flow import settings

# Boto3 Connection Variable
client = boto3.client(
    'apigateway',
    region_name='us-east-2',
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
)


def boto_create_api_key(name: str, enabled: bool, generateDistinctId: bool, customerId: str):
    return client.create_api_key(
        name=str(name),
        enabled=enabled,
        generateDistinctId=generateDistinctId,
        customerId=str(customerId)
    )


def boto_create_usage_plan(name: str):
    return client.create_usage_plan(
        name=str(name),
        throttle={
            'burstLimit': 10,
            'rateLimit': 10
        },
        quota={
            'limit': 100,
            'period': 'MONTH'
        },
    )


def boto_create_usage_plan_key(usagePlanId, keyId, keyType: str):
    return client.create_usage_plan_key(
        usagePlanId=usagePlanId,
        keyId=keyId,
        keyType=str(keyType)
    )


def boto_update_usage_plan(usagePlanId, patchOperationsOp: str, patchOperationsPath: str, patchOperationsValue):
    return client.update_usage_plan(
        usagePlanId=usagePlanId,
        patchOperations=[
            {
                "op": str(patchOperationsOp),
                "path": str(patchOperationsPath),
                "value": patchOperationsValue
            },
        ]
    )
