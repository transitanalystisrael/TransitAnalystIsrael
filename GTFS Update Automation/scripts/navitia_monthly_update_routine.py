"""
Script to update Navitia Coverage with latest GTFS data once a month:
prequisits:
a. remote host on ec2-instace with git, docker, docker-compose, python 3
b. navitia docker is running with 2 coverages: deafult and secondary-cov
c. This script depends on: utils.py and  gtfs2transfers.py
Running this script will:
0. Get the current end of production dates of each coverage for later comparison
1. Copy the existing secondary-cov.nav.lz4 to the host machine for backup and delete it from container
2. Download GTFS & OSM
3. Generate the transfers table )takes 40 minutes) and add it to the GTFS Zipped file
4. Rename default.lz4 to secondary-cov.nav.lz4 (by that converting it to last month gtfs)
5. Re-start Navitia docker to apply the change for secondary-cov
6. copy OSM & GTFS to the default coverage input folder on the worker container
7. After 15 minutes - test that both osm and gtfs conversions are done
8. Re-start Navitia to make sure all changes are applies
8. If it's up - delete the old gtfs and osm files
At the end: The default coverage shows the new GTFS & OSM and the previous default is now secondary_custom_coverage_name


"""
from scripts import utils
import os
import datetime


if __name__== "__main__":
    #get logger
    update_time = datetime.datetime.now().strftime("m%Y_%H%M")
    _log = utils.get_logger()

    try:
        #config variables to be moved to config-file downstrem
        default_coverage_name = "default"
        secondary_custom_coverage_name = "secondary-cov"
        gtfs_url = "gtfs.mot.gov.il"
        gtfs_file_name_on_mot_server = "israel-public-transportation.zip"
        osm_url = "https://download.geofabrik.de/asia/israel-and-palestine-latest.osm.pbf"

        navitia_docker_compose_file_path = "/home/ec2-user/navitia_server/navitia-docker-compose/"
        navitia_docker_compose_file_name = "docker-israel-custom-instances.yml"

        # Get the docker service client
        docker_client = utils.get_docker_service_client()
        # Get the worker container
        worker_con = docker_client.containers.list(filters={"name": "worker"})[0]

        # Get the current end of production dates of default coverage for post-processing comparison
        default_cov_eop_date = utils.get_covereage_end_production_date(default_coverage_name)
        # Copy the existing secondary-cov.nav.lz4 to the host machine for backup and delete it from container
        # utils.copy_graph_to_local_host(worker_con, secondary_custom_coverage_name)
        # utils.delete_grpah_from_container(worker_con, secondary_custom_coverage_name)

        # Download GTFS & OSM
        # gtfs_file_name = utils.get_file_from_url_ftp(gtfs_url, gtfs_file_name_on_mot_server)
        # osm_file_name = utils.get_file_from_url_http(osm_url)

        # Generate the Transfers file required for Navitia and add to GTFS
        # gtfs_and_transfers_file = utils.generate_gtfs_with_transfers(gtfs_file)

        # Rename default.lz4 to secondary-cov.nav.lz4 (by that converting it to last month gtfs)
        # utils.move_one_graph_to_secondary(worker_con, default_coverage_name, secondary_custom_coverage_name)

        # Re-start Navitia docker to apply the change for secondary-cov
        # utils.stop_all_containers(docker_client)
        # utils.start_navitia_w_custom_cov(secondary_custom_coverage_name, navitia_docker_compose_file_path,
        #                                  navitia_docker_compose_file_name)
        # Get the new worker container
        # worker_con = docker_client.containers.list(filters={"name": "worker"})[0]

        # Clearing the worker log to make sure we're monitoring updated logs
        # utils.clear_container_logs(worker_con)
        # Copy OSM & GTFS to the default coverage input folder on the worker container
        # utils.copy_osm_and_gtfs_to_default_cov(worker_con, os.getcwd(), osm_file_name, os.getcwd(), gtfs_file_name)

        # Validate the conversion process takes place by ensuring tyr_beat is up
        # utils.validate_osm_gtfs_convertion_to_graph_is_running(docker_client, secondary_custom_coverage_name,
        #                                             navitia_docker_compose_file_path, navitia_docker_compose_file_name)

        # After 15 minutes - test that both osm and gtfs conversions are done
        # success = utils.validate_osm_gtfs_convertion_to_graph_is_completed(worker_con, 15)

        # If it didn't succeed, give it 5 more minutes
        # if not success:
            # success = utils.validate_osm_gtfs_convertion_to_graph_is_completed(worker_con, 5)

        # If after total of 20 minutes, it didn't succeed, restart Navitia and wait 15 minutes more
        # utils.stop_all_containers(docker_client)
        # utils.start_navitia_w_custom_cov(secondary_custom_coverage_name, navitia_docker_compose_file_path,
        #                                  navitia_docker_compose_file_name)
        # success = utils.validate_osm_gtfs_convertion_to_graph_is_completed(worker_con, 15)

        # Re-start Navitia to make sure all changes are applies
        # utils.stop_all_containers(docker_client)
        # is_up = utils.start_navitia_w_custom_cov(secondary_custom_coverage_name, navitia_docker_compose_file_path, navitia_docker_compose_file_name)

        # If it's up - delete the old gtfs and osm files
        # if is_up:
        #     utils.delete_file_from_host(osm_file_name)
        #     utils.delete_file_from_host(gtfs_file_name)

        # Validate new data is accessible via default and the old data is accessible via secondary
        default_cov_eop_date="20180629"
        utils.validate_graph_changes_applied(default_coverage_name, secondary_custom_coverage_name, default_cov_eop_date)


        # Send e-mail everything is completed
        # utils.send_log_to_email("Transit Analyst Monthly Update " + update_time, "Update Completed")

        _log.info("Done without errors")

    except Exception as e:
        _log.info("Done with errors")
        # utils.send_log_to_email("Transit Analyst Monthly Update " + update_time, "Update Failed - see logs")




