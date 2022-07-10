#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <SVBCameraSDK.h>

/*
 *
 * Python binding to SVBONY Cameras Driver
 * Copyright (c) 2022 Valerio Faiuolo
 *
 */

static PyObject *py_SVBGetNumOfConnectedCameras(PyObject *self, PyObject *args)
{
    int res = SVBGetNumOfConnectedCameras();

    /*This builds the answer back into a python object */
    return Py_BuildValue("i", res);
}

static PyObject *py_SVBGetCameraInfo(PyObject *self, PyObject *args)
{
    // Default values
    int err = -1, iCameraIndex = err;
    PyObject *ret_obj = Py_BuildValue("{s:s,s:s,s:s,s:i,s:i}",
        "FriendlyName", "", "CameraSN", "",
        "PortType", "", "DeviceID", 0,
        "CameraID", 0
    );

    if (PyArg_ParseTuple(args, "i", &iCameraIndex))
    {
        SVB_CAMERA_INFO info;
        err = SVBGetCameraInfo(&info, iCameraIndex);
        if (err ==  SVB_SUCCESS) {
            ret_obj = Py_BuildValue("{s:s,s:s,s:s,s:i,s:i}",
                "FriendlyName", info.FriendlyName, "CameraSN", info.CameraSN,
                "PortType", info.PortType, "DeviceID", info.DeviceID,
                "CameraID", info.CameraID
            );
        }
    }

    return Py_BuildValue("Oi", ret_obj, err);
}

static PyObject *py_SVBGetCameraProperty(PyObject *self, PyObject *args)
{
    // Default values
    int err = -1, iCameraID = err;
    PyObject *supportedBinsList = PyList_New(0);
    PyObject *supportedVideoFormatsList = PyList_New(0);
    PyObject *ret_obj = Py_BuildValue("{s:l,s:l,s:i,s:i,s:O,s:O,s:i,s:i}",
            "MaxHeight", 0, "MaxWidth", 0,
            "IsColorCam", 0, "BayerPattern", 0,
            "SupportedBins", supportedBinsList, "SupportedVideoFormat", supportedVideoFormatsList,
            "MaxBitDepth", 0, "IsTriggerCam", 0
    );


    if (PyArg_ParseTuple(args, "i", &iCameraID))
    {
        SVB_CAMERA_PROPERTY props;
        err = SVBGetCameraProperty(iCameraID, &props);

        // Supported bins
        // Supported video formats

        if (err ==  SVB_SUCCESS) {
            for (int i = 0; i < sizeof(props.SupportedBins)/sizeof(props.SupportedBins[0]); i++)
            {
                if (props.SupportedBins[i] == 0) break;
                PyList_Append(supportedBinsList, Py_BuildValue("i", props.SupportedBins[i]));
            }

            for (int i = 0; i < sizeof(props.SupportedVideoFormat) / sizeof(props.SupportedVideoFormat[0]); i++)
            {
                if (props.SupportedVideoFormat[i] == SVB_IMG_END) break;
                PyList_Append(supportedVideoFormatsList, Py_BuildValue("i", props.SupportedVideoFormat[i]));
            }

            ret_obj = Py_BuildValue("{s:l,s:l,s:i,s:i,s:O,s:O,s:i,s:i}",
                "MaxHeight", props.MaxHeight, "MaxWidth", props.MaxWidth,
                "IsColorCam", props.IsColorCam, "BayerPattern", props.BayerPattern,
                "SupportedBins", supportedBinsList, "SupportedVideoFormat", supportedVideoFormatsList,
                "MaxBitDepth", props.MaxBitDepth, "IsTriggerCam", props.IsTriggerCam
            );
        }
    }


    return Py_BuildValue("Oi", ret_obj, err);
}

static PyObject *py_SVBGetCameraPropertyEx(PyObject *self, PyObject *args)
{
    // Default values
    int err = -1, iCameraID = err;
    PyObject *ret_obj = Py_BuildValue("{s:i, s:i}",
                "bSupportPulseGuide", 0,
                "bSupportControlTemp", 0
    );

    if (PyArg_ParseTuple(args, "i", &iCameraID))
    {
        SVB_CAMERA_PROPERTY_EX prop_ex;
        err = SVBGetCameraPropertyEx(iCameraID, &prop_ex);
        if (err ==  SVB_SUCCESS) {
            ret_obj = Py_BuildValue("{s:i, s:i}",
                    "bSupportPulseGuide", prop_ex.bSupportPulseGuide,
                    "bSupportControlTemp", prop_ex.bSupportControlTemp
            );
        }
    }

    /*This builds the answer back into a python object */
    return Py_BuildValue("Oi", ret_obj, err);
}

