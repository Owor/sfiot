#import Queue as queue
import queue
def QuBuf(payload):
    q = queue.Queue()
    q.put(payload)
    while not q.empty():
        return q.get()
        #print(q.get())
