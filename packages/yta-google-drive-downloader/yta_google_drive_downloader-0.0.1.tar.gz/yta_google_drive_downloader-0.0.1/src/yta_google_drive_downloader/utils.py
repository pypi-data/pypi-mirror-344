from yta_google_drive_downloader.constants import DRIVE_RESOURCE_URL, CONFIRMATION_STRING
from lxml.html import fromstring

import requests


def parse_url(
    drive_url: str
) -> str:
    """
    Validate the provided 'drive_url' and return it if
    valid, with some modifications if needed.

    This method will raise an Exception if the 'drive_url'
    parameter is not a valid, open and sharable Google Drive
    url.
    """
    # Force 'http' to 'https'
    drive_url = drive_url.replace('http://', 'https://')

    # Force 'https'
    if not drive_url.startswith('https://'):
        drive_url = f'https://{drive_url}'

    if not drive_url.startswith(DRIVE_RESOURCE_URL):
        raise Exception(f'Provided "google_drive_url" parameter {drive_url} is not valid. It must be like "{DRIVE_RESOURCE_URL}..."')

    if not CONFIRMATION_STRING in drive_url:
        # previously was '&confirm=1' to avoid virus scan as they say:
        # https://github.com/tensorflow/datasets/issues/3935#issuecomment-2067094366
        drive_url += f'&{CONFIRMATION_STRING}'

    return drive_url

def is_shareable_google_drive_url(
    drive_url: str
) -> bool:
    """
    Check if the given 'drive_url' is a valid sharable Google
    Drive url.

    This method doesn't modify the url nor includes the
    CONFIRM_STRING.
    """
    # Force 'http' to 'https'
    drive_url = drive_url.replace('http://', 'https://')

    return drive_url.startswith(DRIVE_RESOURCE_URL)

def get_id_from_url(
    drive_url: str
) -> str:
    """
    Parse the provided 'drive_url' and return the Google Drive
    resource id if the url is valid.

    This method will raise an Exception if the 'drive_url'
    parameter is not a valid, open and sharable Google Drive
    url.
    """
    drive_url = parse_url(drive_url)

    return drive_url.replace(DRIVE_RESOURCE_URL, '').split('/')[0]

def get_filename_from_url(
    drive_url: str
) -> str:
    """
    Parse the provided 'drive_url' and return the Google Drive
    resource filename (as stored in Google Drive) if the url is
    valid.

    This is the real filename in Google Drive, so its extension
    should be also the real one.

    (!) This method will fire a GET request to the Google Drive
    url if valid to obtain the metadata.

    This method will raise an Exception if the 'drive_url'
    parameter is not a valid, open and sharable Google Drive
    url.
    """
    drive_url = parse_url(drive_url)

    return fromstring(requests.get(drive_url).content).findtext('.//title').split('-')[0].strip()