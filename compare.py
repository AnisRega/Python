from elasticsearch import Elasticsearch
from pathlib import Path
import shutil
import hashlib
import sys
import arrow

es = Elasticsearch()

def sha256_checksum(absolute_path, block_size=65536):
    sha256 = hashlib.sha256()
    with open(absolute_path, 'rb') as f:
        for block in iter(lambda: f.read(block_size), b''):
            sha256.update(block)
    return sha256.hexdigest()

#def copy_files():

def insert_to_DB(clientID,filename):
	utc = arrow.utcnow()
	local = utc.to('Africa/Tunis')
	es = elasticsearch.Elasticsearch() # port 9200
	es.index(index='sync_svr', doc_type='hash_check', id=clientID, body={
    		'ClientID': clientID,
    		'file_name': filename,
    		'hash': orig_filehash,
    		'datetime': local.timestamp 
	})

def compare(clientID, filename, orig_filehash,path_orig,path_bkp):
	res = es.search(index="sync_svr", doc_type="hash_check", body={"query": {"match": {"file_name": filename}}})
	print("%d documents found" % res['hits']['total'])
	if not res['hits']['total']==0:
		for doc in res['hits']['hits']:
			if orig_filehash==doc['_source']['hash']:
				file_location = Path(path_bkp+'/'+filename)
				if not file_location.exists():
					shutil.copy2(path_orig+'/'+filename, path_bkp)
					print "Hashes do match"
					print "[ERROR] file not found on server : file copy succeeded"
				else:
					print "Hashes do match"
					print "File up to date, no actions taken"
			else:
				shutil.copy2(path_orig+'/'+filename, path_bkp)
				print "Hashes don't match, file copy succeeded"
	else:
		print "File hash sum not found in database, inserting to database..."
		insert_to_DB(clientID,filename)
		
clientID=3
filename="fileZ.txt"
path_orig="/home/superuser/Desktop/Scripting/TryOut/ORIG"
path_bkp="/home/superuser/Desktop/Scripting/TryOut/BKP"
absolute_path = path_orig+'/'+filename
orig_filehash = sha256_checksum(absolute_path)
print orig_filehash
compare(clientID, filename, orig_filehash, path_orig, path_bkp)
