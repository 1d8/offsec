# Webcam Check

Checking the `/sys/class/video4linux` & checking each `video*` directory to find a webcam attached to determine whether or not a machine is a sandbox/VM. This is done by reading the `name` file within each `video*` directory to get the name of the camera device.

No webcam found means potential sandbox/VM
