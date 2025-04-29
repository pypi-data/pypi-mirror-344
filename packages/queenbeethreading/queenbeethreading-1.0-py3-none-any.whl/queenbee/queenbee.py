from exceptions import BeeException

import threading

class BeeBuffer:
    def __init__(self):
        self.buffer=[]
    def put(self,bee):
        self.buffer.append(bee)
    def get(self):
        return self.buffer.pop(0)
    def __iter__(self):
        return self.buffer.__iter__()

drone_number=0

class DroneBee:
    def __init__(self,func,allmd=None,**inf):
        self.md=inf
        self.prop=func
        self.process(allmd=allmd)
    def process(self,allmd):
        global drone_number
        if allmd:
            self.md=allmd
        self.label=self.md.get("label",str(drone_number))
        drone_number+=1
    def mate(self):
        return DroneBee(self.prop,allmd=self.md)
    def retask(self,func):
        self.prop=func


def nulltask():
    raise BeeException("Worker Bee Error: Null Task Found. Please apply() a drone to this bee.")

class WorkerBee:
    def __init__(self):
        self.drone=None
        self.task=nulltask
    def apply(self,d:DroneBee):
        self.drone=d
        self.task=d.prop
    def go(self):
        threading.Thread(target=self.task).run()



class QueenBee:
    @staticmethod
    def create():
        #This is so nobody says 'x=WorkerBee()'
        return WorkerBee()
    def __init__(self):
        self.emptybuffer=BeeBuffer()
        self.runnable={}
        self.dronerepo={}
        for i in range(100):
            self.emptybuffer.put(self.create())
        
    def makeBee(self,d:DroneBee):
            self.dronerepo[d.label]=d
    def uptask(self,label,cap):
            #sanity check
            for item in self.emptybuffer:
                assert isinstance(item,WorkerBee)
            for i in range(cap):
                f=self.emptybuffer.get()
                f.apply(self.dronerepo[label])
                self.runnable[label+str(i)]=f
    def begin(self,label=None):
        if label:
            for l,b in self.runnable.items():
                if l==label:
                    b.go()
        else:
            for b in self.runnable.values():
                b.go()