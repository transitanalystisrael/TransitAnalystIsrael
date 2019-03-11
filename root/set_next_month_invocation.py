import boto3
import process_date
from datetime import datetime as dt
import datetime
import utils
import time


def set_next_invocation_date(main_script_name):

    # Update the GTFS-Monthly-Timer rule with the next date
    next_month_operation_date = process_date.get_auto_date_nextmonth() # The date that the product should already be working
    next_month_operation_date = dt.strptime(next_month_operation_date, '%Y%m%d')
    next_mont_invocatio_date = next_month_operation_date - datetime.timedelta(days=1) # The date that the product starts update

    # AWS Machine
    if utils.is_aws_machine():
        # Get the ColudWatch Events clients
        client = boto3.client('events',region_name='eu-central-1')

        # Set to run in the next day only once at 22:30
        scheduleExpression = next_mont_invocatio_date.strftime("cron(30 22 %d %m ? %Y)") #cron(30 12 11 03 ? 2019)
        response = client.put_rule(
            Name="GTFS-Monthly-Timer",
            ScheduleExpression=scheduleExpression,
            State='ENABLED'
        )

    # # Local Windows machine
    # else:
    #     from win32com import taskscheduler
    #     import win32com.client.pythoncom as pythoncom
    #     import win32api
    #     """creates a daily task"""
    #     name = "Transit Analyst Monthly Update"
    #     cmd = "python3 " + main_script_name
    #     cmd = cmd.split()
    #     ts = pythoncom.CoCreateInstance(taskscheduler.CLSID_CTaskScheduler,None,pythoncom.CLSCTX_INPROC_SERVER,taskscheduler.IID_ITaskScheduler)
    #
    #     task = ts.NewWorkItem(name)
    #     task.SetApplicationName(cmd[0])
    #     task.SetParameters(' '.join(cmd[1:]))
    #     task.SetPriority(taskscheduler.REALTIME_PRIORITY_CLASS)
    #     task.SetFlags(taskscheduler.TASK_FLAG_RUN_ONLY_IF_LOGGED_ON)
    #     task.SetAccountInformation('', None)
    #     ts.AddWorkItem(name, task)
    #     tr_ind, tr = task.CreateTrigger()
    #     tt = tr.GetTrigger()
    #     tt.Flags = 0
    #     tt.BeginYear = int(next_mont_invocatio_date.strftime('%Y'))
    #     tt.BeginMonth = int(next_mont_invocatio_date.strftime('%m'))
    #     tt.BeginDay = int(next_mont_invocatio_date.strftime('%d'))
    #     tt.StartMinute = 00
    #     tt.StartHour = 22
    #     tt.TriggerType = int(taskscheduler.TASK_TIME_TRIGGER_ONCE)
    #     tr.SetTrigger(tt)
    #     pf = task.QueryInterface(pythoncom.IID_IPersistFile)
    #     pf.Save(None,1)
    #     task.Run()
    #
    #     task = ts.Activate(name)
    #     exit_code, startup_error_code = task.GetExitCode()
    #     return win32api.FormatMessage(startup_error_code)
