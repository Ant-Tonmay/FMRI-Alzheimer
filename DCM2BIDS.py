import subprocess
import os
import json

import numpy as np
import logging


# Function to update JSON files recursively
def update_json_files(directory):
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


# Path to the dcm2bids executable
dcm2bids_executable = "venv/bin/dcm2bids"

# Path to the DICOM directory
dicom_directory = "ADNI"

# Participant label
participant_label = "002"
mode = 0o755

# Path to the configuration file
config_file = "config.json"
directory_path = 'scaffold'
try:
    # Create the directory if it doesn't exist
    os.makedirs(directory_path, exist_ok=True)

    # Set permissions on the directory
    os.chmod(directory_path, mode)
    print(f"Directory '{directory_path}' created with permissions {oct(mode)}")
except OSError as e:
    print(f"Error creating directory: {e}")

try:
    subprocess.run(["venv/bin/dcm2bids_scaffold", "-o", directory_path], check=True)
except subprocess.CalledProcessError as e:
    print(f"Error in Scaffolding: {e}")

metadata = {
    "Name": "fMRI Preprocessing",
    "License": "Your License",
    "Authors": ["Agniswar Chakranorty", "Sanjoy Kumar Saha"],
    "Acknowledgments": "Acknowledgments text",
    "HowToAcknowledge": "How to acknowledge text",
    "Funding": ["Funding source 1", "Funding source 2"],
    "ReferencesAndLinks": ["Reference 1", "Reference 2"],
    "DatasetDOI": "Your Dataset DOI"
}

# Specify the path to the JSON file
json_file_path = f"{directory_path}/dataset_description.json"

# Load the existing JSON data
with open(json_file_path, 'r') as json_file:
    existing_data = json.load(json_file)

# Update the existing JSON data with the metadata values
existing_data.update(metadata)

# Write back the updated JSON data
with open(json_file_path, 'w') as json_file:
    json.dump(existing_data, json_file, indent=4)

# Construct the command to run dcm2bids
# dcm2bids -d sourcedata/dcm_qa_nih/In/ -p ID01 -c code/dcm2bids_config.json --bids_validate

file_path = "license.txt"

file_content = """agnichakra.cdcju@jadavpuruniversity.in
74656
*C2naUD.T79MY
FSzkCS5lEogMI
fcwGoTSkImw+SB8ZRdlGBk6nlg4fUKiVL6nznX9W8Lnm8omGiu38L7wNMqWvkO74"""
file_mode = 0o755  # Example mode - Read, Write, Execute for owner; Read, Execute for group and others

# Create the file
with open(file_path, 'w') as file:
    file.write(file_content)

# Set the file permissions
os.chmod(file_path, file_mode)




command = [dcm2bids_executable, "-d", dicom_directory, "-p", participant_label, "-o", directory_path, "-c", config_file,
           "--auto_extract_entities", "--force_dcm2bids", "--clobber"]

print(command)
# Execute the dcm2bids command using subprocess
try:
    subprocess.run(command, check=True)
    print("DICOM to BIDS conversion successful.")
except subprocess.CalledProcessError as e:
    print(f"Error converting DICOM to BIDS: {e}")

update_json_files(f"{directory_path}/sub-{participant_label}")

bids_validation_command = ["bids-validator", directory_path]

try:
    subprocess.run(bids_validation_command, check=True)
except subprocess.CalledProcessError as e:
    print(e)
