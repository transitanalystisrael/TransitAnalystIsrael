"""
Script to update Navitia Coverage with latest GTFS data once a month:
prequisits:
a. remote host on ec2-instace with git, docker, docker-compose, python 3
b. navitia docker is running with 2 coverages: deafult and secondary-cov
c. This script depends on: utils.py and  gtfs2transfers.py
Running this script will:
1. Copy the existing secondary-cov.nav.lz4 to the host machine for backup and delete it from container
2. Download GTFS & OSM
3. Generate the transfers table )takes 40 minutes) and add it to the GTFS Zipped file
4. Rename default.lz4 to secondary-cov.nav.lz4 (by that converting it to last month gtfs)
5. Re-start Navitia docker to apply the change for secondary-cov
6. copy OSM & GTFS to the default coverage input fodler on the worker container
7. After 60 minutes - test that both coverages work
At the end: The default coverage shows the new GTFS & OSM and the previous default is now secondary_custom_coverage_name


"""
from scripts import utils

if __name__== "__main__":

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
    # worker_con = docker_client.containers.list(filters={"name": "worker"})[0]

    # Copy the existing secondary-cov.nav.lz4 to the host machine for backup and delete it from container
    # utils.copy_graph_to_local_host(worker_con, secondary_custom_coverage_name)
    # utils.delete_grpah_from_container(worker_con, secondary_custom_coverage_name)

    # Download GTFS & OSM
    # gtfs_file = utils.get_file_from_url_ftp(gtfs_url, gtfs_file_name_on_mot_server)
    # osm_file = utils.get_file_from_url_http(osm_url)

    # Generate the Transfers file required for Navitia and add to GTFS
    # gtfs_and_transfers_file = utils.generate_gtfs_with_transfers(gtfs_file)

    # Rename default.lz4 to secondary-cov.nav.lz4 (by that converting it to last month gtfs)
    # utils.move_one_graph_to_secondary(worker_con, default_coverage_name, secondary_custom_coverage_name)

    # Re-start Navitia docker to apply the change for secondary-cov
    # utils.stop_all_containers(docker_client)
    utils.start_navitia_w_custom_cov(secondary_custom_coverage_name, navitia_docker_compose_file_path,
                                     navitia_docker_compose_file_name)
    # Get the new worker container
    worker_con = docker_client.containers.list(filters={"name": "worker"})[0]
    '''
    6. copy OSM & GTFS to the default coverage input fodler on the worker container
    7. After 60 minutes - test that both coverages work
    '''

    ###OLD CODEEEE!!!!

    # Monitor processing of GTFS & OSM (might require restarting / downloading tyr_beat) on default coverage
    # validate_osm_gtfs_convertion_to_graph(docker_client, secondary_custom_coverage_name,
    #                                       navitia_docker_compose_file_path, navitia_docker_compose_file_name)
    # Move the default coverage graph to the secondary coverage
    # try:
    # move_one_graph_to_secondary(worker_con, default_coverage_name, secondary_custom_coverage_name)
    # catch error:
    #   print(error)
    #   exit

    # stop all docker containers and restart to process renamed graphs
    # stop_all_containers(docker_client)
    # start_navitia_w_custom_cov(secondary_custom_coverage_name, navitia_docker_compose_file_path, navitia_docker_compose_file_name, True)

    # Copy the old secondary custom graph to your host and delete it from the container
    # copy_graph_to_local_host(worker_con, old_secondary_custom_coverage_name)
    # delete_grpah_from_container(worker_con, old_secondary_custom_coverage_name)

    #####NEED TO IMPLEMENT COPY BETWEEN E2C
    # copy_graph_from_remote_host_to_container(worker_con, old_secondary_custom_coverage_name)


    # Copy the OSM & GTFS to default coverage
    # Re-start the service so the graph name changes will be updated and OSM & GTFS run

    # Verify the covereges reflect new data within 2 hours, otherwise send an email with alert

    print("Done")



