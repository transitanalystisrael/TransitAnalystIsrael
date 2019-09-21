import docker
import json
import os
import requests
import subprocess
import time
import re
from io import BytesIO
from logger import _log
from pathlib import Path
from datetime import datetime as dt
import glob
import mobility_spectrum_cfg as cfg

def get_config_params(gtfsdate):
    """
    Reads config file and returns the configuration parameters
    :return: configuration parameters
    """
    # Get parameters
    navitia_docker_compose_file_path = Path(os.getcwd()).parent.parent / "navitia-docker-compose" / "compose_files"
    if cfg.get_service_date == "on_demand":
        navitia_docker_compose_file_name = "navitia-docker-ondemand-" + gtfsdate + ".yml"
        coverage_name = "ondemand-" + gtfsdate
    return coverage_name, navitia_docker_compose_file_path, navitia_docker_compose_file_name

def get_docker_service_client():
    """
    Checks that the docker daemon service is running and returns the service client
    :return: the docker service client
    """
    # Check that the docker daemon service is up, and timeout after five minutes
    docker_check_alive_cmd = "docker info"
    docker_is_up = False
    timeout = time.time() + 60 * 5
    try:
        while not docker_is_up:
            if time.time() > timeout:
                raise TimeoutError
            # Check that the daemon is up and running
            docker_check_alive_process = subprocess.Popen(docker_check_alive_cmd, stdout=subprocess.PIPE, shell=True)
            output, error = docker_check_alive_process.communicate()
            docker_is_up = "Containers" in output.decode('utf-8')

        # Get the docker client
        client = docker.from_env()
        return client
    except BaseException as error:
        _log.error("Docker daemon service is not up")
        raise error


def get_navitia_url_for_cov_status(cov_name):
    """
    Get the url of Navitia coverage status page
    :param cov_name: the name of the coverage to return, e.g. "default" or "secondary-cov"
    :return: url of Navitia coverage status page
    """
    return "http://localhost:9191/v1/coverage/" + cov_name #+ "/status/"


def check_coverage_running(url, coverage_name):
    """
    Check if Navitia coverage is up and running
    :param url: Navitia server coverage url
    :param coverage_name: the name of the coverage to check
    :return: Whether a Navitia coverage is up and running
    """
    _log.info("checking if %s is up", coverage_name)
    response = requests.get(url)

    # Get the status of the coverage as Json
    json_data = json.loads(response.text)
    if "regions" not in json_data or "running" not in json_data["regions"][0]['status']:
        _log.info("%s coverage is down", coverage_name)
        return False
    else:
        _log.info("%s coverage is up", coverage_name)
    return True

def start_navitia_with_single_coverage(navitia_docker_compose_file_path, navitia_docker_compose_file_name,
                                       coverage_name, extend_wait_time=False):
    """
    Start Navitia server with only default coverage (using docker-compose)
    :param navitia_docker_compose_file_path: path where docker-compose file exists
    :param extend_wait_time: whether an extended time of wait should be applied. Should be set to True when Navitia
    docker compose is started up the first time (images are being downloaded from the web)
    :return: Whether Navitia was started successfully with default coverage
    """

    _log.info("Attempting to start Navitia with %s coverage", coverage_name)

    # run the docker- compose and redirect logs to prevent from printing in the output
    navitia_docker_start_command = "docker-compose -f" + navitia_docker_compose_file_name + " -p navitia-docker-compose up --remove-orphans"

    subprocess.Popen(navitia_docker_start_command, shell=True, cwd=navitia_docker_compose_file_path, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

    # Longer wait time is required because images are being re-downloaded
    if extend_wait_time:
        t_wait = 60 * 6
    else:
        t_wait = 60 * 4
    _log.info("Waiting %s seconds to validate Navitia docker is up and running", t_wait)
    time.sleep(t_wait)

    # Check if coverage is up and running
    is_default_up = check_coverage_running(get_navitia_url_for_cov_status(coverage_name), coverage_name)
    if not is_default_up:
        return False
    return True

def is_cov_exists(container, coverage_name):
    _log.info("Checking if %s exists in /srv/ed/output of %s", coverage_name, container.name)
    file_list_command = "/bin/sh -c \"ls\""
    exit_code, output = container.exec_run(cmd=file_list_command, stdout=True, workdir="/srv/ed/output/")
    exists = coverage_name in str(output)
    if exists:
        _log.info("%s exists in /srv/ed/output of %s", coverage_name, container.name)
    else:
        _log.info("%s doesn't exists in /srv/ed/output of %s", coverage_name, container.name)
    return exists

def stop_all_containers(docker_client):
    """
    Stop all the running docker containers
    :param docker_client: docker client
    """
    _log.info("Going to stop all Docker containers")
    for container in docker_client.containers.list():
        container.stop()
    _log.info("Stopped all Docker containers")

