from threading import Timer
import timeit
import datetime
import time
import os 
import websocket
import json

def recibir_pulso():
    try:
        cont = 1
        while True:
            start = timeit.default_timer()
            
            time.sleep(2)
            ws.send(json.dumps({"cont":cont,"var":1}))
            time.sleep(1)
            ws.send(json.dumps({"cont":cont,"var":0}))
            stop = timeit.default_timer()
            print (stop - start)
            print (datetime.datetime.now().strftime("%H:%M:%S:%f"))
    except KeyboardInterrupt:
        print ("Received Interrupt") 

if __name__ == '__main__':
    while True:
        try:
            websocket.enableTrace(True)
            ws = websocket.create_connection("ws://52.33.79.79:3000/websocket")
            Timer(1, recibir_pulso()).start()
        except:
            print ("failed at: ", datetime.datetime.now().strftime("%H:%M:%S:%f"))
            continue
        break
