# pysvb

pysvb is a python binding that allows you to use the SVBONY camera SDK directly in your python software

## Quickstart

### Install via pip from git

`pip install git+https://github.com/olosnet/pysvb.git`

### Import in your python project

```python  
from pysvb.camera import PySVBCameraSDK 
```

### Example: obtain SDK version and connected camera info

```python 
from pysvb.camera import PySVBCameraSDK 

camera_sdk = PySVBCameraSDK()

connected = camera_sdk.get_num_of_connected_cameras()
print("SDK VERSION:", camera_sdk.sdk_version)
print("Connected camera(s): {}".format(connected) )
camera_id = -1

if connected > 0:
    for i in range(0, connected):
        info = camera_sdk.get_camera_info(i)
        print("Friendly name:", info.FriendlyName)
        print("Port type:", info.PortType)
        print("Serial number",info.CameraSN)
        print("Device ID:", hex(info.DeviceID))
        print("Camera ID:", info.CameraID)
        camera_id = info.CameraID 
```

you can find more examples in the project's demos directory

## Documentation
you can find the module documentation at this url: https://olosnet.github.io/pysvb/ or in the docs directory of the project

## SDK Info
The SDK included in the module is owned by SVBONY, you can download it at this address: https://www.svbony.com/Support/SoftWare-Driver