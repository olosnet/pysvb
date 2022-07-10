#
# Python binding to SVBONY Cameras Driver
# Copyright (c) 2022 Valerio Faiuolo
#
# Helper functions
#

def SVB_ERROR_CODE_TO_EXC(code):
    from pysvb.errors import SVB_CAMERA_ERRORS, SvbonyCameraError

    codes = {
        SVB_CAMERA_ERRORS.SVB_ERROR_INVALID_INDEX: SvbonyCameraError.InvalidIndex,
        SVB_CAMERA_ERRORS.SVB_ERROR_INVALID_ID: SvbonyCameraError.InvalidId,
        SVB_CAMERA_ERRORS.SVB_ERROR_INVALID_CONTROL_TYPE: SvbonyCameraError.InvalidControlType,
        SVB_CAMERA_ERRORS.SVB_ERROR_CAMERA_CLOSED: SvbonyCameraError.CameraClosed,
        SVB_CAMERA_ERRORS.SVB_ERROR_CAMERA_REMOVED: SvbonyCameraError.CameraRemoved,
        SVB_CAMERA_ERRORS.SVB_ERROR_INVALID_PATH: SvbonyCameraError.InvalidPath,
        SVB_CAMERA_ERRORS.SVB_ERROR_INVALID_FILEFORMAT: SvbonyCameraError.InvalidFileFormat,
        SVB_CAMERA_ERRORS.SVB_ERROR_INVALID_SIZE: SvbonyCameraError.InvalidSize,
        SVB_CAMERA_ERRORS.SVB_ERROR_INVALID_IMGTYPE: SvbonyCameraError.InvalidImgType,
        SVB_CAMERA_ERRORS.SVB_ERROR_OUTOF_BOUNDARY: SvbonyCameraError.OutOfBoundary,
        SVB_CAMERA_ERRORS.SVB_ERROR_TIMEOUT: SvbonyCameraError.Timeout,
        SVB_CAMERA_ERRORS.SVB_ERROR_INVALID_SEQUENCE: SvbonyCameraError.InvalidSequence,
        SVB_CAMERA_ERRORS.SVB_ERROR_BUFFER_TOO_SMALL: SvbonyCameraError.BufferTooSmall,
        SVB_CAMERA_ERRORS.SVB_ERROR_VIDEO_MODE_ACTIVE: SvbonyCameraError.VideoModeActive,
        SVB_CAMERA_ERRORS.SVB_ERROR_EXPOSURE_IN_PROGRESS: SvbonyCameraError.Timeout,
        SVB_CAMERA_ERRORS.SVB_ERROR_GENERAL_ERROR: SvbonyCameraError.GeneralError,
        SVB_CAMERA_ERRORS.SVB_ERROR_INVALID_MODE: SvbonyCameraError.InvalidMode,
        SVB_CAMERA_ERRORS.SVB_ERROR_INVALID_DIRECTION: SvbonyCameraError.InvalidDirection,
        SVB_CAMERA_ERRORS.SVB_ERROR_UNKNOW_SENSOR_TYPE: SvbonyCameraError.UnknowSensorType,
        SVB_CAMERA_ERRORS.SVB_ERROR_END: SvbonyCameraError.ErrorEnd,
        SVB_CAMERA_ERRORS.SVB_PYINTERNAL_ERROR: SvbonyCameraError.PyInternalError
    }

    return codes.get(code, SvbonyCameraError.UnknownError)


def image_type_to_bpp(image_type):
    from pysvb.camera import SVB_IMG_TYPE

    types = {
        SVB_IMG_TYPE.SVB_IMG_RAW8: 8,
        SVB_IMG_TYPE.SVB_IMG_RAW10: 10,
        SVB_IMG_TYPE.SVB_IMG_RAW12: 12,
        SVB_IMG_TYPE.SVB_IMG_RAW14: 14,
        SVB_IMG_TYPE.SVB_IMG_RAW16: 16,
        SVB_IMG_TYPE.SVB_IMG_Y8: 8,
        SVB_IMG_TYPE.SVB_IMG_Y10: 10,
        SVB_IMG_TYPE.SVB_IMG_Y12: 12,
        SVB_IMG_TYPE.SVB_IMG_Y14: 14,
        SVB_IMG_TYPE.SVB_IMG_Y16: 16,
        SVB_IMG_TYPE.SVB_IMG_RGB24: 24,
        SVB_IMG_TYPE.SVB_IMG_RGB32: 32
    }

    return types[image_type]
