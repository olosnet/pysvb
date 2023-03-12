#
# Python binding to SVBONY Cameras Driver
# Copyright (c) 2022 Valerio Faiuolo
#
# Main camera class and types
#

from dataclasses import dataclass
from enum import IntEnum, auto
from pysvb import svbcamerasdk

from pysvb.errors import SVB_CAMERA_ERRORS
from pysvb.helpers import SVB_ERROR_CODE_TO_EXC

SVBCAMERA_ID_MAX = 128


class SVB_BAYER_PATTERN(IntEnum):
    SVB_BAYER_RG = 0
    SVB_BAYER_BG = auto()
    SVB_BAYER_GR = auto()
    SVB_BAYER_GB = auto()

# Supported video format


class SVB_IMG_TYPE(IntEnum):
    SVB_IMG_RAW8 = 0
    SVB_IMG_RAW10 = auto()
    SVB_IMG_RAW12 = auto()
    SVB_IMG_RAW14 = auto()
    SVB_IMG_RAW16 = auto()
    SVB_IMG_Y8 = auto()
    SVB_IMG_Y10 = auto()
    SVB_IMG_Y12 = auto()
    SVB_IMG_Y14 = auto()
    SVB_IMG_Y16 = auto()
    SVB_IMG_RGB24 = auto()
    SVB_IMG_RGB32 = auto()

# Guider direction


class SVB_GUIDE_DIRECTION(IntEnum):
    SVB_GUIDE_NORTH = 0
    SVB_GUIDE_SOUTH = auto()
    SVB_GUIDE_EAST = auto()
    SVB_GUIDE_WEST = auto()


class SVB_FLIP_STATUS(IntEnum):
    SVB_FLIP_NONE = 0
    """Original"""
    SVB_FLIP_HORIZ = auto()
    """Horizontal flip"""
    SVB_FLIP_VERT = auto()
    """Verical flip"""
    SVB_FLIP_BOTH = auto()
    """Both horizontal and vertical flip"""


class SVB_CAMERA_MODE(IntEnum):
    SVB_MODE_NORMAL = 0
    SVB_MODE_TRIG_SOFT = auto()
    SVB_MODE_TRIG_RISE_EDGE = auto()
    SVB_MODE_TRIG_FALL_EDGE = auto()
    SVB_MODE_TRIG_DOUBLE_EDGE = auto()
    SVB_MODE_TRIG_HIGH_LEVEL = auto()
    SVB_MODE_TRIG_LOW_LEVEL = auto()


class SVB_TRIG_OUTPUT(IntEnum):
    SVB_TRIG_OUTPUT_PINA = 0  # Only Pin A output
    SVB_TRIG_OUTPUT_PINB = auto()  # Only Pin B output
    SVB_TRIG_OUTPUT_NONE = -1

# Control type


class SVB_CONTROL_TYPE(IntEnum):
    SVB_GAIN = 0
    SVB_EXPOSURE = auto()
    SVB_GAMMA = auto()
    SVB_GAMMA_CONTRAST = auto()
    SVB_WB_R = auto()
    SVB_WB_G = auto()
    SVB_WB_B = auto()
    SVB_FLIP = auto()
    """Reference: SVB_FLIP_STATUS"""
    SVB_FRAME_SPEED_MODE = auto()
    """Frame speed: 0:low_speed, 1:medium_speed, 2:high_speed"""
    SVB_CONTRAST = auto()
    SVB_SHARPNESS = auto()
    SVB_SATURATION = auto()
    SVB_AUTO_TARGET_BRIGHTNESS = auto()
    SVB_BLACK_LEVEL = auto()
    """Black level offset"""
    SVB_COOLER_ENABLE = auto()
    """Cooler enable, 0:disable - 1:enable"""
    SVB_TARGET_TEMPERATURE = auto()
    """Target temperature, unit is 0.1C"""
    SVB_CURRENT_TEMPERATURE = auto()
    """Current temperature, unit is 0.1C"""
    SVB_COOLER_POWER = auto()
    """Cooler power, range: 0-100"""
    SVB_BAD_PIXEL_CORRECTION_ENABLE = auto()
    """Enable or disable bad pixel correction"""

