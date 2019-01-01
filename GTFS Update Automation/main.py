# Script to update Navitia Coverage with latest GTFS data:
# 1. Download GTFS & OSM
# 2. bring up custom coverage
# 3. copy OSM & GTFS to the default coverage,
# 4. move default graph to the new coverage,
# 5. store the previous custom graph on your host
# 6. Restart the docker
# At the end: The default coverage shows the new GTFS & OSM and the previous default is now secondary_custom_coverage_name

import sys, os
import platform
import requests
import ftplib
import docker
import subprocess
import json
import time
from dateutil import parser
import progressbar


DEVNULL = open('/dev/null', 'w')

def get_file_from_url_http(url):
    r = requests.get(url, stream=True)
    local_file_name = "israel-and-palestine-latest.osm.pbf"
    file = open(local_file_name, 'wb')
    size = int(r.headers['Content-Length'])
    pbar = createProgressBar(size)
    # Download
    size_iterator = 0
    for chunk in r.iter_content():
        file_write(chunk, file, pbar, size_iterator )
        size_iterator += 1
    file.close()
    pbar.finish()
    print("Finished loading latest OSM to: ", local_file_name)

def createProgressBar(file_size):
    widgets = ['Downloading: ', progressbar.Percentage(), ' ',
               progressbar.Bar(marker='#', left='[', right=']'),
               ' ', progressbar.ETA(), ' ', progressbar.FileTransferSpeed()]
    pbar = progressbar.ProgressBar(widgets=widgets, maxval=file_size)
    pbar.start()
    return pbar

def file_write(data, dest_file, pbar, size_iterator):
    """
    Call back for writing the downlaoed data from FTP while updating the progress bar
    """
    dest_file.write(data)
    pbar.update(size_iterator)

def get_file_from_url_ftp(url, file_name_on_server):

    try:
        # Connect to FTP
        ftp = ftplib.FTP(url)
        ftp.login()

        # Get the GTFS time stamp and generate local file name, "GTFS-Dec-18"
        file_lines = []
        local_file_name = ""
        size = 0

        ftp.dir("", file_lines.append)
        for line in file_lines:
            tokens = line.split(maxsplit=4)
            # print(tokens)
            name = tokens[3]
            if name == file_name_on_server:
                time_str = tokens[0]
                time = parser.parse(time_str)
                local_file_name = str(time.strftime('%b') + "-" + time.strftime('%y'))
                size = float(tokens[2])

        # Generate a progress bar and download
        local_file = open(local_file_name, 'wb')
        pbar = createProgressBar(size)
        # Download
        ftp.retrbinary("RETR " + file_name_on_server, lambda data: file_write(data, local_file, pbar, len(data)))

        # Finish
        local_file.close()
        ftp.quit()
        pbar.finish()
        sys.stdout.flush()

        print("Finished loading latest GTFS to: ", local_file_name)

    except ftplib.all_errors as err:
        error_code = err.args[0]
        if error_code == 2:
            print(file_name_on_server, "is not found on", url)
            ftp.quit()
        if error_code == 11001:
            print("URL", url, "is not valid ")


def start_navitia_with_default_and_custom_coverage():
    pass

def copy_file_into_docker():
    pass


def copy_file_from_docker():
    pass


def get_docker_service_client():
    if platform.uname()[0] == "Windows":
        # TRAILS FOR RUNNING THE SERVICE
        # docker_run_command = "C:/Program Files/Docker/Docker/Docker for Windows.exe"
        # subprocess.call(["C:\\WINDOWS\\system32\\WindowsPowerShell\\v1.0\\powershell.exe", ". \"./SamplePowershell\";", "&hello"])
        # subprocess.check_output('powershell Net start -ArgumentList  "com.docker.service" -Verb "runAs"',
        #                         shell=True)
        # print(subprocess.check_output(["runas", "/noprofile", "/user:Administrator", "|", "echo", "shaked"]))

        # docker_run_command = "start-service *docker*"

        # proc = subprocess.Popen([docker_run_command], shell=True, stdin=None, stdout=None, stderr=None, close_fds=True)
        # win32serviceutil.StartService(docker_run_command,None)
        docker_check_alive_cmd = "docker info"
        docker_is_up = False
        while not docker_is_up:
            docker_check_alive_process = subprocess.Popen(docker_check_alive_cmd, stdout=subprocess.PIPE)
            output, error = docker_check_alive_process.communicate()
            docker_is_up = "Containers" in output.decode('utf-8')
        try:
            client = docker.from_env()
            print("Docker Daemon service is up and running")
        except error:
            print("Docker deamon service is not up")
    return client

def get_navitia_url_for_cov(cov_name):
    return "http://localhost:9191/v1/coverage/" + cov_name + "/status/"


def check_covereage_running(url, coverage_name):
    response = requests.get(url)
    json_data = json.loads(response.text)
    if "status" not in json_data or "running" not in json_data["status"]["status"]:
        print(coverage_name + " coverage is down")
    else:
        print(coverage_name + " coverage is up")


