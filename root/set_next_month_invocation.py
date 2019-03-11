import boto3

client = boto3.client('events',region_name='eu-central-1')
response = client.put_rule(
    Name="test",
    # ScheduleExpression='string',
    EventPattern="{ \"source\": [\"aws.ec2\"] }" ,
    # State='ENABLED'|'DISABLED',
    # Description='string',
    # RoleArn='string'
)