# Not implemented?


class SVB_EXPOSURE_STATUS(IntEnum):
    SVB_EXP_IDLE = 0
    """idle states, you can start exposure now"""
    SVB_EXP_WORKING = auto()
    """exposing"""
    SVB_EXP_SUCCESS = auto()
    """exposure finished and waiting for download"""
    SVB_EXP_FAILED = auto()
    """exposure failed, you need to start exposure again"""


class SVB_CAMERA_INFO:

    @property
    def FriendlyName(self) -> str:
        """Camera friendly name"""
        return self.__b["FriendlyName"]

    @property
    def CameraSN(self) -> str:
        """Camera serial number"""
        return self.__b["CameraSN"]

    @property
    def PortType(self) -> str:
        """Camera port type"""
        return self.__b["PortType"]

    @property
    def DeviceID(self) -> int:
        """Camera device ID"""
        return self.__b["DeviceID"]

    @property
    def CameraID(self) -> int:
        """Camera ID"""
        return self.__b["CameraID"]

    def __init__(self, b) -> None:
        self.__b = b


class SVB_CAMERA_PROPERTY:

    @property
    def MaxHeight(self) -> int:
        """the max height of the camera"""
        return self.__b["MaxHeight"]

    @property
    def MaxWidth(self) -> int:
        """the max width of the camera"""
        return self.__b["MaxWidth"]

    @property
    def IsColorCam(self) -> bool:
        """is camera color"""
        return bool(self.__b["BayerPattern"] != 0)

    @property
    def BayerPattern(self) -> SVB_BAYER_PATTERN:
        """camera bayern pattern"""
        return SVB_BAYER_PATTERN(self.__b["BayerPattern"])

    @property
    def SupportedBins(self) -> 'list[int]':
        """list of supported binning methods"""
        return self.__b["SupportedBins"]

    @property
    def SupportedVideoFormat(self) -> 'list[SVB_IMG_TYPE]':
        """list of supported video formats"""
        return [SVB_IMG_TYPE(el) for el in self.__b["SupportedVideoFormat"]]

    @property
    def MaxBitDepth(self) -> int:
        return self.__b["MaxBitDepth"]

    @property
    def IsTriggerCam(self) -> bool:
        return bool(self.__b["IsTriggerCam"] != 0)

    def __init__(self, b) -> None:
        self.__b = b


class SVB_CAMERA_PROPERTY_EX:

    @property
    def bSupportPulseGuide(self) -> bool:
        """Support pulse guide"""
        return bool(self.__b["bSupportPulseGuide"])

    @property
    def bSupportControlTemp(self) -> bool:
        """Support control temp"""
        return bool(self.__b["bSupportControlTemp"])

    def __init__(self, b) -> None:
        self.__b = b


class SVB_CONTROL_CAPS:

    @property
    def Name(self) -> str:
        """Control name"""
        return self.__b["Name"]

    @property
    def Description(self) -> str:
        """Control description"""
        return self.__b["Description"]

    @property
    def MaxValue(self) -> int:
        """Control max value"""
        return self.__b["MaxValue"]

    @property
    def MinValue(self) -> int:
        """Control min value"""
        return self.__b["MinValue"]

    @property
    def DefaultValue(self) -> int:
        """Control default value"""
        return self.__b["DefaultValue"]

    @property
    def IsAutoSupported(self) -> bool:
        """Support auto set"""
        return bool(self.__b["IsAutoSupported"] != 0)

    @property
    def IsWritable(self) -> bool:
        """Control is writable"""
        return bool(self.__b["IsWritable"] != 0)

    @property
    def ControlType(self) -> SVB_CONTROL_TYPE:
        """Control type, used to get value and set value of the control"""
        return SVB_CONTROL_TYPE(self.__b["ControlType"])

    def __init__(self, b) -> None:
        self.__b = b


