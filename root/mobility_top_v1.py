#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
"""
This script is the top level script for compare of mobility from city/town to POIs at two different dates

prerequisit:
    create navitia graph for date1
        coverage_name = "ondemand-" + cfg.gtfsdate1
        graph_name = coverage_name + ".nav.lz4"
        navitia_docker_compose_file_name = "navitia-docker-ondemand-" + cfg.gtfsdate1 + ".yml"
        navitia_docker_compose_file_path = Path(os.getcwd()).parent.parent / "navitia-docker-compose" / "compose_files"
    create navitia graph for date2
        coverage_name = "ondemand-" + cfg.gtfsdate2
        graph_name = coverage_name + ".nav.lz4"
        navitia_docker_compose_file_name = "navitia-docker-ondemand-" + cfg.gtfsdate2 + ".yml"
        navitia_docker_compose_file_path = Path(os.getcwd()).parent.parent / "navitia-docker-compose" / "compose_files"
    docker running with both graphs loaded into container

flow:
    mobility_navitia_up.py with gtfsdate1 to create the server
    mobility_spectrum_v8.py with servicedate1 muni name and POI locations and names. 
        output file per poi: "cumareapersample_"+muni_name+servicedate1+poi_name+"_v7.txt"
    mobility_navitia_up.py with gtfsdate2 to create the server
    mobility_spectrum_v8.py with servicedate2 muni name and POI locations and names
        output file per poi: "cumareapersample_"+muni_name+servicedate2+poi_name+"_v7.txt"
    mobility_compare.py date1 and date2 results per POI
        output file with histogram and cumulative histogram compare
        output file with time samples and statistics compare: min | 25% | 50% | 75% | max

"""
import mobility_spectrum_cfg as cfg
import mobility_navitia_up
import mobility_spectrum_v8
import mobility_compare

mobility_navitia_up.main(cfg.gtfsdate1)
mobility_spectrum_v8.main(cfg.gtfsdate1, cfg.servicedate1)

mobility_navitia_up.main(cfg.gtfsdate2)
mobility_spectrum_v8.main(cfg.gtfsdate2, cfg.servicedate2)

mobility_compare.main()
