#!/usr/bin/env python3
# -*- coding: utf8 -*-
""" A simple continuous receiver class. """
# Copyright 2015 Mayer Analytics Ltd.
#
# This file is part of pySX127x.
#
# pySX127x is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public
# License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# pySX127x is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more
# details.
#
# You can be released from the requirements of the license by obtaining a commercial license. Such a license is
# mandatory as soon as you develop commercial activities involving pySX127x without disclosing the source code of your
# own applications, or shipping pySX127x with a closed source product.
#
# You should have received a copy of the GNU General Public License along with pySX127.  If not, see
# <http://www.gnu.org/licenses/>.


from time import sleep
import time
import json
import packer
import sys 
import numpy as np
sys.path.insert(0, '../')
from SX127x.LoRa import *
from SX127x.board_config import BOARD
from SX127x.LoRaArgumentParser import LoRaArgumentParser

BOARD.setup()

parser = LoRaArgumentParser("Continous LoRa receiver.")

import queue
from buf import QuBuf

#socket to container --Yu_Cheng
#!/usr/bin/env python3
import socket
import sys
HOST = '127.0.0.1'
PORT = 6000


# python2
try:
    import sys
    reload(sys)
    sys.setdefaultencoding('utf-8')
except:
    pass

class LoRaRcvCont(LoRa):
    def __init__(self, verbose=False):
        super(LoRaRcvCont, self).__init__(verbose)
        self.set_mode(MODE.SLEEP)
        self.set_dio_mapping([0,0,0,0,0,0])    # RX
        self._id = "GW_01"
        #self.value = None


    def on_rx_done(self):
        print("\nRxDone")
        print('----------------------------------')

        payload = self.read_payload(nocheck=True)
        #payload = QuBuf(pl)
        data = ''.join([chr(c) for c in payload])
        #data = QuBuf(pl)
        print(data)
        try:
            _length, _data = packer.Unpack_Str(data)
            print("\nTime: {}".format( str(time.ctime() )))
            #print("Length: {}".format( _length ))
            #print("Raw RX: {}".format( payload ))

            try:
                # python3 unicode
                #print("\nReceive: {}".format( _data.encode('latin-1').decode('unicode_escape')))
                data = "\n{}".format( _data.encode('latin-1').decode('unicode_escape'))
                print("\nRxData:{}".format(data)) 
                #socket_connect(data) 
            except:
                # python2
                print("\nReceive: {}".format( _data ))
        except:
            print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
            print("Non-hexadecimal digit found...")
            print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
            print("Receive: {}".format( data))



        self.set_dio_mapping([1,0,0,0,0,0])    # TX
        self.set_mode(MODE.STDBY)
  
        sleep(1)
        self.clear_irq_flags(TxDone=1)
        data = {"id":self._id, "data":packer.ACK}
        _length, _ack = packer.Pack_Str( json.dumps(data) )

        try:
            # for python2
            ack = [int(hex(ord(c)), 0) for c in _ack]
        except:
            # for python3 
            ack = [int(hex(c), 0) for c in _ack]

        print("\nACK: {}".format( self._id))
        self.write_payload(ack)    
        self.set_mode(MODE.TX)


    def on_tx_done(self):
        print("\nTxDone")
        self.set_dio_mapping([0,0,0,0,0,0])    # RX
        self.set_mode(MODE.STDBY)
        sleep(1)
        self.reset_ptr_rx()
        self.set_mode(MODE.RXCONT)
        self.clear_irq_flags(RxDone=1)


    def start(self):
        self.reset_ptr_rx()
        self.set_mode(MODE.RXCONT)
        while True:
        
            sleep(1)
            rssi_value = self.get_rssi_value()
            status = self.get_modem_status()
            sys.stdout.flush()
            sys.stdout.write("\r%d %d %d" % (rssi_value, status['rx_ongoing'], status['modem_clear']))
          
            """
            try:
                #input = raw_input
                rawinput = raw_input(">>> ")
            except NameError:
                rawinput = input(">>> ")
            except KeyboardInterrupt:
                lora.set_mode(MODE.SLEEP)
                sleep(.5) BOARD.teardown() exit() """ 


    #socket to container --Yu_Cheng 
    #!/usr/bin/env python3 
    def socket_connect(data): 
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: 
            s.connect((HOST,PORT))
            RxData = data.encode('utf-8')
            print(RxData)
            if RxData:
                s.send(RxData)
            s.close()



lora = LoRaRcvCont(verbose=False)
args = parser.parse_args(lora)
lora.set_mode(MODE.STDBY)
lora.set_pa_config(pa_select=1)

try:
    lora.start()
except KeyboardInterrupt:
    sys.stdout.flush()
    sys.stderr.write("KeyboardInterrupt\n")
finally:
    sys.stdout.flush()
    lora.set_mode(MODE.SLEEP)
    sleep(.5)
    BOARD.teardown()