class SVB_SUPPORTED_MODE:

    @property
    def SupportedCameraMode(self) -> 'list[SVB_CAMERA_MODE]':
        """This list will content with the support camera mode types"""
        return [SVB_CAMERA_MODE(el) for el in self.__b["SupportedCameraMode"]]

    def __init__(self, b) -> None:
        self.__b = b


class SVB_ID:

    @property
    def id(self) -> str:
        """Camera serial number"""
        return self.__b['id']

    def __init__(self, b) -> None:
        self.__b = b


@dataclass
class SVB_ROI_FORMAT:
    """Roi format dataclass"""
    start_x: int = -1
    "roi area start X"
    start_y: int = -1
    "roi area start Y"
    width: int = -1
    "the width of the ROI area. Make sure width%8 = 0"
    height: int = -1
    "the height of the ROI area. Make sure height%2 = 0 further, for USB2.0 camera SVB120, please make sure that width*height%1024=0"
    bin: int = -1
    "binning method. bin1=1, bin2=2"


@dataclass
class SVB_TRIGGER_OUTPUT_IO_CONF:
    pin_high: bool = False
    delay: int = 0
    duration: int = 0

@dataclass
class SVB_CAMERA_UPGRADE_STATUS:
    """Camera firmware update status dataclass"""
    needed: bool = False
    "Upgrade needed"
    min_version: str = ""
    "Required firmware min version"""


