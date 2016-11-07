# coding=utf-8
from tornado import gen, web
import json
import timeit
import datetime
import tornado.web
import tornado.websocket
import tornado.httpserver
import tornado.ioloop
import pymongo
from bson.json_util import dumps

from tasks import guardar_Data
#EJEMPLO DE POST Y GET COMUN Y CORRIENTE CON MONGO
# Aqui la idea es hacer los gets para trabajar la
#información guardada
class DataHandler(tornado.web.RequestHandler):
	def check_origin(self, origin):
		return True

	def get(self):
		db = self.application.database
		self.write(dumps(db.pulsos.find()))

	def post(self):
		#self.get_argument('anArg')
		pass

#Maneja el Index
class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index_p.html")

#EJEMPLO DE PUSH LUEGO DE CAPTURAR UN DATO DE LA 
#BASE DE DATOS EN TIEMPO REAL
class WebSocketHandler(tornado.websocket.WebSocketHandler):

    def check_origin(self, origin):
        return True

    clients = []
    def open(self):
    	print ('new connection')
    	self.write_message("Hello World")
    	WebSocketHandler.clients.append(self)

    def on_message(self, message):     
        print ("el mensaje llego a las:")
        llegada = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        print ("llegada:")
        print (llegada)

        start = timeit.default_timer()

        msg = json.loads(message)

        for c in WebSocketHandler.clients:
            if c != self:
                c.write_message(msg)
        #Envio_a_la_cola
        guardar_Data.delay(msg, llegada)

        stop = timeit.default_timer()
        diferencia = stop - start
        if "cont" in msg:
            print (msg["cont"])
        print (diferencia)
        #Diferencia en enviar la data 
        #y enviar a la cola de guardado
#        print ("diferencia Total: ")
#	if "cont" in msg:
#		print (msg["cont"])
#	print (diferencia)
        
        
    def on_close(self):
        print ('connection closed')
        WebSocketHandler.clients.remove(self)

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/', IndexHandler),
            (r'/data', DataHandler),
            (r'/websocket', WebSocketHandler)
        ]
        self.con = pymongo.MongoClient()
        #conexion con la base de datos prueba de Mongo
        self.database = self.con["prueba"]
        tornado.web.Application.__init__(self, handlers, debug=True)

if __name__ == '__main__':
    ws_app = Application()
    server = tornado.httpserver.HTTPServer(ws_app)
    server.listen(3000)
    tornado.ioloop.IOLoop.instance().start()
