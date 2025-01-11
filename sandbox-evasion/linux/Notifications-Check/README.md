# Linux Notifications Monitoring Tool

This script will monitor notifications on a Linux host for X amount of seconds in order to gauge whether or not a system is a VM/sandbox or a real host. Typically, a VM/sandbox wouldn't get any notifications from applications.

It works by using the dbus python library which monitors the notifications interface on a machine and will report on the application that invoked the notification & the message of the notification. After running for X seconds, it will report back any notifications received & the count of notifications. If the amount of notifications received is greater than 0, it'll report back that it's likely not a sandbox/VM.

*NOTE: This threshold likely isn't enough to differentiate between a VM/sandbox since notifications can be spoofed via `notify-send`. But it also wouldn't be difficult to add in a blacklist to the script to avoid counting notifications from programs such as `notify-send` to avoid picking up false positives*

This script can also be utilized as a means of passive reconnaissance on a machine to listen for notifications to gauge a user's activity and what applications they have installed on a system & how they may be using them. For example, it can pick up Discord notification.