class PySVBCameraSDK:

    def __init__(self, raise_exc=True) -> None:
        """Initialize class

        Args:
            raise_exc (bool, optional): Enable raise of exceptions. Defaults to True.
        """
        self.__last_error_code_p = SVB_CAMERA_ERRORS.SVB_SUCCESS
        self.__raise_exc = raise_exc

    @property
    def __last_error_code(self) -> SVB_CAMERA_ERRORS:
        return self.__last_error_code_p

    @__last_error_code.setter
    def __last_error_code(self, value: int) -> None:
        self.__last_error_code_p = value
        if self.__raise_exc and value != SVB_CAMERA_ERRORS.SVB_SUCCESS:
            raise SVB_ERROR_CODE_TO_EXC(value)

    @property
    def last_error_code(self) -> SVB_CAMERA_ERRORS:
        """Last error code"""
        return self.__last_error_code

    @property
    def last_error_code_str(self) -> str:
        """Last error string"""
        return SVB_CAMERA_ERRORS(self.__last_error_code).name

    @property
    def sdk_version(self) -> str:
        """Get sdk version string.

        Returns:
            str: version string
        """
        return svbcamerasdk.SVBGetSDKVersion()

    def get_num_of_connected_cameras(self) -> int:
        """This should be the first API to be called get number of connected SVB cameras.


        Returns:
            int: number of connected SVB cameras. 1 means 1 camera connected.
        """

        return svbcamerasdk.SVBGetNumOfConnectedCameras()

    def get_camera_info(self, camera_index: int) -> SVB_CAMERA_INFO:
        """Get the information of the connected cameras, you can do this without open the camera.

        Args:
            camera_index (int): 0 means the first connect camera, 1 means the second connect camera, etc

        Returns:
            SVB_CAMERA_INFO: structure containing the information of camera
        """

        binfo, err = svbcamerasdk.SVBGetCameraInfo(camera_index)
        self.__last_error_code = err
        return SVB_CAMERA_INFO(binfo)

    def get_camera_property(self, camera_id: int) -> SVB_CAMERA_PROPERTY:
        """Get the properties of the connected cameras.

        Args:
            camera_id (int): this is get from the camera info (use get_camera_info)

        Returns:
            SVB_CAMERA_PROPERTY: structure containing the properties of camera
        """
        binfo, err = svbcamerasdk.SVBGetCameraProperty(camera_id)
        self.__last_error_code = err
        return SVB_CAMERA_PROPERTY(binfo)

    def get_camera_property_ex(self, camera_id: int) -> SVB_CAMERA_PROPERTY_EX:
        """Get the extra properties of the connected cameras.

        Args:
            camera_id (int): this is get from the camera info (use get_camera_info)

        Returns:
            SVB_CAMERA_PROPERTY_EX: structure containing the extra properties of camera
        """
        binfo, err = svbcamerasdk.SVBGetCameraPropertyEx(camera_id)
        self.__last_error_code = err
        return SVB_CAMERA_PROPERTY_EX(binfo)

    def open_camera(self, camera_id: int) -> None:
        """Open the camera before any operation to the camera, this will not affect the camera which is capturing.

        Args:
            camera_id (int): this is get from the camera info (use get_camera_info)
        """
        err = svbcamerasdk.SVBOpenCamera(camera_id)
        self.__last_error_code = err

    def close_camera(self, camera_id: int) -> None:
        """You need to close the camera to free all the resource.

        Args:
            camera_id (int): this is get from the camera info (use get_camera_info)
        """
        err = svbcamerasdk.SVBCloseCamera(camera_id)
        self.__last_error_code = err

    def get_num_of_controls(self, camera_id: int) -> int:
        """Get number of controls available for this camera. The camera need be opened at first.

        Args:
            camera_id (int): this is get from the camera info (use get_camera_info)

        Returns:
            int: number of controls
        """
        res, err = svbcamerasdk.SVBGetNumOfControls(camera_id)
        self.__last_error_code = err
        return res

    def get_control_caps(self, camera_id: int, control_index: int) -> SVB_CONTROL_CAPS:
        """Get controls property available for this camera. The camera need be opened at first.

        Args:
            camera_id (int): this is get from the camera info (use get_camera_info)
            control_index (int): index of control, NOT control type

        Returns:
            SVB_CONTROL_CAPS: structure containing the property of the control
        """
        res, err = svbcamerasdk.SVBGetControlCaps(camera_id, control_index)
        self.__last_error_code = err
        return SVB_CONTROL_CAPS(res)

    def get_control_value(self, camera_id: int, control_type: SVB_CONTROL_TYPE) -> 'tuple[int, bool]':
        """Get controls property value and auto value. Note: the value of the temperature is the float value * 10 to convert it to long type,
           control name is "Temperature" because long is the only type for control(except cooler's target temperature, because it is an integer).
           The camera need be opened at first.

        Args:
            camera_id (int): this is get from the camera info (use get_camera_info)
            control_type (SVB_CONTROL_TYPE): this is get from control property (use get_control_caps)

        Returns:
            Tuple[int, bool]: property value, auto value
        """
        res, auto, err = svbcamerasdk.SVBGetControlValue(
            camera_id, control_type)
        self.__last_error_code = err
        return res, bool(auto != 0)

    def set_control_value(self, camera_id: int, control_type: SVB_CONTROL_TYPE, control_value: int, b_auto: bool) -> None:
        """Set controls property value and auto value. The camera need be opened at first.

        Args:
            camera_id (int): this is get from the camera info (use get_camera_info)
            control_type (SVB_CONTROL_TYPE): this is get from control property (use get_control_caps)
            control_value (int): the value set to the control
            b_auto (bool): set the control auto
        """
        b_auto_i = int(b_auto == True)
        err = svbcamerasdk.SVBSetControlValue(
            camera_id, control_type, control_value, b_auto_i)
        self.__last_error_code = err

    def get_output_image_type(self, camera_id: int) -> SVB_IMG_TYPE:
        """Get the output image type. The camera need be opened at first.

        Args:
            camera_id (int): this is get from the camera info (use get_camera_info)

        Returns:
            SVB_IMG_TYPE: current image type
        """
        img_type, err = svbcamerasdk.SVBGetOutputImageType(camera_id)
        self.__last_error_code = err
        return SVB_IMG_TYPE(img_type)

    def set_output_image_type(self, camera_id: int, type: SVB_IMG_TYPE) -> None:
        """Set the output image type, the value set must be the type supported by the SVBGetCameraProperty function. The camera need be opened at first.


        Args:
            camera_id (int): this is get from the camera info (use get_camera_info)
            type (SVB_IMG_TYPE): image type
        """
        err = svbcamerasdk.SVBSetOutputImageType(camera_id, type)
        self.__last_error_code = err

    def set_roi_format(self, camera_id: int, roi_format: SVB_ROI_FORMAT) -> None:
        """Set the ROI area before capture. You must stop capture before call it.
            The width and height is the value after binning. The camera need be opened at first.
            ie. you need to set width to 640 and height to 480 if you want to run at 640X480@BIN2
            SVB120's data size must be times of 1024 which means width*height%1024=0.

        Args:
            camera_id (int): this is get from the camera info (use get_camera_info)
            roi_format (SVB_ROI_FORMAT): roi format paramas dataclass to be set
        """
        err = svbcamerasdk.SVBSetROIFormat(
            camera_id, roi_format.start_x, roi_format.start_y,
            roi_format.width, roi_format.height, roi_format.bin)
        self.__last_error_code = err

    def get_roi_format(self, camera_id: int) -> SVB_ROI_FORMAT:
        """Get the current ROI area setting. The camera need be opened at first.

        Args:
            camera_id (int): this is get from the camera info (use get_camera_info)

        Returns:
            SVB_ROI_FORMAT: roi format paramas dataclass
        """
        start_x, start_y,\
            width, height, bin, err = svbcamerasdk.SVBGetROIFormat(camera_id)
        self.__last_error_code = err
        return SVB_ROI_FORMAT(start_x, start_y, width, height, bin)

    def get_dropped_frames(self, camera_id: int) -> int:
        """Get dropped frames number. The camera need be opened at first.
           Drop frames happen when USB is traffic or harddisk write speed is slow it will reset to 0 after stop capture.


        Args:
            camera_id (int): this is get from the camera info (use get_camera_info)

        Returns:
            int: dropped frames
        """
        df, err = svbcamerasdk.SVBGetDroppedFrames(camera_id)
        self.__last_error_code = err
        return df

    def start_video_capture(self, camera_id: int) -> None:
        """Start video capture, then you can get the data from get_video_data.
            The camera need be opened at first.

        Args:
            camera_id (int): this is get from the camera info (use get_camera_info)
        """
        err = svbcamerasdk.SVBStartVideoCapture(camera_id)
        self.__last_error_code = err

    def stop_video_capture(self, camera_id: int):
        """Stop video capture

        Args:
            camera_id (int): this is get from the camera info (use get_camera_info)
        """
        err = svbcamerasdk.SVBStopVideoCapture(camera_id)
        self.__last_error_code = err

    def get_video_data(self, camera_id: int, buff_size: int, wait_ms: int) -> bytes:
        """Get data from the video buffer. The buffer is very small, you need to call this API as fast as possible,
            otherwise frame will be discarded so the best way is maintain one buffer loop and call this API in a loop.
            Please make sure the buffer size is biger enough to hold one image otherwise the this API will crash.
            This API will block and wait wait_ms to get one image the unit is ms -1 means wait forever.
            The camera need be opened at first.


        Args:
            camera_id (int): this is get from the camera info (use get_camera_info)
            buff_size (int): buffer size (bytes) to allocate (8bit mono:width*height, 16bit mono:width*height*2, RGB24:width*height*3)
            wait_ms (int): wait value (milliseconds), this value is recommend set to exposure*2+500ms

        Returns:
            bytes: buffer data
        """
        data, err = svbcamerasdk.SVBGetVideoData(camera_id, buff_size, wait_ms)
        self.__last_error_code = err
        return data

    def white_balance_once(self, camera_id: int) -> None:
        """White balance once time. If success, please get SVB_WB_R, SVB_WB_G and SVB_WB_B values to update UI display.
            The camera need be opened at first.


        Args:
            camera_id (int): this is get from the camera info (use get_camera_info)
        """
        err = svbcamerasdk.SVBWhiteBalanceOnce(camera_id)
        self.__last_error_code = err

    def get_camera_firmware_version(self, camera_id, buff_size=64) -> str:
        """Gets the camera firmware version number

        Args:
            camera_id (int): this is get from the camera info (use get_camera_info)
            buff_size (int): buffer size, form firmware version string, which needs to be at least 64 bytes in size (default)
        """

        data, err = svbcamerasdk.SVBGetCameraFirmwareVersion(
            camera_id, buff_size)
        self.__last_error_code = err
        return str(data).strip()

    def get_camera_support_mode(self, camera_id: int) -> SVB_SUPPORTED_MODE:
        """Get the camera supported mode, only need to call when the IsTriggerCam in the CameraInfo is true.
            The camera need be opened at first.


        Args:
            camera_id (int): this is get from the camera info (use get_camera_info)

        Returns:
            SVB_SUPPORTED_MODE: the camera supported mode
        """
        modes, err = svbcamerasdk.SVBGetCameraSupportMode(camera_id)
        self.__last_error_code = err
        return SVB_SUPPORTED_MODE(modes)

    def get_camera_mode(self, camera_id: int) -> SVB_CAMERA_MODE:
        """Get the camera current mode, only need to call when the IsTriggerCam in the CameraInfo is true
            The camera need be opened at first.


        Args:
            camera_id (int): this is get from the camera info (use get_camera_info)

        Returns:
            SVB_CAMERA_MODE: the current camera mode
        """
        mode, err = svbcamerasdk.SVBGetCameraMode(camera_id)
        self.__last_error_code = err
        return SVB_CAMERA_MODE(mode)

    def set_camera_mode(self, camera_id: int, mode: SVB_CAMERA_MODE) -> None:
        """Set the camera mode, only need to call when the IsTriggerCam in the CameraInfo is true.
            The camera need be opened at first.

        Args:
            camera_id (int): this is get from the camera info (use get_camera_info)
            mode (SVB_CAMERA_MODE): this is get from the camera property (use get_camera_property)
        """
        err = svbcamerasdk.SVBSetCameraMode(camera_id, mode)
        self.__last_error_code = err

    def send_soft_trigger(self, camera_id: int) -> None:
        """Send out a softTrigger. For edge trigger, it only need to set true which means send a
            rising trigger to start exposure. For level trigger, it need to set true first means
            start exposure, and set false means stop exposure. It only need to call when the
            IsTriggerCam in the CameraInfo is true.
            The camera need be opened at first.

        Args:
            camera_id (int): this is get from the camera info (use get_camera_info)
        """
        err = svbcamerasdk.SVBSendSoftTrigger(camera_id)
        self.__last_error_code = err

    def get_serial_number(self, camera_id: int) -> SVB_ID:
        """Get a serial number from a camera. The camera need be opened at first.

        Args:
            camera_id (int): this is get from the camera info (use get_camera_info)

        Returns:
            SVB_ID: SVB_ID structure
        """
        sn, err = svbcamerasdk.SVBGetSerialNumber(camera_id)
        self.__last_error_code = err
        return SVB_ID(sn)

    def set_trigger_output_io_conf(self, camera_id: int, pin: SVB_TRIG_OUTPUT, trigger_conf: SVB_TRIGGER_OUTPUT_IO_CONF) -> None:
        """Config the output pin (A or B) of Trigger port. If duration <= 0, this output pin will be closed.
            Only need to call when the IsTriggerCam in the CameraInfo is true.
            The camera need be opened at first.


        Args:
            camera_id (int): this is get from the camera info (use get_camera_info)
            pin (SVB_TRIG_OUTPUT) : select the pin for output
            trigger_conf (SVB_TRIGGER_OUTPUT_IO_CONF): trigger configuration dataclass
        """
        err = svbcamerasdk.SVBSetTriggerOutputIOConf(camera_id, pin,
                                                     int(trigger_conf.pin_high == True), trigger_conf.delay, trigger_conf.duration)
        self.__last_error_code = err

    def get_trigger_output_io_conf(self, camera_id: int, pin: SVB_TRIG_OUTPUT) -> SVB_TRIGGER_OUTPUT_IO_CONF:
        """ Get the output pin configuration, only need to call when the IsTriggerCam in the CameraInfo is true.
            The camera need be opened at first.

        Args:
            camera_id (int): this is get from the camera info (use get_camera_info)
            pin (SVB_TRIG_OUTPUT) : select the pin for getting the configuration
        Returns:
            SVB_TRIGGER_OUTPUT_IO_CONF: trigger configuration dataclass
        """

        pin_high, delay, duration, err = svbcamerasdk.SVBGetTriggerOutputIOConf(
            camera_id, pin)
        self.__last_error_code = err
        return SVB_TRIGGER_OUTPUT_IO_CONF(bool(pin_high != 0), delay, duration)

    def pulse_guide(self, camera_id: int, direction: SVB_GUIDE_DIRECTION, duration: int) -> None:
        """ Send a PulseGuide command to camera to control the telescope.
            The camera need be opened at first.

        Args:
            camera_id (int): this is get from the camera info (use get_camera_info)
            direction (SVB_GUIDE_DIRECTION): the direction
            duration (int): duration of pulse in missilseconds
        """

        err = svbcamerasdk.SVBPulseGuide(camera_id, direction, duration)
        self.__last_error_code = err

    def get_sensor_pixel_size(self, camera_id: int) -> float:
        """Get sensor pixel size in microns.
           The camera need be opened at first.
        Args:
            camera_id (int): this is get from the camera info (use get_camera_info)

        Returns:
            float: pixel size in microns
        """
        size, err = svbcamerasdk.SVBGetSensorPixelSize(camera_id)
        self.__last_error_code = err
        return size

    def can_pulse_guide(self, camera_id: int) -> bool:
        """Get whether to support pulse guide.
           The camera need be opened at first.


        Args:
            camera_id (int): this is get from the camera info (use get_camera_info)

        Returns:
            bool: if True then support pulse guide
        """
        can, err = svbcamerasdk.SVBCanPulseGuide(camera_id)
        self.__last_error_code = err
        return bool(can != 0)

    def set_autosave_param(self, camera_id: int, enable: bool) -> None:
        """Whether to save the parameter file automatically

        Args:
            camera_id (int): this is get from the camera info (use get_camera_info)
            enable (bool): if True then save the parameter file automatically
        """
        err = svbcamerasdk.SVBSetAutoSaveParam(camera_id, int(enable == True))
        self.__last_error_code = err

    def is_camera_need_to_upgrade(self, camera_id: int, buff_size=64) -> SVB_CAMERA_UPGRADE_STATUS:
        """Detect if the camera firmware needs to be upgraded

        Args:
            camera_id (int): this is get from the camera info (use get_camera_info)
            buff_size (int): buffer size, for min firmware version string, which needs to be at least 64 bytes in size (default)
        """
        needed, min_version, err = svbcamerasdk.SVBIsCameraNeedToUpgrade(camera_id, buff_size)
        self.__last_error_code = err
        return SVB_CAMERA_UPGRADE_STATUS(bool(needed != 0), str(min_version).strip())
    

    def restore_default_param(self, camera_id: int) -> None:
        """Restore default parameters

        Args:
            camera_id (int): this is get from the camera info (use get_camera_info)
        """
        err = svbcamerasdk.SVBRestoreDefaultParam(camera_id)
        self.__last_error_code = err