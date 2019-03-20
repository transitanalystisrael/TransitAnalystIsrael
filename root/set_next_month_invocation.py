import boto3
import process_date
from datetime import datetime as dt
import utils
import datetime

from pathlib import Path
import sys

def set_next_invocation_date(main_script_name):
    # Update the GTFS-Monthly-Timer rule with the next date
    next_month_operation_date = process_date.get_auto_date_nextmonth() # The date that the product should already be working
    next_month_operation_date = dt.strptime(next_month_operation_date, '%Y%m%d')
    next_mont_invocation_date = next_month_operation_date - datetime.timedelta(days=1) # The date that the product starts update

    
    # AWS Machine
    if utils.is_aws_machine():
        # Get the ColudWatch Events clients
        client = boto3.client('events',region_name='eu-central-1')

        # Set to run in the next day only once at 22:30
        scheduleExpression = next_mont_invocation_date.strftime("cron(30 22 %d %m ? %Y)") #cron(30 12 11 03 ? 2019)
        response = client.put_rule(
            Name="GTFS-Monthly-Timer",
            ScheduleExpression=scheduleExpression,
            State='ENABLED'
        )
    else:
        import win32com.client
        scheduler = win32com.client.Dispatch('Schedule.Service')
        scheduler.Connect()
        root_folder = scheduler.GetFolder('\\')
        task_def = scheduler.NewTask(0)

        # Create trigger
        start_time = next_mont_invocation_date + datetime.timedelta(hours=22)

        TASK_TRIGGER_TIME = 1
        trigger = task_def.Triggers.Create(TASK_TRIGGER_TIME)
        trigger.StartBoundary = start_time.isoformat()

        # Create action
        TASK_ACTION_EXEC = 0
        action = task_def.Actions.Create(TASK_ACTION_EXEC)
        action.ID = 'TransitAnalystIsraelUpdater'
        action.WorkingDirectory = Path.cwd().as_posix()
        action.Path = sys.executable
        action.Arguments = main_script_name

        # Set parameters
        task_def.RegistrationInfo.Description = 'Transit Analyst Israel Updater'
        task_def.Settings.Enabled = True
        task_def.Settings.StopIfGoingOnBatteries = False
        task_def.Settings.WakeToRun = True
        task_def.Settings.StartWhenAvailable = False

        # Register task
        # If task already exists, it will be updated
        TASK_CREATE_OR_UPDATE = 6
        TASK_LOGON_NONE = 0
        root_folder.RegisterTaskDefinition(
            'Transit Analyst Israel Updater',  # Task name
            task_def,
            TASK_CREATE_OR_UPDATE,
            '',  # No user
            '',  # No password
            TASK_LOGON_NONE)