static PyObject *py_SVBOpenCamera(PyObject *self, PyObject *args)
{
    int err = -1, iCameraID = err;

    if (PyArg_ParseTuple(args, "i", &iCameraID))
    {
        err = SVBOpenCamera(iCameraID);
    }

    return Py_BuildValue("i", err);
}

static PyObject *py_SVBCloseCamera(PyObject *self, PyObject *args)
{
    int err = -1, iCameraID = err;

    if (PyArg_ParseTuple(args, "i", &iCameraID))
    {
        err = SVBCloseCamera(iCameraID);
    }

    return Py_BuildValue("i", err);
}

static PyObject *py_SVBGetNumOfControls(PyObject *self, PyObject *args)
{
    int err = -1, iCameraID = err, numberOfControls = err;

    if (PyArg_ParseTuple(args, "i", &iCameraID))
    {
        err = SVBGetNumOfControls(iCameraID, &numberOfControls);
    }

    /*This builds the answer back into a python object */
    return Py_BuildValue("ii", numberOfControls, err);
}

static PyObject *py_SVBGetControlCaps(PyObject *self, PyObject *args)
{
    // Default values
    int err = -1, controlIndex = err, iCameraID = err;
    PyObject *ret_obj = Py_BuildValue("{s:s, s:s, s:l, s:l, s:l, s:i, s:i, s:i}",
                "Name", "", "Description", "",
                "MaxValue", 0, "MinValue", 0,
                "DefaultValue", 0, "IsAutoSupported", 0,
                "IsWritable", 0, "ControlType", 0);

    if (PyArg_ParseTuple(args, "ii", &iCameraID, &controlIndex))
    {
        SVB_CONTROL_CAPS ctrl_caps;
        err = SVBGetControlCaps(iCameraID, controlIndex, &ctrl_caps);

        if (err ==  SVB_SUCCESS) {
            ret_obj = Py_BuildValue("{s:s, s:s, s:l, s:l, s:l, s:i, s:i, s:i}",
                "Name", ctrl_caps.Name, "Description", ctrl_caps.Description,
                "MaxValue", ctrl_caps.MaxValue, "MinValue", ctrl_caps.MinValue,
                "DefaultValue", ctrl_caps.DefaultValue, "IsAutoSupported", ctrl_caps.IsAutoSupported,
                "IsWritable", ctrl_caps.IsWritable, "ControlType", ctrl_caps.ControlType);
        }
    }

    return Py_BuildValue("Oi", ret_obj, err);
}

static PyObject *py_SVBGetControlValue(PyObject *self, PyObject *args)
{
    int err = -1, controlType = err, iCameraID = err;
    SVB_BOOL pbauto = -1;
    long controlValue = -1;

    if (PyArg_ParseTuple(args, "ii", &iCameraID, &controlType))
    {
        err = SVBGetControlValue(iCameraID, controlType, &controlValue, &pbauto);
    }

    /*This builds the answer back into a python object */
    return Py_BuildValue("lii", controlValue, pbauto, err);
}

static PyObject *py_SVBSetControlValue(PyObject *self, PyObject *args)
{
    int err = -1, controlType = err, iCameraID = err;
    long controlValue = -1;
    SVB_BOOL pbauto = -1;

    if (PyArg_ParseTuple(args, "iili", &iCameraID, &controlType, &controlValue, &pbauto))
    {
        err = SVBSetControlValue(iCameraID, controlType, controlValue, pbauto);
    }

    /*This builds the answer back into a python object */
    return Py_BuildValue("i", err);
}

static PyObject *py_SVBGetOutputImageType(PyObject *self, PyObject *args)
{
    int err = -1, iCameraID = err;
    SVB_IMG_TYPE imageType = -1;

    if (PyArg_ParseTuple(args, "i", &iCameraID))
    {
        err = SVBGetOutputImageType(iCameraID, &imageType);
    }

    /*This builds the answer back into a python object */
    return Py_BuildValue("ii", imageType, err);
}

static PyObject *py_SVBSetOutputImageType(PyObject *self, PyObject *args)
{
    int err = -1, iCameraID = err;
    SVB_IMG_TYPE imageType = -1;

    if (PyArg_ParseTuple(args, "ii", &iCameraID, &imageType))
    {
        err = SVBSetOutputImageType(iCameraID, imageType);
    }

    /*This builds the answer back into a python object */
    return Py_BuildValue("i", err);
}

