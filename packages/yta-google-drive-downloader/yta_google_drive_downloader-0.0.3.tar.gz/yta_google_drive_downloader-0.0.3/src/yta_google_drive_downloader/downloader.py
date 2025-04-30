from yta_google_drive_downloader.constants import DOWNLOAD_URL
from yta_google_drive_downloader.utils import is_shareable_google_drive_url
from yta_general_utils.file.writer import FileWriter
from yta_general_utils.file.filename import get_file_extension
from yta_general_utils.programming.validator import PythonValidator
from yta_general_utils.programming.output import Output
from typing import Union

import requests


class GoogleDriveDownloader:
    """
    Class to simplify the way we download Google Drive
    resources.
    """

    @staticmethod
    def download(
        id_or_drive_url_or_resource: Union[str, 'GoogleDriveResource'],
        output_filename: Union[str, None] = None
    ):
        """
        Download the Google Drive resource according to the
        id, url or resource instance provided. It will be
        stored locally with the also given 'output_filename'
        that will match the real filename extension.
        """
        if (
            not PythonValidator.is_string and
            not PythonValidator.is_instance(id_or_drive_url_or_resource, 'GoogleDriveResource')
        ):
            raise Exception('The provided "id_or_drive_url_or_resource" parameter is not a valid GoogleDriveResource instance nor a valid id or Google Drive url.')

        # 1. First way:
        if PythonValidator.is_instance(id_or_drive_url_or_resource, 'GoogleDriveResource'):
            output_filename = Output.get_filename(
                output_filename,
                get_file_extension(id_or_drive_url_or_resource.filename)
            )
            id_or_drive_url_or_resource = id_or_drive_url_or_resource.id,

        download_method = (
            GoogleDriveDownloader.download_from_url
            if is_shareable_google_drive_url(id_or_drive_url_or_resource) else
            GoogleDriveDownloader.download_from_id
        )

        return download_method(
            id_or_drive_url_or_resource,
            output_filename
        )

    @staticmethod
    def download_from_url(
        drive_url: str,
        output_filename: Union[str, None] = None
    ):
        """
        Download the Google Drive resource from the given
        'drive_url' and store it locally with the also
        provided 'output_filename'.
        """
        from yta_google_drive_downloader.resource import GoogleDriveResource

        return GoogleDriveDownloader.download(
            GoogleDriveResource(drive_url),
            output_filename
        )
    
    @staticmethod
    def download_from_id(
        id: str,
        output_filename: Union[str, None] = None
    ):
        """
        Download the Google Drive resource with the given
        'id' and store it locally with the also provided
        'output_filename'.
        """
        session = requests.Session()
        # Trying to obtain the web title to get the file name
        response = session.get(DOWNLOAD_URL, params = {'id': id}, stream = True)

        # Look for a token to be able to download
        token = None
        for key, value in response.cookies.items():
            if key.startswith('download_warning'):
                token = value
                break

        if token:
            params = {'id': id, 'confirm': token}
            response = session.get(DOWNLOAD_URL, params = params, stream = True)
            # TODO: Handle virus unchecked Google warning that contains this below:
            # <title>Google Drive - Virus scan warning</title>
            # check Notion for the entire error message

        # Save response
        FileWriter.write_file_by_chunks_from_response(response, output_filename)

        return output_filename