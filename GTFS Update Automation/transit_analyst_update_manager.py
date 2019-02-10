"""
This module is a command-line interface to initiate different update options for Transit Analyst Israel
There are 5 different options:
1. Trigger a manual monthly update on PRODUCTION (Moves current version to be previous and enters new data to current)
2. Prepare an OD (On-Demand) to be deployed on AWS EC2 with 2 user-selected service dates (and option to start it)
3. Prepare an OD to be deployed on Windows with 2 user-selected service dates
4. Start and existing OD with/without Navitia time-map (thin option)
5. Stop & terminate existing OD hosted on AWE
6. Remove user-selected S3 buckets
"""

import navitia_monthly_update_routine


def trigger_monthly_update():
    trigger_update = input("Are you sure you want to execute a monthly update? This will change the current "
                           "and past version which are on AWS production? [Y/N]\n")
    if trigger_update != "Y":
        return
    navitia_monthly_update_routine.main()



def prepare_od_machine_on_aws():
    should_start = input("Going to prepare an On-demand machine for AWS, would you like to start it once "
                         "finished? [Y/N]")
    pass

def start_an_existing():


def stop_and_terminate_od():


def remove_buckets():


def prepare_od_machine_on_windows():
    print("Going to prepare an On-demand instance for local Windows machine")


def main():
    """
    UI fo the manager
    """
    task_number = ""
    while task_number != 'exit':
        print("Welcome to Transit Analyst Israel update manager - please type a number to select an operation")
        print(
            "1. Trigger a manual monthly update on PRODUCTION (Moves current version to be previous and enters new "
            "data to current)\n"
            "2. Prepare an OD (On-Demand) to be deployed on AWS EC2 with 2 user-selected service dates (and option to "
            "start it)\n"
            "3. Prepare an OD to be deployed on Windows with 2 user-selected service dates\n"
            "4. Start an existing OD with/without Navitia time-map (thin option)\n"
            "5. Stop & terminate existing OD hosted on AWE\n"
            "6. Remove user-selected S3 buckets\n\n"
        )
        task_number = input("Please select a task [1-6] or type \"exit\'\n")
        if task_number == "1":
            trigger_monthly_update()
            break
        if task_number == "2":
            prepare_od_machine_on_aws()
            break
        if task_number == "3":
            prepare_od_machine_on_windows()
            break
        if task_number == "4":
            start_an_existing()
            break
        if task_number == "5":
            stop_and_terminate_od()
            break
        if task_number == "6":
            remove_buckets()
            break



if __name__== "__main__":
    main()