static PyObject *py_SVBSetROIFormat(PyObject *self, PyObject *args)
{
    int err = -1, iCameraID = err, iStartX = err, iStartY = err,
        iWidth = err, iHeight = err, iBin = err;

    if (PyArg_ParseTuple(args, "iiiiii", &iCameraID, &iStartX, &iStartY, &iWidth, &iHeight, &iBin))
    {
        err = SVBSetROIFormat(iCameraID, iStartX, iStartY, iWidth, iHeight, iBin);
    }

    /*This builds the answer back into a python object */
    return Py_BuildValue("i", err);
}

static PyObject *py_SVBGetROIFormat(PyObject *self, PyObject *args)
{
    int err = -1, iCameraID = err, iStartX = err, iStartY = err,
        iWidth = err, iHeight = err, iBin = err;

    if (PyArg_ParseTuple(args, "i", &iCameraID))
    {
        err = SVBGetROIFormat(iCameraID, &iStartX, &iStartY, &iWidth, &iHeight, &iBin);
    }

    return Py_BuildValue("iiiiii", iStartX, iStartY, iWidth, iHeight, iBin, err);
}

static PyObject *py_SVBGetDroppedFrames(PyObject *self, PyObject *args)
{
    int err = -1, iCameraID = err, piDropFrames = err;

    if (PyArg_ParseTuple(args, "i", &iCameraID))
    {
        err = SVBGetDroppedFrames(iCameraID, &piDropFrames);
    }

    return Py_BuildValue("ii", piDropFrames, err);
}

static PyObject *py_SVBStartVideoCapture(PyObject *self, PyObject *args)
{
    int err = -1, iCameraID = err;

    if (PyArg_ParseTuple(args, "i", &iCameraID))
    {
        err = SVBStartVideoCapture(iCameraID);
    }

    return Py_BuildValue("i", err);
}

static PyObject *py_SVBStopVideoCapture(PyObject *self, PyObject *args)
{
    int err = -1, iCameraID = err;

    if (PyArg_ParseTuple(args, "i", &iCameraID))
    {
        err = SVBStopVideoCapture(iCameraID);
    }

    return Py_BuildValue("i", err);
}

static PyObject *py_SVBGetVideoData(PyObject *self, PyObject *args)
{
    int err = -1, iCameraID = err, lBuffSize = 0, iWaitms = lBuffSize;

    if (!PyArg_ParseTuple(args, "iii", &iCameraID, &lBuffSize, &iWaitms))
    {
        return Py_BuildValue("y#i", NULL, sizeof(NULL), err);
    }

    unsigned char *pBuffer = malloc(lBuffSize * sizeof(unsigned char));
    err = SVBGetVideoData(iCameraID, pBuffer, lBuffSize, iWaitms);

    return Py_BuildValue("y#i", pBuffer, lBuffSize, err);
}

static PyObject *py_SVBWhiteBalanceOnce(PyObject *self, PyObject *args)
{
    int err = -1, iCameraID = err;

    if (PyArg_ParseTuple(args, "i", &iCameraID))
    {
        err = SVBWhiteBalanceOnce(iCameraID);
    }

    return Py_BuildValue("i", err);
}

static PyObject *py_SVBGetSDKVersion(PyObject *self, PyObject *args)
{
    const char *version = SVBGetSDKVersion();
    return Py_BuildValue("s", version);
}

static PyObject *py_SVBGetCameraSupportMode(PyObject *self, PyObject *args)
{
    int err = -1, iCameraID = err;
    PyObject *supportedModes = PyList_New(0);
    PyObject *ret_obj = Py_BuildValue("{s:O}", "SupportedCameraMode", supportedModes);

    if (PyArg_ParseTuple(args, "i", &iCameraID))
    {
        SVB_SUPPORTED_MODE modes;
        err = SVBGetCameraSupportMode(iCameraID, &modes);

        if (err ==  SVB_SUCCESS) {
            for (int i = 0; i < sizeof(modes.SupportedCameraMode)/sizeof(modes.SupportedCameraMode[0]); i++)
            {
                if (modes.SupportedCameraMode[i] == SVB_MODE_END) break;
                PyList_Append(supportedModes, Py_BuildValue("i", modes.SupportedCameraMode[i]));
            }
        }
    }


    return Py_BuildValue("Oi", ret_obj, err);
}

