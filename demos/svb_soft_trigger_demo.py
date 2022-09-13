#!/usr/bin/env python3

from datetime import datetime
from time import sleep
from pysvb.camera import SVB_CAMERA_MODE, SVB_CONTROL_TYPE, SVB_IMG_TYPE, PySVBCameraSDK, SVB_ROI_FORMAT
from pysvb.errors import SvbonyCameraError
from threading import Thread

def capture_func(camera_sdk, camera_id, buffer_size, data):
    camera_sdk.send_soft_trigger(camera_id)

    while(True):
        sleep(0.1)
        try:
            data = camera_sdk.get_video_data(camera_id, buffer_size, 100)
        except SvbonyCameraError.Timeout:
            pass
        except Exception as e:
            print("Error: ", str(e))
            break
        else:
            break

    return data

if __name__ == "__main__":

    camera_sdk = PySVBCameraSDK()

    connected = camera_sdk.get_num_of_connected_cameras()
    print("SDK VERSION:", camera_sdk.sdk_version)
    print("Connected camera(s): {}".format(connected) )
    camera_id = -1

    if connected > 0:
        for i in range(0, connected):
            print("\n---------------------------------------------------\n")
            info = camera_sdk.get_camera_info(i)
            print("Friendly name:", info.FriendlyName)
            print("Port type:", info.PortType)
            print("Serial number",info.CameraSN)
            print("Device ID:", hex(info.DeviceID))
            print("Camera ID:", info.CameraID)
            camera_id = info.CameraID
            print("\n---------------------------------------------------\n")

        print("Open latest camera...")
        sleep(1)
        camera_sdk.open_camera(camera_id)

        print("\n---------------------------------------------------\n")
        # Camera properties
        props = camera_sdk.get_camera_property(camera_id)
        print("Camera properties:")
        print("\tmaximum width:", props.MaxWidth)
        print("\tmaximum height:", props.MaxHeight)
        print("\tcolor space:", ('color' if props.IsColorCam else 'mono'))
        print("\tbayer pattern:", props.BayerPattern)
        print("\tsupported bins:")
        for b in props.SupportedBins:
            print("\t\tbin:", b)
        print("\tsupported image types:")
        for b in props.SupportedVideoFormat:
            print("\t\ttype:", b)
        print("\tmax depth:", props.MaxBitDepth)
        print("\tis trigger camera:", props.IsTriggerCam)

        # Property EX
        prop_ex = camera_sdk.get_camera_property_ex(camera_id)
        print("\tsupport control temp:", prop_ex.bSupportControlTemp)
        print("\tsupport pulse guide:", prop_ex.bSupportPulseGuide)

        print("\n---------------------------------------------------\n")

        # Controls
        ncontrols = camera_sdk.get_num_of_controls(camera_id)
        print("Num of controls: {}".format(ncontrols))

        print("Controls list:")
        for i in range(0, ncontrols):
            # Get control
            control = camera_sdk.get_control_caps(camera_id, i)
            # Get value
            value, auto = camera_sdk.get_control_value(camera_id, control.ControlType)
            print("=================================")
            print("\ttype:", control.ControlType)
            print("\tname:", control.Name)
            print("\tdescription:", control.Description)
            print("\tminimum value:", control.MinValue)
            print("\tmaximum value:", control.MaxValue)
            print("\tdefault value:", control.DefaultValue)
            print("\tis auto supported:", ('YES' if control.IsAutoSupported else 'NO'))
            print("\tis writable:", ('YES' if control.IsWritable else 'NO'))
            print("\tcurrent value:", value)
            print("=================================")

        print("\n---------------------------------------------------\n")

        print("Camera supported modes:\n")

        mode = camera_sdk.get_camera_support_mode(camera_id)
        for m in mode.SupportedCameraMode:
            print("\t", m)

        if SVB_CAMERA_MODE.SVB_MODE_TRIG_SOFT not in mode.SupportedCameraMode:
            print("ERROR: this is a trigger demo, your camera does not support soft trigger mode, exiting...")
            camera_sdk.close_camera(camera_id)
            exit()

        current_mode = camera_sdk.get_camera_mode(camera_id)
        print("\nCurrent camera mode: ", current_mode)

        if(current_mode != SVB_CAMERA_MODE.SVB_MODE_TRIG_SOFT):
            print("Set camera mode to soft trigger mode...")
            camera_sdk.set_camera_mode(camera_id, SVB_CAMERA_MODE.SVB_MODE_TRIG_SOFT)

        print("\n---------------------------------------------------\n")

        print("Set default ROI format...")
        roi_format = SVB_ROI_FORMAT(0, 0, props.MaxWidth, props.MaxHeight, 1)
        camera_sdk.set_roi_format(camera_id, roi_format)

        print("Set image type to raw 16...")
        camera_sdk.set_output_image_type(camera_id, SVB_IMG_TYPE.SVB_IMG_RAW16)

        croi_format = camera_sdk.get_roi_format(camera_id)
        print("Current roi format: ")
        print("\tstartX:", croi_format.start_x)
        print("\tstartY:", croi_format.start_y)
        print("\twidth:", croi_format.width)
        print("\theight:", croi_format.height)

        #print("Set custom format...")
        #roi_format = SVB_ROI_FORMAT(0, 0, 800, 600, 1)
        #camera_sdk.set_roi_format(camera_id, roi_format)

        #croi_format = camera_sdk.get_roi_format(camera_id)
        #print("Current roi format: ")
        #print("\tstartX:", croi_format.start_x)
        #print("\tstartY:", croi_format.start_y)
        #print("\twidth:", croi_format.width)
        #print("\theight:", croi_format.height)

        print("\n---------------------------------------------------\n")


        # Disable autosave
        camera_sdk.set_autosave_param(camera_id, False)

        pixel_size = camera_sdk.get_sensor_pixel_size(camera_id)
        print("Camera pixel size:", pixel_size)

        # Get current camera image type
        image_type = camera_sdk.get_output_image_type(camera_id)

        print("Init capture...")
        camera_sdk.start_video_capture(camera_id)

        #buffer_size = int(int((props.MaxBitDepth + 7) / 8) * croi_format.width * croi_format.height * 4)
        buffer_size = int(croi_format.width * croi_format.height * 16 / 8)

        max_captures = 5

        exposure_secs = 10
        camera_sdk.set_control_value(camera_id, SVB_CONTROL_TYPE.SVB_EXPOSURE, (exposure_secs * 1000000), False)

        print("Buffer size: ", buffer_size)

        for i in range(0, max_captures):
            data = None

            print("Capture frame nr. {}".format(i+1))
            start_time = datetime.now()
            exposure_thread = Thread(target=capture_func, args=(camera_sdk, camera_id, buffer_size, data))
            exposure_thread.start()

            current_secs = exposure_secs
            while(current_secs > 0):
                sleep(1)
                print("\ttime left (secs):",current_secs)
                current_secs -= 1

            exposure_thread.join()

            if data:
                filename = "SVB_image_{}.raw".format(i+1)
                print("\tsave on: ",filename)

                with open(filename, 'wb') as f:
                    f.write(data)

            delta = datetime.now() - start_time
            print("\tseconds: ", delta.seconds)

            dropped_frames = camera_sdk.get_dropped_frames(camera_id)
            print("\tdropped frames:", dropped_frames)


        camera_sdk.stop_video_capture(camera_id)

        print("Close camera")
        camera_sdk.close_camera(camera_id)
