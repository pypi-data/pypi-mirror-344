import datetime
from pathlib import Path
from typing import Optional
from pydantic import BaseModel, ConfigDict

from yarl import URL


class BaseSample(BaseModel):
    """
    Model of samples that is used for the hand-over between the import and export parts of the code.
    """
    # Name of the project
    project_name: Optional[str] = None

    # Label of the subject
    subject_label: Optional[str] = None

    # Label of the experiment
    experiment_label: Optional[str] = None

    # Date on which the experiment is acquired
    experiment_date: Optional[datetime.date] = None

    # ID of the scan
    scan_id: Optional[str] = None

    # Type of the scan (e.g. T1w)
    scan_type: Optional[str] = None

    # The filename of the file within the scan. This can be a partial path if it has subdirectories
    # e.g. DICOM for a dicom folder or NIFTI/image.nii.gz for a nifti file
    filename: Optional[str] = None

    # The label of the timepoint the data is from (e.g. baseline)
    timepoint: Optional[str] = None


class PathSample(BaseSample):
    # Path to the data on disk, this is where the import part of the tool wrote the data and where
    # the export part can pick it up
    data_path: Path


class URLSample(BaseSample):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    # The URL of the data to retrieve.
    data_url: URL