def start_navitia_w_custom_cov(secondary_custom_coverage_name):
    navitia_docker_compose_file_path = "C:/Dev/Nativia/navitia-docker-compose/"
    navitia_docker_compose_file_name = "docker-israel-custom-instances.yml"
    navitia_docker_compose_file = open(navitia_docker_compose_file_path + navitia_docker_compose_file_name, mode='r')
    navitia_docker_compose_file_contents = navitia_docker_compose_file.read()
    navitia_docker_compose_file.close()

    if secondary_custom_coverage_name != "default" \
            and not secondary_custom_coverage_name in navitia_docker_compose_file_contents:
        print("The custom configuration does not include a coverage area named: " + secondary_custom_coverage_name +
              ". Fix config, restart docker and start again")

    # run the custom cmopose and redirect logs while nuting the output
    navitia_docker_start_command = "docker-compose -f docker-compose.yml -f  " + navitia_docker_compose_file_name + " up"

    #RETURN MEEEE TO START FOCKER
    subprocess.Popen(navitia_docker_start_command, cwd=navitia_docker_compose_file_path,  stderr=DEVNULL, stdout=DEVNULL)

    # wait 90 seconds for everything to go up
    time.sleep(90)

    # Check if default and secondary_custom_coverage_name regions are up and running
    check_covereage_running(get_navitia_url_for_cov(default_coverage_name), default_coverage_name)
    check_covereage_running(get_navitia_url_for_cov(secondary_custom_coverage_name), secondary_custom_coverage_name)


def move_one_graph_to_secondary(conatiner, source_cov_name, dest_cov_name):
    command_list = "/bin/sh -c \"mv " + source_cov_name + ".nav.lz4 "+ dest_cov_name + ".nav.lz4\""
    exit_code, output = container.exec_run(cmd=command_list,  stdout=True, workdir="/srv/ed/output/")
    if exit_code != 0:
        print("Couldn't change ", source_cov_name, " to ", dest_cov_name)
        raise Exception("STOP the program")


def copy_graph_to_local_host(container, coverage_name):
    # Create a local file for writing the incoming graph
    local_graph_file = open('./' + coverage_name + '.nav.lz4', 'wb')
    bits, stat = container.get_archive('/srv/ed/output/' + coverage_name + '.nav.lz4')
    for chunk in bits:
        local_graph_file.write(chunk)
    local_graph_file.close()
    print("Finished copying ", coverage_name, ".nav.lz4 to ", os.getcwd())


def copy_graph_from_remote_host_to_container(container, coverage_name):
    # Create a local file for writing the incoming graph
    print(coverage_name + '.nav.lz4')
    success = container.put_archive('/srv/ed/output/', coverage_name + '.nav.lz4')
    if success:
        print("Finished copying ", coverage_name, ".nav.lz4 to ", container.name)


def delete_grpah_from_container(container, coverage_name):
    delete_command= "/bin/sh -c \"rm " + coverage_name +".nav.lz4\""
    exit_code, output = container.exec_run(cmd=delete_command,  stdout=True, workdir="/srv/ed/output/")
    if exit_code != 0:
        print("Couldn't delete ", coverage_name, " graph")
        raise Exception("STOP the program")
    print("Delete graph", coverage_name, "from container ", container.name)


def stop_all_containers(docker_client):
    for container in docker_client.containers.list():
        container.stop()

if __name__== "__main__":
    # Global varaibles that might be needed to be in config. file
    gtfs_url = "gtfs.mot.gov.il"
    gtfs_file_name_on_server = "zones.zip"
    # gtfs_file_name_on_server = "israel-public-transportation.zip"
    osm_url = "https://s3.eu-central-1.amazonaws.com/israeltimemap/Time+Map/vendor.53be82b43926a4befafc.js.map"
    secondary_custom_coverage_name = "nov-18"
    old_secondary_custom_coverage_name = "jul-18"
    default_coverage_name = "default"


    # Download GTFS
    # gtfs_file = get_file_from_url_ftp(gtfs_url, gtfs_file_name_on_server)

    # Download OSM
    # osm_file = get_file_from_url_http(osm_url)

    # Start up docker service and copy files into secondary_custom_coverage_name for processing
    # get the docker service client
    docker_client = get_docker_service_client()
    worker_con = docker_client.containers.list(filters={"name": "worker"})[0]
    # start Navitia with custom docker-compose that include secondary_custom_coverage_name
    # start_navitia_w_custom_cov(secondary_custom_coverage_name)

    # Move the default coverage graph to the secondary coverage
    # try:
    # move_one_graph_to_secondary(worker_con, default_coverage_name, secondary_custom_coverage_name)
    # catch error:
    #   print(error)
    #   exit

    # stop all docker containers and restart to process renamed graphs
    # stop_all_containers(docker_client)
    # start_navitia_w_custom_cov(secondary_custom_coverage_name)

    # Copy the old secondary custom graph to your host and delete it from the container
    # copy_graph_to_local_host(worker_con, old_secondary_custom_coverage_name)
    # delete_grpah_from_container(worker_con, old_secondary_custom_coverage_name)

    #####NEED TO IMPLEMENT COPY BETWEEN E2C
    copy_graph_from_remote_host_to_container(worker_con, old_secondary_custom_coverage_name)


    # Copy the OSM & GTFS to default coverage
    # Re-start the service so the graph name changes will be updated and OSM & GTFS run

    # Verify the covereges reflect new data within 2 hours, otherwise send an email with alert

    print("Done")
