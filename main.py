import threading
import select
import subprocess
import alsaaudio
import socket
import pynotify

import gtk
from daemon import Daemon as d
import time
import sys
import traceback

#
#Class listens for audiojack events
class AudioJackEventHandler(object):
        def __init__(self):
                self.subscribers = []
        def subscribe(self,somefunction):
                self.subscribers.append(somefunction)
        def unsubscribe(self,somefunction):
                self.subscribers.remove(somefunction)
        def start(self):
                t = threading.Thread(target=self.reallystart)
                t.daemon = True
                t.start()
        def reallystart(self):
                process = subprocess.Popen('acpi_listen', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		while True:
			#the items to be read by process
			reads = [process.stderr.fileno(), process.stdout.fileno()]
			returned = select.select(reads, [], [])
			for readydata in returned[0]:
				if (readydata == process.stdout.fileno()):
					self.notify(process.stdout.readline())
				#if (readydata == process.stderr.fileno()):
				#	print("stderr says {}".format(process.stderr.readline()))
        def notify(self,someevent):
                for sub in self.subscribers:
                        sub(someevent)
#
#Class listens for .. events
class ComputerStateEventHandler(object):
        def __init__(self):
                self.subscribers = []
                self.s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
                self.s.connect("/var/run/acpid.socket")
        def subscribe(self,somefunction):
                self.subscribers.append(somefunction)
        def unsubscribe(self,somefunction):
                self.subscribers.remove(somefunction)
        def start(self):
                t = threading.Thread(target=self.reallystart)
                t.daemon = True
                t.start()
        def reallystart(self):
                while 1:
                    for event in self.s.recv(4096).split('\n'):
                        event=event.split(' ')
                        if len(event)<2: continue
                        #print event
                        #if event[0]=='ac_adapter':
                        #    if event[3]=='00000001': #plugged
                        #        print('power plugged in')
                        #    else: #unplugged
                        #        print('power unplugged')
                        #elif event[0]=='button/power':
                        #    print('power button pressed')
                        if event[0]=='button/lid':
                            if event[2]=='open':
                                self.notify('lid open')
                            elif event[2]=='close':
                                self.notify('lid closed')
        def notify(self,someevent):
                for sub in self.subscribers:
                        sub(someevent)
volume = 0
voluman = None
#method to be called with the events generated by audio jack
def audiojackresponder(someeventstring):
        someeventstring = someeventstring.rstrip()

        global volume
        if (someeventstring=="jack/headphone HEADPHONE unplug"):
                if (voluman!=None):
                        currVolume = int(voluman.getvolume()[0])
                        if (currVolume!=0):
                                volume = currVolume
                                voluman.setvolume(0)

        elif (someeventstring=="jack/headphone HEADPHONE plug"):
                if (voluman!=None):
                        voluman.setvolume(volume)
        elif (someeventstring.startswith("button/mute MUTE")):
                if (voluman!=None):
                        voluman.setvolume(volume)


# method for changing audio state back to what it was
def changestate_cb(n, action):
        assert action == "ignore"
        print('change state callled')
        if (voluman!=None):
                voluman.setvolume(volume)
        gtk.main_quit()
def donotchangestate_cb(n, action):
        assert action == "ignore"
        print('Audio has not been changed')
        gtk.main_quit()
#method to be called with the events of the computer lid
def computerlidresponder(someeventstring):
        if (someeventstring=='lid closed'):
                if (voluman!=None):
                        currVolume = int(voluman.getvolume()[0])
                        if (currVolume!=0):
                                volume = currVolume
                                voluman.setvolume(0)
        elif (someeventstring=='lid open'):
                title = "audiojacker"
                msg = "Audio was open muted on lid close. unmute?"
                pynotify.init(title)
		notif = pynotify.Notification(title, msg, )
                notif.set_urgency(pynotify.URGENCY_CRITICAL)
                notif.add_action("ignore","No", donotchangestate_cb)
                notif.add_action("ignore","Yes", changestate_cb)
		notif.show()
                gtk.main()

#
#AudioJack daemon
class AudioJack(d):
        def run(self):
                global voluman
                global volume

                ajeh = AudioJackEventHandler()
                ajeh.subscribe(audiojackresponder)
                ajeh.start()

                voluman = alsaaudio.Mixer()
                volume = int(voluman.getvolume()[0])

                cseh = ComputerStateEventHandler()
                cseh.subscribe(computerlidresponder)
                cseh.start()

                while True:
                        pass

#
#Control in indicator panel
class IndicatorPanelControl(object):
        def __init__(self):
                try:
                        import gobject
                        import gtk
                        import appindicator
                        import sys

                        ind = appindicator.Indicator ("example-simple-client","indicator-messages",
                                                        appindicator.CATEGORY_APPLICATION_STATUS)

                        ind.set_status (appindicator.STATUS_ACTIVE)
                        ind.set_attention_icon ("indicator-messages-new")

                        # create a menu
                        menu = gtk.Menu()

                        # create some drop down options

                        optionName = "Menu Option - 1"
                        menu_items = gtk.MenuItem(optionName)
                        menu.append(menu_items)
                        menu_items.connect("activate", self.menuitem_response, optionName)
                        menu_items.show()

                        optionName = "Menu Option - 2"
                        menu_items = gtk.MenuItem(optionName)
                        menu.append(menu_items)
                        menu_items.connect("activate", self.menuitem_response, optionName)
                        menu_items.show()

                        optionName = "Quit"
                        menu_items = gtk.MenuItem(optionName)
                        menu.append(menu_items)
                        menu_items.connect("activate", self.quitApplication, optionName)
                        menu_items.show()

                        ind.set_menu(menu)
                        gtk.main()
                except Exception:
                        traceback.print_exc()
        def menuitem_response(self,w, optionName):
                print optionName
        def quitApplication(self,w, optionName):
                daemonaudiojack.stop()
                sys.exit(0)

daemonaudiojack = None

def IndicatorPanelWorker():
        ipc = IndicatorPanelControl()
if __name__=='__main__':
        daemonaudiojack = AudioJack('/tmp/audiojacker.pid')
        if len(sys.argv) == 2:
                if 'start' == sys.argv[1]:
                        ipwt = threading.Thread(target=IndicatorPanelWorker)
                        ipwt.daemon = True
                        ipwt.start()
                        daemonaudiojack.start()
                elif 'stop' == sys.argv[1]:
                        daemonaudiojack.stop()
                elif 'restart' == sys.argv[1]:
                        daemonaudiojack.restart()
                else:
                        print "Unknown command"
                        sys.exit(2)
                sys.exit(0)
        else:
                print "usage: %s start|stop|restart" % sys.argv[0]
                sys.exit(2)
