import os
import time
from datetime import datetime, timedelta
import pymongo
from bson.json_util import dumps, loads

con = pymongo.MongoClient(connect=False)
#database = con["prueba"]
database = con["test"]

def obtener_pulso_mongo():
	rango = datetime.now()
	contador = 0
	#db.pulsos.find({"llegada":{$gte:ISODate("2016-11-06T20:02:54Z"),$lt:ISODate("2016-11-06T20:02:57Z")}})
	query_result = loads(dumps(database.pulsos.find({
							"llegada":{
								"$gte": rango-timedelta(seconds=5000),
								"$lt": rango
							}
						})
					))
	for document in query_result:
		print document
		#if document["valor"] == "1":
		#	contador += 1
	print "este es el contador" + str(contador)
	print ">>>>>> query"
	print query_result

obtener_pulso_mongo()