from yta_file_downloader.utils import download_file
from yta_file_downloader.dataclass import UnparsedFile
from yta_file_downloader.enums import FileParsingMethod
from yta_general_utils.programming.output import Output
from yta_general_utils.file.enums import FileTypeX
from typing import Union


def download_video(
    url: str,
    output_filename: Union[str, None] = None
) -> UnparsedFile:
    """
    Download the video from the given 'url' (if valid) and
    store it locally as 'output_filename' if provided.
    """
    file = download_file(url, Output.get_filename(output_filename, FileTypeX.VIDEO))

    file.parsing_method = FileParsingMethod.MOVIEPY_VIDEO

    return file