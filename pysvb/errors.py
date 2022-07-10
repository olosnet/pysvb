#
# Python binding to SVBONY Cameras Driver
# Copyright (c) 2022 Valerio Faiuolo
#
# Errors and exceptions
#

from enum import IntEnum, auto


class SVB_CAMERA_ERRORS(IntEnum):

    SVB_PYINTERNAL_ERROR = -1
    "python binding internal error"
    SVB_SUCCESS = 0
    "all ok"
    SVB_ERROR_INVALID_INDEX = auto()
    "no camera connected or index value out of boundary"
    SVB_ERROR_INVALID_ID = auto()
    "invalid ID"
    SVB_ERROR_INVALID_CONTROL_TYPE = auto()
    "invalid control type"
    SVB_ERROR_CAMERA_CLOSED = auto()
    "camera didn't open"
    SVB_ERROR_CAMERA_REMOVED = auto()
    "failed to find the camera, maybe the camera has been removed"
    SVB_ERROR_INVALID_PATH = auto()
    "cannot find the path of the file"
    SVB_ERROR_INVALID_FILEFORMAT = auto()
    "invalid file format"
    SVB_ERROR_INVALID_SIZE = auto()
    "wrong video format size"
    SVB_ERROR_INVALID_IMGTYPE = auto()
    "unsupported image format"
    SVB_ERROR_OUTOF_BOUNDARY = auto()
    "the startpos is out of boundary"
    SVB_ERROR_TIMEOUT = auto()
    "timeout"
    SVB_ERROR_INVALID_SEQUENCE = auto()
    "stop capture first"
    SVB_ERROR_BUFFER_TOO_SMALL = auto()
    "buffer size is not big enough"
    SVB_ERROR_VIDEO_MODE_ACTIVE = auto()
    SVB_ERROR_EXPOSURE_IN_PROGRESS = auto()
    "exposure in progress"
    SVB_ERROR_GENERAL_ERROR = auto()
    "general error, eg: value is out of valid range"
    SVB_ERROR_INVALID_MODE = auto()
    "the current mode is wrong"
    SVB_ERROR_INVALID_DIRECTION = auto()
    "invalid guide direction"
    SVB_ERROR_UNKNOW_SENSOR_TYPE = auto()
    "unknow sensor type"
    SVB_ERROR_END = auto()


class SvbonyCameraError:

    class InvalidIndex(Exception):
        """No camera connected or index value out of boundary exception"""
        def __init__(self):
            super().__init__()

    class InvalidId(Exception):
        """Invalid ID exception"""
        def __init__(self):
            super().__init__()

    class InvalidControlType(Exception):
        """Invalid control type exception"""
        def __init__(self):
            super().__init__()

    class CameraClosed(Exception):
        """Camera didn't open exception"""
        def __init__(self):
            super().__init__()

    class CameraRemoved(Exception):
        """Failed to find the camera, maybe the camera has been removed exception"""
        def __init__(self):
            super().__init__()

    class InvalidPath(Exception):
        """Cannot find the path of the file exception"""
        def __init__(self):
            super().__init__()

    class InvalidFileFormat(Exception):
        """Invalid file format exception"""
        def __init__(self):
            super().__init__()

    class InvalidSize(Exception):
        """Wrong video format size exception"""
        def __init__(self):
            super().__init__()

    class InvalidImgType(Exception):
        """Unsupported image format exception"""
        def __init__(self):
            super().__init__()

    class OutOfBoundary(Exception):
        """The startpos is out of boundary exception"""
        def __init__(self):
            super().__init__()

    class Timeout(Exception):
        """Timeout exception"""
        def __init__(self):
            super().__init__()

    class InvalidSequence(Exception):
        """Invalid sequence exception (stop capture first)"""
        def __init__(self):
            super().__init__()

    class BufferTooSmall(Exception):
        """Buffer size is not big enough exception"""
        def __init__(self):
            super().__init__()

    class VideoModeActive(Exception):
        def __init__(self):
            super().__init__()

    class ExposureInProgress(Exception):
        """Exposure in progress exception"""
        def __init__(self):
            super().__init__()

    class GeneralError(Exception):
        """General error exception"""
        def __init__(self):
            super().__init__()

    class InvalidMode(Exception):
        """Invalid mode exception"""
        def __init__(self):
            super().__init__()

    class InvalidDirection(Exception):
        """Invalid guide direction exception"""
        def __init__(self):
            super().__init__()

    class UnknowSensorType(Exception):
        """Unknow sensor type exception"""
        def __init__(self):
            super().__init__()

    class ErrorEnd(Exception):
        def __init__(self):
            super().__init__()

    class PyInternalError(Exception):
        """Python internal error exception"""
        def __init__(self):
            super().__init__()

    class UnknownError(Exception):
        """Unknown error exception"""
        def __init__(self):
            super().__init__()



