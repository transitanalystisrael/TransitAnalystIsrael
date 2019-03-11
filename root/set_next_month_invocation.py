import boto3
import process_date
from datetime import datetime as dt
import datetime
# Get the ColudWatch Events clients
client = boto3.client('events',region_name='eu-central-1')

# Update the GTFS-Monthly-Timer rule with the next date

next_month_operation_date = process_date.get_auto_date_nextmonth() # The date that the product should already be working
next_month_operation_date = dt.strptime(next_month_operation_date, '%Y%m%d')
next_mont_invocatio_date = next_month_operation_date - datetime.timedelta(days=1) # The date that the product starts update
# Set to run in the next day only once at 22:30
scheduleExpression = next_mont_invocatio_date.strftime("cron(30 22 %m %d ? %Y)") #cron(30 12 11 03 ? 2019)
response = client.put_rule(
    Name="GTFS-Monthly-Timer",
    ScheduleExpression=scheduleExpression,
    State='ENABLED'
)