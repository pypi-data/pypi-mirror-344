from yta_file_downloader.enums import FileParsingMethod
from yta_general_utils.file.enums import FileTypeX
from yta_general_utils.file.filename import get_file_extension
from typing import Union
from dataclasses import dataclass


@dataclass
class UnparsedFile:
    """
    Class to wrap the information about a file that we
    are returning in a method that can be parsed in the
    library who is using this one.

    This dataclass has been created to avoid the library
    dependency so you just import the one you need to
    handle the file.
    """

    filename: str
    """
    The filename that contains the information.
    """
    is_file: bool
    """
    Flag to indicate if the 'filename' value is actually
    a file or if it is the raw content.
    """
    parsing_method: Union[FileParsingMethod, None]
    """
    The method to parse the file properly. If None, we
    didn't know the expected file type. Maybe you can
    check the exception.
    """
    extra_args: any
    """
    Any extra arg we should use when parsing the file.
    """

    @property
    def file_type(self) -> FileTypeX:
        """
        The file type associated to the parsing method that
        this unparsed file has.
        """
        return (
            self.parsing_method.as_file_type
            if self.FileParsingMethod is not None else
            None
        )

    @property
    def extension(self) -> Union[str, None]:
        """
        The extension of the file if a filename exist.
        """
        return (
            get_file_extension(self.filename)
            if (
                self.filename is not None and
                self.is_file
            ) else
            None
        )
    
    def __init__(
        self,
        filename: str,
        is_file: bool = True,
        parsing_method: Union[str, FileParsingMethod, None] = None,
        extra_args: any = {}
    ):
        self.filename = filename
        self.is_file = is_file
        self.parsing_method = (
            FileParsingMethod.to_enum(parsing_method)
            if parsing_method is not None else
            None
        )
        self.extra_args = extra_args

