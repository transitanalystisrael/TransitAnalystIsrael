import argparse
import csv
import math
import sys
from argparse import RawTextHelpFormatter
import os
from scripts import utils
import progressbar
import re

EARTH_RADIUS = 6372797.560856


# holds Transfer metrics between stops
class TransferMetrics:
    def __init__(self, from_stop_id, to_stop_id, transfer_type, min_transfer_time):
        self.from_stop_id = from_stop_id
        self.to_stop_id = to_stop_id
        self.transfer_type = transfer_type
        self.min_transfer_time = min_transfer_time

    def __str__(self):
        return self.from_stop_id + "," + self.to_stop_id + "," + self.transfer_type + "," + self.min_transfer_time


class Stop:
    def __init__(self, sid, lon, lat, location_type):
        self.sid = sid
        self.lat = lat
        self.lon = lon
        self.location_type = location_type

    def __str__(self):
        return self.sid + "," + self.lon + "," + self.lat + "," + self.location_type

    def to_dict(self):
        return {
            'sid': self.sid,
            'lon': self.lon,
            'lat': self.lat,
            'location_type': self.location_type
        }


def read_file(input_file):
    stops = dict()

    with open(input_file, encoding="utf8", mode='r') as f:
        reader = csv.reader(f)
        header = next(reader)
        # Due to encoding, sometimes the "stop_id" string is preceded by different characters
        stop_id_reg = re.compile(r".*stop_id")
        stop_id_rep = list(filter(stop_id_reg.match, header))[0]
        stop_id_ind = header.index(stop_id_rep)
        stop_lon_ind = header.index("stop_lon")
        stop_lat_ind = header.index("stop_lat")
        location_type_ind = header.index("location_type")

        for row in reader:
            # we want only stops of type 0 (which are stops and not physical station or entrance - see GTFS docs)
            stop_location_type = row[location_type_ind]
            if stop_location_type == '0':
                data_tpl = Stop(row[stop_id_ind], row[stop_lon_ind], row[stop_lat_ind], row[location_type_ind])
                # Store the stop data: id, lon, Lat
                stop_id = row[stop_id_ind]
                stops[stop_id] = data_tpl
    return stops


def calculate_transfers(stops, walking_speed, transfer_time, max_distance):
    transfers = list()
    pbar = utils.createProgressBar((len(stops)**2), action='Calculating Transfers: ')
    # for progress bar we need the number of coming
    i = 0
    # itrerations
    for stop_1_ind in stops:
        stop_1 = stops[stop_1_ind]
        for stop_2_ind in stops:
            # updating the progress bar
            pbar.update(i)
            progressbar.streams.flush()
            i += 1
            stop_2 = stops[stop_2_ind]
            # if stop_1.sid != stop_2.sid: - Navitia's rust code doesnt ignore this
            man_distance = calculate_man_distance(stop_1, stop_2)
            if man_distance <= max_distance:
                transfers.append(TransferMetrics(stop_1.sid, stop_2.sid, 2, int(man_distance / walking_speed)
                                                 + transfer_time))
    pbar.finish()
    return transfers


def calculate_man_distance(stop1, stop2):
    phi1 = math.radians(float(stop1.lat))
    phi2 = math.radians(float(stop2.lat))
    lambda1 = math.radians(float(stop1.lon))
    lambda2 = math.radians(float(stop2.lon))

    x = math.sin((phi2 - phi1) / 2) ** 2
    y = math.cos(phi1) * math.cos(phi2) * math.sin((lambda2 - lambda1) / 2.) ** 2

    return 2 * EARTH_RADIUS * math.asin(math.sqrt(x + y))


def write_file(output, transfers):
    with open(output, "w") as text_file:
        print(f"from_stop_id,to_stop_id,transfer_type,min_transfer_time", file=text_file)
        for ind, transfer in enumerate(transfers):
            transfer_datum = transfers[ind]
            print(f"{transfer_datum.from_stop_id},{transfer_datum.to_stop_id},{transfer_datum.transfer_type}, "
                  f"{transfer_datum.min_transfer_time} ", file=text_file)
    text_file.close()
    return text_file


def generate_transfers(input="stops.txt", output="transfers.txt", walking_speed=0.785, transfer_time=0,
                       max_distance=500):
    '''
    Generating the transfers file for Navitia Server - see default values above
    :param input: the name of the stops file to enter
            If the file isn't in the same folder as the script, give the full path
    :param output: the of the transfers files to output
    :param walking_speed: the walking speed
    :param transfer_time: if transfer time between stops should be calcualted
    :param max_distance: the maximum distance for tansfer
    :return: output file full path
    '''
    stops = read_file(input)
    transfers = calculate_transfers(stops, walking_speed, transfer_time, max_distance)
    write_file(output, transfers)
    print("Finished generating the transfers.txt file")
    return os.getcwd() + "/" + output


def generate_transfers_from_command_line(argv):
    """
    Generate a Transfers table for Navitia Server from command line
    :param argv:
    :return:
    """
    parser = argparse.ArgumentParser(formatter_class=RawTextHelpFormatter)
    parser.add_argument('input', nargs='?', help='input file', default='stops.txt')
    parser.add_argument('output', nargs='?', help='output file', default='transfers.txt')
    parser.add_argument('walking_speed', type=float, nargs='?',
                        help='The walking speed is meters per second.\n '
                             'You may want to divide your initial speed by \n '
                             'sqrt(2) to simulate Manhattan distances', default=0.785)
    parser.add_argument('transfer_time', type=int, nargs='?', help='Transfer time in seconds',
                        default='0')
    parser.add_argument('max_distance', type=float, nargs='?',
                        help='The max distance in meters to compute the transfer',
                        default=500)

    args = parser.parse_args(argv)

    stops = read_file(args.input)
    transfers = calculate_transfers(stops, args.walking_speed, args.transfer_time, args.max_distance)
    write_file(args.output, transfers)
    print("done")


if __name__ == "__main__":
    generate_transfers_from_command_line(sys.argv[1:])


# USE https://stackoverflow.com/questions/46572860/speeding-up-a-nested-for-loop-through-two-pandas-dataframes