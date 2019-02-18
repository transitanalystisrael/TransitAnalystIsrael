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
import utils
import data_utils
import boto3

def trigger_monthly_update():
    """

    :return: Whether the main manager should exit after the execution of this method
    """
    trigger_update = input("Are you sure you want to execute a monthly update? This will change the current "
                           "and past version which are on AWS production? [Y/N]\n")
    if trigger_update != "Y":
        return
    if not utils.is_aws_machine():
        print("You are trying to run a monthly update on a non AWS EC2 machine. Please use a different task")
        return False
    navitia_monthly_update_routine.main()
    return True


def prepare_od_machine_on_aws():
    # should_start = input("Going to prepare an On-demand machine on a new AWS EC2, would you like to start it once "
    #                      "finished? [Y/N]")
    gtfs_dates_and_urls = data_utils.get_gtfs_list_from_omd()
    dates_for_print= []
    for idx, version_entry in enumerate(gtfs_dates_and_urls ):
        dates_for_print.append(str(idx+1) + ". " + version_entry['date'].strftime('%d/%m/%Y'))
    print(*dates_for_print, sep="\n")
    first_version_number = int(input("Please select 2 versions of GTFS data to compile - enter the code of the first "
                               "version\n"))
    second_version_number = int(
        input("Enter the code of the secondversion\n"))

    _log.info("Going to prepare On-Demand machine on EC2 with GTFS with \"current\" service start date of: %s "
              "and \"past\" service start date of: %s",
              gtfs_dates_and_urls[first_version_number-1]['date'].strftime('%d/%m/%Y'),
              gtfs_dates_and_urls[second_version_number - 1]['date'].strftime('%d/%m/%Y'))

    current_gtfs_file_name  = data_utils.get_gtfs_from_omd(gtfs_dates_and_urls[first_version_number-1]['url'],
                                 gtfs_dates_and_urls[first_version_number-1]['date'].strftime('%d%m%Y'))

    past_gtfs_file_name = data_utils.get_gtfs_from_omd(gtfs_dates_and_urls[second_version_number - 1]['url'],
                                                          gtfs_dates_and_urls[second_version_number - 1][
                                                              'date'].strftime('%d%m%Y'))

    utils.setup_ec2_from_ami()


def start_an_existing():
    pass

def stop_and_terminate_od():
    pass

def remove_buckets():
    pass

def prepare_od_machine_on_windows():
    print("Going to prepare an On-demand instance for local Windows machine")


def main():
    """
    UI fo the manager
    """
    task_number = ""
    selected = False
    should_exit = False
    while task_number != 'exit' and not should_exit:
        if not selected:
            print("Welcome to Transit Analyst Israel update manager - please type a number to select an operation")
            print(
                "1) Trigger a manual monthly update on PRODUCTION (Moves current version to be previous and enters new "
                "data to current)\n"
                "2) Prepare an OD (On-Demand) to be deployed on AWS EC2 with 2 user-selected service dates (and option to "
                "start it)\n"
                "3) Prepare an OD to be deployed on Windows with 2 user-selected service dates\n"
                "4) Start an existing OD with/without Navitia time-map (thin option)\n"
                "5) Stop & terminate existing OD hosted on AWE\n"
                "6) Remove user-selected S3 buckets\n\n"
            )
        task_number = input("Please select a task [1-6] or type \"exit\'\n")        
        if task_number == "1":
            should_exit = trigger_monthly_update()
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
        selected = True



if __name__== "__main__":
    # main()
    _log = utils.get_logger()
    prepare_od_machine_on_aws()
