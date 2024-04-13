def create_key(template, outtype=('nii.gz',), annotation_classes=None):
    if template is None or not template:
        raise ValueError("Template must be a valid format string")

    return template, outtype, annotation_classes

# Define the conversion rules using create_key function
subject_sessions = create_key('sub-{subject}/{session}/')

# Specify conversion rules for each modality
t1w = create_key(subject_sessions[0] + 'anat/sub-{subject}_{session}_T1w')
t2w = create_key(subject_sessions[0]  + 'anat/sub-{subject}_{session}_T2w')
func_rest = create_key(subject_sessions[0]  + 'func/sub-{subject}_{session}_task-rest_bold')
dwi = create_key(subject_sessions[0]  + 'dwi/sub-{subject}_{session}_acq-multiband_dwi')

# Define the heuristic dictionary
def infotodict(seqinfo):
    return {
        t1w: [info for info in seqinfo if info.series_description.startswith('T1')],
        t2w: [info for info in seqinfo if info.series_description.startswith('T2')],
        func_rest: [info for info in seqinfo if info.series_description.startswith('rest')],
        dwi: [info for info in seqinfo if info.series_description.startswith('multiband')]
    }


def infotoids(seqinfo, outdir):
    subject_list = []
    for key in seqinfo:
        # Extract subject ID from DICOM metadata (adjust this based on your DICOM metadata structure)
        subject_id = key.patient_id  # assuming the DICOM key has a 'patient_id' attribute
        if subject_id:
            subject_list.append(subject_id)
    return subject_list