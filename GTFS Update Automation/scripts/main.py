# Script to update Navitia Coverage with latest GTFS data:
# 1. Download GTFS & OSM
# 2. bring up custom coverage
# 3. copy OSM & GTFS to the default coverage,
# 4. move default graph to the new coverage,
# 5. store the previous custom graph on your host
# 6. Restart the docker
# At the end: The default coverage shows the new GTFS & OSM and the previous default is now secondary_custom_coverage_name

from scripts import utils
import py_compile
from scripts import gtfs2transfers

if __name__== "__main__":
    # Global varaibles that might be needed to be in config. file
    # gtfs_url = "gtfs.mot.gov.il"
    # gtfs_file_name_on_server = "zones.zip"
    # # gtfs_file_name_on_server = "israel-public-transportation.zip"
    # osm_url = "https://download.geofabrik.de/asia/israel-and-palestine-latest.osm.pbf"
    # secondary_custom_coverage_name = "secondary-cov"
    # default_coverage_name = "default"
    # transfers_script_path = "C:/Dev/Nativia/navitia-transfers/"
    # transfers_script_name = "gtfs2transfers.py"
    #
    # navitia_docker_compose_file_path = "C:/Dev/Nativia/navitia-docker-compose/"
    # navitia_docker_compose_file_name = "docker-israel-custom-instances.yml"
    #
    # # Download GTFS
    # # gtfs_file = get_file_from_url_ftp(gtfs_url, gtfs_file_name_on_server)
    # gtfs_file_path = "C:/Dev/TransitAnalystIsrael/GTFS Update Automation/"  # FOR TESTING
    # gtfs_file_name = "GTFS2018-07-01.zip" # FOR TESTING
    # # Download OSM
    # osm_file_path = "C:/Dev/TransitAnalystIsrael/GTFS Update Automation/" # FOR TESTING
    # osm_file_name = "israel-and-palestine-latest.osm.pbf" # FOR TESTING
    # # osm_file = get_file_from_url_http(osm_url)
    #
    # # Generate the Transfers file required for Navitia and add to GTFS
    # # gtfs_and_transfers_file = generate_gtfs_with_transfers(gtfs_file, transfers_script_path, transfers_script_name)
    #
    #
    #
    # # Start up docker service and copy files into secondary_custom_coverage_name for processing
    # # get the docker service client
    # docker_client = utils.get_docker_service_client()
    # # start Navitia with custom docker-compose that include secondary_custom_coverage_name
    # utils.start_navitia_w_custom_cov(secondary_custom_coverage_name, navitia_docker_compose_file_path,
    #                                  navitia_docker_compose_file_name, False)
    # worker_con = docker_client.containers.list(filters={"name": "worker"})[0]

    # Copy OSM & GTFS files to default cov in order to generate a new graph
    # copy_osm_and_gtfs_to_default_cov(worker_con, osm_file_path, osm_file_name, gtfs_file_path, gtfs_file_name)

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

    py_compile.compile('gtfs2transfers.py', "","",True)
    print("Done")



