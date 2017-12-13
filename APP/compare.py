from elasticsearch import Elasticsearch
import elasticsearch
from pathlib import Path
import shutil
import hashlib
import sys
import arrow
import json

class Compare:

	def __init__(self,clientID):
		self.clientID = clientID

	def getConnection(self):
		with open('config.json') as json_data_file:
			data = json.load(json_data_file)
		host = data['elasticsearch']['host']
		es = Elasticsearch([{'host':data['elasticsearch']['host'], 'port':9200}]);
		return es

	def sha256_checksum(self, absolute_path, block_size=65536):
		sha256 = hashlib.sha256()
		with open(absolute_path, 'rb') as f:
			for block in iter(lambda: f.read(block_size), b''):
		    		sha256.update(block)
		return sha256.hexdigest()


	def insert_to_DB(self, clientID,filename,orig_filehash):
		utc = arrow.utcnow()
		local = utc.to('Africa/Tunis')
		C = Compare(clientID)		
		es = C.getConnection()
		es.index(index='sync_svr', doc_type='hash_check', body={
	    		'ClientID': clientID,
	    		'file_name': filename,
	    		'hash': orig_filehash,
	    		'datetime': local.timestamp 
		})
	
	def copyFile(self, absoluteFileSrc, path_bkp):
		shutil.copy2(absoluteFileSrc,path_bkp)

	def compareHashesAndCopy(self, clientID, filename, orig_filehash,path_orig,path_bkp):
		C = Compare(clientID)		
		es = C.getConnection()
		res = es.search(index="sync_svr", doc_type="hash_check", body={"query": {"bool": {"must": [{"match": {"ClientID": clientID}},{"match": {"file_name": filename}}]}}})
		print("%d documents found" % res['hits']['total'])
		if not res['hits']['total']==0:
			for doc in res['hits']['hits']:
				if orig_filehash==doc['_source']['hash']:
					print(doc['_id'])
					file_location = Path(path_bkp+'/'+filename)
					#On verifie si le fichier est present dans le dossier du serveur
					if not file_location.exists():
						print "Hashes do match"
						C.copyFile(path_orig+'/'+filename, path_bkp)
						print "[ERROR] file not found on server : file copy succeeded"
					else:
						print "Hashes do match"
						print "File up to date, no actions taken"
				else:
					C.copyFile(path_orig+'/'+filename, path_bkp)
					print "Hashes don't match, file copy succeeded"
		else:
			print "File hash sum not found in database, inserting to database..."
			C.insert_to_DB(clientID,filename,orig_filehash)
			shutil.copy2(path_orig+'/'+filename, path_bkp)
