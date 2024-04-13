import json
import logging
import os
import subprocess
import sys
from typing import Any

import numpy as np


class Preprocessing:
    def __init__(self, root):
        self.bids_validator_installed = self.check_bids_validator
        self.root = root
        self.metadata = {
            "Name": "fMRI Preprocessing",
            "License": "Your License",
            "Authors": ["Agniswar Chakranorty", "Sanjoy Kumar Saha"],
            "Acknowledgments": "Acknowledgments text",
            "HowToAcknowledge": "How to acknowledge text",
            "Funding": ["Funding source 1", "Funding source 2"],
            "ReferencesAndLinks": ["Reference 1", "Reference 2"],
            "DatasetDOI": "Your Dataset DOI"
        }

        # print(f"root is initialised at {self.root}")

        if self.bids_validator_installed:
            logging.info("<==================BIDS validator already installed=========>")
        else:
            logging.warning("<==================BIDS validator not installed=========>")
            self.install_bids_validator()

    """
    It will check BIDS validator is installed or not
 
    """

    def check_bids_validator(self) -> bool:
        try:
            # Check if bids-validator is installed globally
            subprocess.check_output(["bids-validator", "--version"])
            return True
        except (FileNotFoundError, subprocess.CalledProcessError):
            return False

    """
    It will install BIDS validator if it is  not installed 
     
    """

    def install_bids_validator(self) -> Any:
        try:
            # Install bids-validator globally using npm
            subprocess.check_call(["npm", "install", "-g", "bids-validator"])
            self.bids_validator_installed = True
            print("BIDS validator installed successfully.")
        except subprocess.CalledProcessError:
            print("Failed to install BIDS validator.")

    def check_existence(self, file_or_folder_names: list) -> bool:
        for name in file_or_folder_names:
            if not os.path.exists(name):
                return False
        return True

    def update_json_files(self, directory) -> Any:
        TRsec = 3
        nSlices = 48
        TA = TRsec / nSlices  # assumes no temporal gap between volumes
        bidsSliceTiming = np.arange(0, TRsec, TA)  # ascending

        # Update the metadata dictionary with SliceTiming
        sliceTiming = bidsSliceTiming.tolist()
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith(".json"):  # Check if the file is a JSON file
                    file_path = os.path.join(root, file)
                    # Read the JSON file
                    with open(file_path, 'r') as json_file:
                        data = json.load(json_file)
                    # Update the JSON data with TaskName: rest
                    data["TaskName"] = "rest"
                    data["SliceTiming"] = sliceTiming
                    # Write back the updated JSON data
                    with open(file_path, 'w') as json_file:
                        json.dump(data, json_file, indent=4)

    def convert_dcom_to_bids_json(self, data_directory: str, output_directory: str, participant_label: str,
                                  config_file: str) -> Any:
        # Construct the path to the virtual environment folder
        venv_folder_path = os.path.basename(os.environ['VIRTUAL_ENV'])
        print(venv_folder_path)
        dcm2bids_executable = f"{venv_folder_path}/bin/dcm2bids"
        # Path to the DICOM directory
        dicom_directory = data_directory
        mode = 0o755
        # Path to the configuration file
        config_file = config_file
        directory_path = output_directory
        try:
            # Create the directory if it doesn't exist
            os.makedirs(directory_path, exist_ok=True)
            # Set permissions on the directory
            os.chmod(directory_path, mode)
            print(f"Directory '{directory_path}' created with permissions {oct(mode)}")
        except OSError as e:
            os.rmdir(directory_path)
            print(f"Error creating directory: {e}")

        try:
            subprocess.run([f"{venv_folder_path}/bin/dcm2bids_scaffold", "-o", directory_path], check=True)
        except subprocess.CalledProcessError as e:
            os.rmdir(directory_path)
            print(f"Error in Scaffolding: {e}")

        logging.info("Meta data creation for bids scaffolding is starting....")

        metadata_choice = input("Do you wish to create the metadata? (y/n) ")
        if metadata_choice == "y":
            print("Creating metadata...")
        # take some inputs to build the metadata for the dcm to bids structure.... Reminder  you have to take atleast
        # two authors and have to make alist like that: "Authors": ["Agniswar Chakranorty", "Sanjoy Kumar Saha"],

        # Specify the path to the JSON file
        json_file_path = f"{directory_path}/dataset_description.json"
        # Load the existing JSON data
        with open(json_file_path, 'r') as json_file:
            existing_data = json.load(json_file)

        # Update the existing JSON data with the metadata values
        existing_data.update(self.metadata)
        # Write back the updated JSON data
        with open(json_file_path, 'w') as json_file:
            json.dump(existing_data, json_file, indent=4)

        command = [dcm2bids_executable, "-d", dicom_directory, "-p", participant_label, "-o", directory_path, "-c",
                   config_file,
                   "--auto_extract_entities", "--force_dcm2bids", "--clobber"]

        try:
            subprocess.run(command, check=True)
            print("DICOM to BIDS conversion successful.")
        except subprocess.CalledProcessError as e:
            print(f"Error converting DICOM to BIDS: {e}")

        self.update_json_files(f"{directory_path}/sub-{participant_label}")

        bids_validation_command = ["bids-validator", directory_path]

        try:
            subprocess.run(bids_validation_command, check=True)
        except subprocess.CalledProcessError as e:
            print(e)

    def fmri_preprocessing(self, data_directory: str, output_directory: str, participant_label: str,
                           config_file: str) -> Any:
        pass
