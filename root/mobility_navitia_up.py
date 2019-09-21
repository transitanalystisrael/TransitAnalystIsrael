#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
"""
This script ...
"""

import mobility_TTM_utils_min as utils
import datetime
import os
from pathlib import Path
from logger import _log

def main(gtfsdate) :
    # config variables to be moved to config-file downstrem
    coverage_name, navitia_docker_compose_file_path, navitia_docker_compose_file_name = utils.get_config_params(gtfsdate)

    try:
        # Stop docker containers running 
        docker_client = utils.get_docker_service_client()
        containers = docker_client.containers.list()
        
        if len(containers) > 0:
            print(containers)
            utils.stop_all_containers(utils.get_docker_service_client())

        # Get the docker service client
        docker_client = utils.get_docker_service_client()

        containers = docker_client.containers.list(filters={"name": "worker"})
        if len(containers) == 0:
            _log.info("Navitia docker containers are down, bringing them up with on_demand coverage ")
            utils.start_navitia_with_single_coverage(navitia_docker_compose_file_path, navitia_docker_compose_file_name,
                                                     coverage_name)
            containers = docker_client.containers.list(filters={"name": "worker"})
            
        print(containers)

    except Exception as e:
        raise Exception
