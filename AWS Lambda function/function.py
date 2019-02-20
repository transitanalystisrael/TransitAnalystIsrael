import boto3
import paramiko
def worker_handler(event, context):
    """
    This function connects to the Transit Analyst EC2 peridocally
    and runs the navitia_monthly_update_routine
    """

    # Prepare ssh object to conenct to the EC2
    k = paramiko.RSAKey.from_private_key_file("<key-file>")
    c = paramiko.SSHClient()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    host='<EC2 private IP (not public one)>'
    print("Connecting to " + host)
    c.connect( hostname = host, username = "ec2-user", pkey = k )
    print ("Connected to " + host)

    # Change directory to scripts and run update without waiting for it to end - see logs on EC2 under ~/scripts/logs
    commands = [
        "cd /home/ec2-user/scripts",
        "nohup python3 navitia_monthly_update_routine.py"

        ]
    for command in commands:
        print ("Executing {}".format(command))
        c.exec_command(command, timeout=5)

    return {
        'message' : "Monthly update was initiated. See Cloudwatch logs for complete output of Labmda execution and"
                    "the EC2 ~/scripts/logs for the monthly update execution logs"
    }