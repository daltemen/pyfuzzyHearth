import os
import time
import redis
from datetime import datetime, timedelta
import pymongo
from bson.json_util import dumps, loads

from fuzzy_logic import fuzzy_logic_hearth

from celery import Celery


r = redis.StrictRedis(host='localhost', port=6379, db=0)
SET_REDIS = "pulsos"

DATABASE_HEARTH = "MONGO"

celery = Celery("tasks", broker="amqp://guest:guest@localhost//")
celery.conf.result_backend = os.environ.get('result_backend', 'amqp')
con = pymongo.MongoClient(connect=False)
#database = con["prueba"]
database = con["test"]

#configuracion de periodicTasks
@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls test('hello') every 10 seconds.
    if DATABASE_HEARTH == "REDIS":
    	sender.add_periodic_task(60.0, obtener_pulso_redis.s(), name='obtener_pulso')
    else:
    	sender.add_periodic_task(60.0, obtener_pulso_mongo.s(), name='obtener_pulso')

celery.conf.timezone = 'UTC'

@celery.task
def guardar_Data(mensaje, llegada):
    if DATABASE_HEARTH == "REDIS":
    	#r.zadd('prueba',r.time()[0],{"valor":mensaje["var"],"llegada":datetime.strptime(llegada, "%Y-%m-%dT%H:%M:%S")})
    	r.zadd('prueba',r.time()[0],{"valor":mensaje["var"],"llegada":datetime.strptime(llegada, "%Y-%m-%dT%H:%M:%S")})
	    if "var" in mensaje:
		    '''insert = database.pulsos.insert({
		                                "valor": mensaje["var"],    				    
		                                "llegada": datetime.strptime(llegada, "%Y-%m-%dT%H:%M:%S")
		                             })'''
		    print (mensaje["cont"])
		else:
		    print ("invalido") 
		
    else:
    	if "var" in mensaje:
		    insert = database.pulsos.insert({
		                                "valor": mensaje["var"],    				    
		                                "llegada": datetime.strptime(llegada, "%Y-%m-%dT%H:%M:%S")
		                             })
		    print (mensaje["cont"])
		else:
		    print ("invalido")


@celery.task
def obtener_pulso_mongo():
	rango = datetime.now()
	contador = 0

	query_result = loads(dumps(database.pulsos.find({
							"llegada":{
								"$gte": rango-timedelta(seconds=10000),
								"$lt": rango
							}
						})
					))

	for document in query_result:
		print document
		if document["valor"] == 1:
			contador += 1

	print "este es el contador" + str(contador)
	#se controla en logica difusa 
	fuzzy_logic_hearth(contador)


@celery.task
def obtener_pulso_redis():
	#example query last_day 
	query =	r.zrangebyscore('prueba', r.time()[0]-86400000, r.time()[0])


if __name__ == "__main__":
    celery.start()
