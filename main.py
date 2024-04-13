import configparser
import logging
import os

import coloredlogs

from Preprocessing import Preprocessing


def main():
    preprocessor = Preprocessing(root=os.path.abspath('/'))
    data_directory = input("Please enter the path to the data directory: ")
    output_directory = input("Please enter the path to the output directory: ")
    config_file = input("Please enter the path to the configuration file: ")
    participants_label = input("Please enter the participants label: ")

    if preprocessor.check_existence([data_directory, config_file]):
        preprocessor.convert_dcom_to_bids_json(data_directory, output_directory, participants_label, config_file)
    else:
        logging.error("The data directory or configuration file does not exist.")


if __name__ == "__main__":
    coloredlogs.install()
    main()
