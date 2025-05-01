from yta_general_utils.programming.enum import YTAEnum as Enum
from yta_general_utils.file.enums import FileTypeX


class FileParsingMethod(Enum):
    """
    Enum class to indicate the different options we have
    to parse an UnparsedFile according to its content.

    This enum class is very usefull when we are returning
    files that will be parsed in another library, but we
    don't want to install those libraries here as 
    dependencies, so it is only the external library who
    does it and only with the needed libraries. If we are
    parsing only image files, we will install the 'pillow'
    library to parse those images, but not the other
    libraries as they are not needed.

    Each enum element includes docummentation about which
    library must be installed and what is the exact code
    to parse the file properly.
    """

    PILLOW_IMAGE = 'pillow_image'
    """
    The file is an image file and must be read with the
    pillow library.

    Needed library:
    - `pillow`

    Needed code:
    - `Image.open(filename)`
    """
    PYDUB_AUDIO = 'pydub_audio'
    """
    The file is an audio file and must be read with the
    pydub library.

    Needed library:
    - `pydub`

    Needed code:
    - `AudioSegment.from_file(filename)`
    """
    MOVIEPY_VIDEO = 'moviepy_video'
    """
    The file is a video file and must be read with the
    moviepy library.

    Needed library:
    - `moviepy`

    Needed code:
    - `VideoFileClip(filename)`
    """
    IO_SUBTITLES = 'io_subtitles'
    """
    This file is a plain text file (that contains
    subtitles) and must be read with the io library.

    Needed library:
    - `io`

    Needed code:
    - `io.BytesIO(filename).getvalue().decode('utf-8')`
    """
    IO_TEXT = 'io_text'
    """
    This file is a plain text file and must be read with
    the io library.

    Needed library:
    - `io`

    Needed code:
    - `io.BytesIO(filename).getvalue().decode('utf-8')`
    """
    UNPARSEABLE = 'unparseable'
    """
    This file has an extension that cannot be parsed by
    our system.
    """

    @property
    def as_file_type(
        self
    ) -> FileTypeX:
        """
        Transform this FileParsingMethod enum to its corresponding
        FileTypeX enum instance.
        """
        return FileParsingMethod.to_file_type(self)
    
    @staticmethod
    def to_file_type(
        file_parsing_method: 'FileParsingMethod'
    ) -> FileTypeX:
        """
        Transform the given 'file_parsing_method' FileParsingMethod
        enum instance parameter to its corresponding FileTypeX enum
        instance.
        """
        return {
            FileParsingMethod.MOVIEPY_VIDEO: FileTypeX.VIDEO,
            FileParsingMethod.PILLOW_IMAGE: FileTypeX.IMAGE,
            FileParsingMethod.PYDUB_AUDIO: FileTypeX.AUDIO,
            FileParsingMethod.IO_SUBTITLES: FileTypeX.SUBTITLE,
            FileParsingMethod.IO_TEXT: FileTypeX.TEXT
        }.get(
            FileParsingMethod.to_enum(file_parsing_method),
            # TODO: How to handle this 'unknown' file type?
            FileTypeX.UNKNOWN
        )

    @staticmethod
    def from_file_type(
        file_type: 'FileTypeX'
    ):
        """
        Get the FileParsingMethod enum instance that corresponds
        to the given 'file_type' FileTypeX enum instance.
        """
        return {
            FileTypeX.VIDEO: FileParsingMethod.MOVIEPY_VIDEO,
            FileTypeX.IMAGE: FileParsingMethod.PILLOW_IMAGE,
            FileTypeX.AUDIO: FileParsingMethod.PYDUB_AUDIO,
            FileTypeX.SUBTITLE: FileParsingMethod.IO_SUBTITLES,
            FileTypeX.TEXT: FileParsingMethod.IO_TEXT
        }.get(
            FileTypeX.to_enum(file_type),
            FileParsingMethod.UNPARSEABLE
        )