static PyObject *py_SVBGetCameraMode(PyObject *self, PyObject *args)
{
    int err = -1, iCameraID = err, mode = err;

    if (PyArg_ParseTuple(args, "i", &iCameraID))
    {
        err = SVBGetCameraMode(iCameraID, &mode);
    }

    return Py_BuildValue("ii", mode, err);
}

static PyObject *py_SVBSetCameraMode(PyObject *self, PyObject *args)
{
    int err = -1, iCameraID = err, mode = err;

    if (PyArg_ParseTuple(args, "ii", &iCameraID, &mode))
    {
        err = SVBSetCameraMode(iCameraID, mode);
    }

    return Py_BuildValue("i", err);
}

static PyObject *py_SVBSendSoftTrigger(PyObject *self, PyObject *args)
{
    int err = -1, iCameraID = err;

    if (PyArg_ParseTuple(args, "i", &iCameraID))
    {
        err = SVBSendSoftTrigger(iCameraID);
    }

    return Py_BuildValue("i", err);
}

static PyObject *py_SVBGetSerialNumber(PyObject *self, PyObject *args)
{
    int err = -1, iCameraID = err;
    PyObject *ret_obj = Py_BuildValue("{s:s}", "id", "");

    if (PyArg_ParseTuple(args, "i", &iCameraID))
    {
        SVB_SN sn;
        err = SVBGetSerialNumber(iCameraID, &sn);

        if(err == SVB_SUCCESS) {
            ret_obj = Py_BuildValue("{s:s}", "id", sn.id);
        }

    }

    return Py_BuildValue("Oi", ret_obj, err);
}

static PyObject *py_SVBSetTriggerOutputIOConf(PyObject *self, PyObject *args)
{
    int err = -1, iCameraID = err;
    SVB_BOOL bPinHigh = -1;
    SVB_TRIG_OUTPUT_PIN pin = -1;
    long lDelay = 0, lDuration = 0;

    if (PyArg_ParseTuple(args, "iiill", &iCameraID, &pin, &bPinHigh, &lDelay, &lDuration))
    {
        err = SVBSetTriggerOutputIOConf(iCameraID, pin, bPinHigh, lDelay, lDuration);
    }

    return Py_BuildValue("i", err);
}

static PyObject *py_SVBGetTriggerOutputIOConf(PyObject *self, PyObject *args)
{
    int err = -1, iCameraID = err;
    SVB_BOOL bPinHigh = -1;
    SVB_TRIG_OUTPUT_PIN pin = -1;
    long lDelay = 0, lDuration = 0;

    if (PyArg_ParseTuple(args, "ii", &iCameraID, &pin))
    {
        err = SVBGetTriggerOutputIOConf(iCameraID, pin, &bPinHigh, &lDelay, &lDuration);
    }

    return Py_BuildValue("illi", bPinHigh, lDelay, lDuration, err);
}

static PyObject *py_SVBPulseGuide(PyObject *self, PyObject *args)
{
    int err = -1, iCameraID = err, duration = 0;
    SVB_GUIDE_DIRECTION direction = -1;

    if (PyArg_ParseTuple(args, "iii", &iCameraID, &direction, &duration))
    {
        err = SVBPulseGuide(iCameraID, direction, duration);
    }

    return Py_BuildValue("i", err);
}

static PyObject *py_SVBGetSensorPixelSize(PyObject *self, PyObject *args)
{
    int err = -1, iCameraID = err;
    float fPixelSize = 0.0;

    if (PyArg_ParseTuple(args, "i", &iCameraID))
    {
        err = SVBGetSensorPixelSize(iCameraID, &fPixelSize);
    }

    return Py_BuildValue("fi", fPixelSize, err);
}

static PyObject *py_SVBCanPulseGuide(PyObject *self, PyObject *args)
{
    int err = -1, iCameraID = err;
    SVB_BOOL CanPulseGuide = 0;

    if (PyArg_ParseTuple(args, "i", &iCameraID))
    {
        err = SVBCanPulseGuide(iCameraID, &CanPulseGuide);
    }

    return Py_BuildValue("ii", CanPulseGuide, err);
}

static PyObject *py_SVBSetAutoSaveParam(PyObject *self, PyObject *args)
{
    int err = -1, iCameraID = err;
    SVB_BOOL enable = 0;

    if (PyArg_ParseTuple(args, "ii", &iCameraID, &enable))
    {
        err = SVBSetAutoSaveParam(iCameraID, enable);
    }

    return Py_BuildValue("i", err);
}

