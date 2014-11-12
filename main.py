import threading
import select
import subprocess
import alsaaudio

class AudioJackEventHAndler(object):
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

volume = 0
voluman = None
#method to be called with the events
def audiojackresponder(someeventstring):
        if (someventstring=="jack/headphone HEADPHONE unplug"):
                if (voluman!=None):
                        currVolume = voluman.getvolume()
                        if (currVolume!=0):
                                global volume
                                volume = currVolume
                                voluman.setvolume(0)
        elif (someventstring=="jack/headphone HEADPHONE plug"):
                if (voluman!=None):
                        voluman.set
if __name__=='__main__':
        ajeh = AudioJackEventHAndler()
        ajeh.subscribe(test)
        ajeh.start()

        global voluman
        voluman = alsaaudio.Mixer()
        global volume
        volume = voluman.getvolume()
        while True:
                pass
