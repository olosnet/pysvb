#!/usr/bin/env python3

from pysvb.camera import SVB_CAMERA_MODE, PySVBCameraSDK, SVB_ROI_FORMAT

def separator(c="-", l=50):
    print("\n{}\n".format(c*l))


if __name__ == "__main__":

    camera_sdk = PySVBCameraSDK()

    connected = camera_sdk.get_num_of_connected_cameras()
    print("SDK VERSION:", camera_sdk.sdk_version)
    print("Connected camera(s): {}".format(connected) )
    camera_id = -1

    if connected > 0:
        for i in range(0, connected):
            separator()
            info = camera_sdk.get_camera_info(i)
            print("Friendly name:", info.FriendlyName)
            print("Port type:", info.PortType)
            print("Serial number",info.CameraSN)
            print("Device ID:", hex(info.DeviceID))
            print("Camera ID:", info.CameraID)
            camera_id = info.CameraID
            separator()

        print("Open latest camera...")
        camera_sdk.open_camera(camera_id)

        print("\n{}\n".format("-"*50))
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

        separator()

        # Controls
        ncontrols = camera_sdk.get_num_of_controls(camera_id)
        print("Num of controls: {}".format(ncontrols))

        print("Controls list:")
        for i in range(0, ncontrols):
            # Get control
            control = camera_sdk.get_control_caps(camera_id, i)
            # Get value
            value, auto = camera_sdk.get_control_value(camera_id, control.ControlType)
            separator(c="=", l=40)
            print("\ttype:", control.ControlType)
            print("\tname:", control.Name)
            print("\tdescription:", control.Description)
            print("\tminimum value:", control.MinValue)
            print("\tmaximum value:", control.MaxValue)
            print("\tdefault value:", control.DefaultValue)
            print("\tis auto supported:", ('YES' if control.IsAutoSupported else 'NO'))
            print("\tis writable:", ('YES' if control.IsWritable else 'NO'))
            print("\tcurrent value:", value)
            separator(c="=", l=40)

        separator()
        print("Camera supported modes:\n")

        mode = camera_sdk.get_camera_support_mode(camera_id)
        for m in mode.SupportedCameraMode:
            print("\t", m)

        current_mode = camera_sdk.get_camera_mode(camera_id)
        print("\nCurrent camera mode: ", current_mode)

        if(current_mode != SVB_CAMERA_MODE.SVB_MODE_NORMAL):
            print("Set camera mode to normal...")
            camera_sdk.set_camera_mode(camera_id, SVB_CAMERA_MODE.SVB_MODE_NORMAL)

        separator(c="=")

        print("Set default ROI format...")
        roi_format = SVB_ROI_FORMAT(0, 0, props.MaxWidth, props.MaxHeight, 1)
        camera_sdk.set_roi_format(camera_id, roi_format)

        croi_format = camera_sdk.get_roi_format(camera_id)
        print("Current roi format: ")
        print("\tstartX:", croi_format.start_x)
        print("\tstartY:", croi_format.start_y)
        print("\twidth:", croi_format.width)
        print("\theight:", croi_format.height)

        print("Set custom format...")
        roi_format = SVB_ROI_FORMAT(0, 0, 800, 600, 1)
        camera_sdk.set_roi_format(camera_id, roi_format)

        croi_format = camera_sdk.get_roi_format(camera_id)
        print("Current roi format: ")
        print("\tstartX:", croi_format.start_x)
        print("\tstartY:", croi_format.start_y)
        print("\twidth:", croi_format.width)
        print("\theight:", croi_format.height)

        separator(c="=")


        # Disable autosave
        camera_sdk.set_autosave_param(camera_id, False)

        pixel_size = camera_sdk.get_sensor_pixel_size(camera_id)
        print("Camera pixel size:", pixel_size)

        print("Init capture...")
        camera_sdk.start_video_capture(camera_id)
        buffer_size = int(int((props.MaxBitDepth + 7) / 8) * croi_format.width * croi_format.height * 4)

        wait_ms = 100
        max_captures = 2

        print("Buffer size: ", buffer_size)

        for i in range(0, max_captures):
            print("\tCapture {} frame".format(i+1))
            data = camera_sdk.get_video_data(camera_id, buffer_size, wait_ms)
            filename = "SVB_image_{}.raw".format(i+1)
            print("\tSave on: ",filename)

            with open(filename, 'wb') as f:
                f.write(data)

            dropped_frames = camera_sdk.get_dropped_frames(camera_id)
            print("\tdropped frames:", dropped_frames)


        print("Close camera")
        camera_sdk.close_camera(camera_id)
