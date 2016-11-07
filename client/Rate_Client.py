import timeit
import datetime
import time
import RPi.GPIO as io 
import os 
import websocket
import json
import sys
#import Adafruit_DHT
#import Queue as Q
#import zmq
from threading import Timer
#from multiprocessing import Process, Queue


def recibir_pulso():
    io.setmode(io.BCM)
    io.setwarnings(False)

    receiver_in = 23
    LED_in = 24

    io.setup(receiver_in, io.IN) 
    io.setup(LED_in, io.OUT)  
    io.output(LED_in, io.HIGH) 

    sample=2
    oldSample=1
    try:
	cont = 1
        while True:
            sample = io.input(receiver_in)
            if sample == 1 and oldSample == 0:
                print ("Beat 1")
                start = timeit.default_timer()
                ws.send(json.dumps({"cont":cont,"var":1}))
                stop = timeit.default_timer()
                print ("diferencia: ")
                print (stop - start)
                print (datetime.datetime.now().strftime("%H:%M:%S:%f"))		
		cont = cont+1
		print cont
                #io.output(LED_in, io.LOW)
                """print("Receiving...")
                result = ws.recv()
                print("Received {}".format(result))"""
                
            if sample == 0 and oldSample == 1:
                print "Beat 0"
                start = timeit.default_timer()
                ws.send(json.dumps({"cont":cont,"var":0}))
                stop = timeit.default_timer()
                print ("diferencia: ")
                print (stop - start)
                print (datetime.datetime.now().strftime("%H:%M:%S:%f"))
		cont = cont +1
		print cont
                #io.o   dsfutput(LED_in, io.HIGH) # turn LED off
                """print("Receiving...")
                result = ws.recv()
                print("Received {}".format(result))"""
            
            oldSample = sample
    except KeyboardInterrupt:
        print "Received Interrupt" 

if __name__ == '__main__':
    while True:
        try:
            websocket.enableTrace(True)
            ws = websocket.create_connection("ws://52.43.170.107:3000/websocket")
            Timer(1, recibir_pulso()).start()
        except:
            continue
        break
