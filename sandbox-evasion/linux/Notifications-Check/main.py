import dbus
from gi.repository import GLib
from dbus.mainloop.glib import DBusGMainLoop
import argparse

'''
dbus-monitor interface=org.freedesktop.Notifications,member=Notify

Reference: https://stackoverflow.com/questions/46688576/custom-d-bus-monitor-written-in-python-not-receiving-all-messages#75122112
'''

notifications = []

def msgFilter(bus, msg):
    if msg.get_interface() == 'org.freedesktop.Notifications':
        args = msg.get_args_list()
        
        if len(args) != 0:
            # print the notification origin & message
            origin = args[0]
            msg = args[4]
            
            notifications.append(f'{origin}:{msg}')



    #print(notifications)


def main():
    parser = argparse.ArgumentParser(description="Monitor notifications")
    parser.add_argument("-d", "--duration", help="Duration to sniff notifications for", required=True, type=int)
    arguments = parser.parse_args()

    DBusGMainLoop(set_as_default=True)
    
    bus = dbus.SessionBus()

    obj = bus.get_object('org.freedesktop.DBus',
                        '/org/freedesktop/DBus')


    obj.BecomeMonitor(["interface='org.freedesktop.Notifications'"],
                        dbus.UInt32(0),
                        interface='org.freedesktop.Notifications')

    
    
    bus.add_message_filter(msgFilter)
    
    duration = arguments.duration
    loop = GLib.MainLoop()
    GLib.timeout_add(int(duration * 1000), loop.quit)
    loop.run()

    print(f"[+] Notifications received: {notifications}")
    if len(notifications) > 0:
        print(f"[+] Notification count: {len(notifications)}. May not be a sandbox/VM")
    else:
        print(f"[!] No notifications received! Possible VM/Sandbox!")


if __name__ == '__main__':
    main()
