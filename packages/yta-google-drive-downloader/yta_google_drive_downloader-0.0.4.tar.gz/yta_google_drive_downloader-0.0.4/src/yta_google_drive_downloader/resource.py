from yta_google_drive_downloader.utils import parse_url, get_filename_from_url, get_id_from_url
from yta_google_drive_downloader.downloader import GoogleDriveDownloader
from typing import Union


class GoogleDriveResource:
    """
    Class to handle Google Drive Resources. Just instantiate it with its
    Google Drive url and it will be ready for download if the url is valid
    and available.

    A valid 'drive_url' must be like this:
    https://drive.google.com/file/d/1rcowE61X8c832ynh0xOt60TH1rJfcJ6z/view?usp=sharing&confirm=1
    """
    url: str = ''
    """
    The sharable url that contains the resource id.
    """

    @property
    def id(self) -> str:
        """
        The id of the resource, extracted from the given url.
        """
        if not hasattr(self, '_id'):
            self._id = get_id_from_url(self.url)

        return self._id
    
    @property
    def filename(self) -> str:
        """
        The original resource's filename with which it has been
        stored in Google Drive.
        """
        if not hasattr(self, '_filename'):
            self._filename = get_filename_from_url(self.url)

        return self._filename

    def __init__(
        self,
        drive_url: str
    ):
        """
        Initialize the instance by setting the provided 'drive_url',
        that must be a valid one. This method will fire a GET request
        to obtain the real resource filename (if a valid resource).

        This method will raise an Exception if the 'drive_url'
        parameter is not a valid, open and sharable Google Drive
        url.
        """
        self.url = parse_url(drive_url)
        # Force 'filename' to be obtained firing the request
        if self.filename is None:
            raise Exception('No original "filename" found, so it is not accesible.')

    def download(
        self,
        output_filename: Union[str, None] = None
    ) -> str:
        """
        Download the Google Drive resource to the local storage
        with the given 'output_filename'.

        This method returns the definitive downloaded filename.
        """
        return GoogleDriveDownloader.download(self, output_filename)