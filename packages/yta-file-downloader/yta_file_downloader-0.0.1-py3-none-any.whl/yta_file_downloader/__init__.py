from yta_file_downloader.downloader.audio import download_audio
from yta_file_downloader.downloader.gif import download_gif
from yta_file_downloader.downloader.image import download_image_2
from yta_file_downloader.downloader.video import download_video
from yta_file_downloader.downloader.web.facebook.downloader import download_facebook_video
from yta_file_downloader.downloader.web.instagram.downloader import download_instagram_video
from yta_file_downloader.downloader.web.tiktok.downloader import download_tiktok_video
from yta_file_downloader.utils import download_file
from yta_file_downloader.dataclass import UnparsedFile
from yta_general_utils.programming.output import Output
from yta_general_utils.programming.validator import PythonValidator
from yta_general_utils.programming.validator.parameter import ParameterValidator
from yta_general_utils.file.enums import FileTypeX, FileExtension
from yta_google_drive_downloader.resource import GoogleDriveResource
from typing import Union


class Downloader:
    """
    Class to encapsulate the functionality related to downloading
    resources from the Internet.
    """

    @staticmethod
    def download_audio(
        url: str,
        output_filename: Union[str, None] = None
    ) -> UnparsedFile:
        """
        Download the audio file from the provided 'url' and stores
        it locally as 'output_filename'.
        """
        ParameterValidator.validate_mandatory_string('url', url, False)

        return download_audio(
            url,
            Output.get_filename(output_filename, FileTypeX.AUDIO)
        )
    
    @staticmethod
    def download_gif(
        query: str, 
        output_filename: Union[str, None] = None
    ) -> Union[UnparsedFile, None]:
        """
        Search for a gif with the provided 'query' and download it,
        if existing, to a local file called 'output_filename'.

        TODO: I think this is unexpected, because it is searching
        from Giphy and not downloading a file from a url as a gif...
        and I think it would be like 'download_image' just with
        the gif extension.
        """
        ParameterValidator.validate_mandatory_string('query', query, False)

        return download_gif(
            query,
            Output.get_filename(output_filename, FileExtension.GIF)
        )
    
    @staticmethod
    def download_google_drive_resource(
        google_drive_url: str,
        output_filename: Union[str, None] = None
    ) -> UnparsedFile:
        """
        Download the Google Drive resource from the given
        'google_drive_url', if existing and available, and
        store it locally with the provided 'output_filename'.
        """
        ParameterValidator.validate_mandatory_string('google_drive_url', google_drive_url, False)

        resource = GoogleDriveResource(google_drive_url)
        filename = resource.download(Output.get_filename(output_filename))

        return UnparsedFile(
            filename = filename,
            is_file = True,
            # TODO: Parse resource.extension to turn it into a
            # valid FileParsingMethod
            parsing_method = None,
            extra_args = {}
        )
    
    @staticmethod
    def download_image(
        url: str,
        output_filename: Union[str, None] = None
    ) -> UnparsedFile:
        """
        Download the image from the provided 'url' and stores it, if
        existing and available, as a local file called 'output_filename'.
        """
        ParameterValidator.validate_mandatory_string('url', url, False)
        
        return download_image_2(
            url,
            Output.get_filename(output_filename)
        )

    @staticmethod
    def download_video(
        url: str,
        output_filename: Union[str, None] = None
    ) -> UnparsedFile:
        """
        Download the video from the provided 'url' and stores it, if
        existing and available, as a local file called 'output_filename'.
        """
        ParameterValidator.validate_mandatory_string('url', url, False)
        
        return download_video(
            url,
            Output.get_filename(output_filename)
        )
    
    @staticmethod
    def download_file(
        url: str,
        output_filename: str
    ) -> UnparsedFile:
        if not PythonValidator.is_string(url):
            raise Exception('The provided "url" parameter is not a string.')
        
        # We don't know the kind of file we are downloading
        # so we need the filename as input
        if output_filename is None:
            raise Exception(f'The "output_filename" parameter is mandatory as we do not know the file extension.')
        
        return download_file(
            url,
            output_filename
        )

    # TODO: All these methods below could be in other library
    @staticmethod
    def download_tiktok(
        url: str,
        output_filename: Union[str, None, bool] = None
    ) -> Union[UnparsedFile, 'BytesIO']:
        """
        Download a Tiktok video from the given 'url' and
        stores it locally as the provided 'output_filename'
        (or a temporary one if not provided).
        """
        if not PythonValidator.is_string(url):
            raise Exception('The provided "url" parameter is not a string.')
        
        return download_tiktok_video(
            url,
            (
                Output.get_filename(output_filename)
                if output_filename is not False else
                False
            )
        )
    
    @staticmethod
    def download_facebook(
        url: str,
        output_filename: Union[str, None, bool] = None
    ) -> Union[UnparsedFile, 'BytesIO']:
        """
        Download a Facebook video from the given 'url' and
        stores it locally as the provided 'output_filename'
        (or a temporary one if not provided).
        """
        if not PythonValidator.is_string(url):
            raise Exception('The provided "url" parameter is not a string.')
        
        return download_facebook_video(
            url,
            (
                Output.get_filename(output_filename)
                if output_filename is not False else
                False
            )
        )
    
    @staticmethod
    def download_instagram(
        url: str,
        output_filename: Union[str, None, bool] = None
    ) -> Union[UnparsedFile, 'BytesIO']:
        """
        Download an Instagram video from the given 'url' and
        stores it locally as the provided 'output_filename'
        (or a temporary one if not provided).
        """
        if not PythonValidator.is_string(url):
            raise Exception('The provided "url" parameter is not a string.')
        
        return download_instagram_video(
            url,
            (
                Output.get_filename(output_filename)
                if output_filename is not False else
                False
            )
        )
