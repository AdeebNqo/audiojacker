import threading
import select
import subprocess
import alsaaudio

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
                self.s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
                self.s.connect("/var/run/acpid.socket")
                print "Connected to acpid"
        def start(self):
                t = threading.Thread(target=self.reallystart)
                t.daemon = True
                t.start()
        def reallystart(self):
                while 1:
                    for event in s.recv(4096).split('\n'):
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
                                print('lid open')
                            elif event[2]=='close':
                                lid_close() #Laptop lid closed
                                print('lid closed')
volume = 0
voluman = None
#method to be called with the events
def audiojackresponder(someeventstring):
        someeventstring = someeventstring.rstrip()
        print(someeventstring)
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
if __name__=='__main__':
        ajeh = AudioJackEventHandler()
        ajeh.subscribe(audiojackresponder)
        ajeh.start()

        voluman = alsaaudio.Mixer()
        volume = int(voluman.getvolume()[0])

        while True:
                pass