/*
 * This tells Python what methods this module has.
 * See the Python-C API for more information.
 */
static PyMethodDef SVBCameraSdkMethods[] = {
    {"SVBGetNumOfConnectedCameras",
     py_SVBGetNumOfConnectedCameras,
     METH_NOARGS, NULL},
    {"SVBGetCameraInfo",
     py_SVBGetCameraInfo,
     METH_VARARGS, NULL},
    {"SVBGetCameraProperty",
     py_SVBGetCameraProperty,
     METH_VARARGS, NULL},
    {"SVBGetCameraPropertyEx",
     py_SVBGetCameraPropertyEx,
     METH_VARARGS, NULL},
    {"SVBOpenCamera",
     py_SVBOpenCamera,
     METH_VARARGS, NULL},
    {"SVBCloseCamera",
     py_SVBCloseCamera,
     METH_VARARGS, NULL},
    {"SVBGetNumOfControls",
     py_SVBGetNumOfControls,
     METH_VARARGS, NULL},
    {"SVBGetControlCaps",
     py_SVBGetControlCaps,
     METH_VARARGS, NULL},
    {"SVBGetControlValue",
     py_SVBGetControlValue,
     METH_VARARGS, NULL},
    {"SVBSetControlValue",
     py_SVBSetControlValue,
     METH_VARARGS, NULL},
    {"SVBGetOutputImageType",
     py_SVBGetOutputImageType,
     METH_VARARGS, NULL},
    {"SVBSetOutputImageType",
     py_SVBSetOutputImageType,
     METH_VARARGS, NULL},
    {"SVBSetROIFormat",
     py_SVBSetROIFormat,
     METH_VARARGS, NULL},
    {"SVBGetROIFormat",
     py_SVBGetROIFormat,
     METH_VARARGS, NULL},
    {"SVBGetDroppedFrames",
     py_SVBGetDroppedFrames,
     METH_VARARGS, NULL},
    {"SVBStartVideoCapture",
     py_SVBStartVideoCapture,
     METH_VARARGS, NULL},
    {"SVBStopVideoCapture",
     py_SVBStopVideoCapture,
     METH_VARARGS, NULL},
    {"SVBGetVideoData",
     py_SVBGetVideoData,
     METH_VARARGS, NULL},
    {"SVBWhiteBalanceOnce",
     py_SVBWhiteBalanceOnce,
     METH_VARARGS, NULL},
    {"SVBGetSDKVersion",
     py_SVBGetSDKVersion,
     METH_NOARGS, NULL},
    {"SVBGetCameraSupportMode",
     py_SVBGetCameraSupportMode,
     METH_VARARGS, NULL},
    {"SVBGetCameraMode",
     py_SVBGetCameraMode,
     METH_VARARGS, NULL},
    {"SVBSetCameraMode",
     py_SVBSetCameraMode,
     METH_VARARGS, NULL},
    {"SVBSendSoftTrigger",
     py_SVBSendSoftTrigger,
     METH_VARARGS, NULL},
    {"SVBGetSerialNumber",
     py_SVBGetSerialNumber,
     METH_VARARGS, NULL},
    {"SVBSetTriggerOutputIOConf",
     py_SVBSetTriggerOutputIOConf,
     METH_VARARGS, NULL},
    {"SVBGetTriggerOutputIOConf",
     py_SVBGetTriggerOutputIOConf,
     METH_VARARGS, NULL},
    {"SVBPulseGuide",
     py_SVBPulseGuide,
     METH_VARARGS, NULL},
    {"SVBGetSensorPixelSize",
     py_SVBGetSensorPixelSize,
     METH_VARARGS, NULL},
    {"SVBCanPulseGuide",
     py_SVBCanPulseGuide,
     METH_VARARGS, NULL},
    {"SVBSetAutoSaveParam",
     py_SVBSetAutoSaveParam,
     METH_VARARGS, NULL},
    {NULL, NULL, 0, NULL}};

/* This initiates the module using the above definitions. */
static struct PyModuleDef moduledef = {
    PyModuleDef_HEAD_INIT,
    "svbcamerasdk",
    NULL,
    -1,
    SVBCameraSdkMethods,
    NULL,
    NULL,
    NULL,
    NULL};

PyMODINIT_FUNC PyInit_svbcamerasdk(void)
{
    PyObject *m;
    m = PyModule_Create(&moduledef);
    if (!m)
    {
        return NULL;
    }
    return m;
}