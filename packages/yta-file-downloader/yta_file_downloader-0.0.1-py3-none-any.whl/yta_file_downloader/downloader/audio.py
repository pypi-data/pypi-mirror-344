from yta_file_downloader.utils import download_file
from yta_file_downloader.dataclass import UnparsedFile
from yta_file_downloader.enums import FileParsingMethod
from yta_general_utils.file.enums import FileTypeX
from yta_general_utils.programming.output import Output
from typing import Union


def download_audio(
    url: str,
    output_filename: Union[str, None] = None
) -> UnparsedFile:
    """
    Download an audio file from the given 'url' (if valid)
    that is stored locally as the given 'output_filename'.

    This method returns an UnparsedFile instance to be able
    to handle the file content with the appropriate library.
    """
    # TODO: What if not able to download it (?)
    file = download_file(url, Output.get_filename(output_filename, FileTypeX.AUDIO))

    file.parsing_method = FileParsingMethod.PYDUB_AUDIO

    return file