import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__),'lib'))

import log_listener as listener
import random
import time
from datetime import datetime
listsm = []

DB_listener = listener.log_listener()

while(True):
    rn = random.randint(0,5)
    now = datetime.now()
    for x in range(rn):
        listsm.append("SM"+str(x))

    DB_listener.get_data(gatewayID="GW01",data=rn,timestamp=now,sm_list=listsm,tag="anomaly") # The tag is anomaly or smfailed .
    time.sleep(10)