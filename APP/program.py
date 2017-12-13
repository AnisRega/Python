from compare import Compare
import json
import sys

print("0) Configuration de l'application!")
print("1) Synchroniser un fichier specifique")
print("2) Synchroniser un dossier specifique")
print("3) Verifier l'etat du dossier avec le serveur")
print("4) Lancer maintenant la synchronisation!")
print("Taper Entree pour quitter!")
print("=============================================")

reponse=raw_input('Saisir une valeur : ')
if reponse == "0":
	with open('config.json') as json_data_file:
		data = json.load(json_data_file)
	data['elasticsearch']['host'] = raw_input('Saisir une adresse IP : ') 
	#data['configApp']['clientID'] = raw_input('Saisir un identifiant : ') 
	#data['configApp']['fileTypes'] = raw_input('Saisir le type de fichiers a syncroniser [*]: ') 
	#data['configApp']['syncFolder'] = raw_input('Preciser le dossier a synchroniser : ')
	#data['configApp']['nbrVersions'] = raw_input('Nombre de versions a garder [1]: ')
	#data['configApp']['syncFreq'] = raw_input('Frequence de synchronisation Cronjob [C]/ OnChange [Ch]: [C] ')
	#data['configApp']['syncFreq'] = raw_input('Periodicite de synchronisation : [1 jour] ')
	with open('config.json', 'w') as outfile:  
    		json.dump(data, outfile)
	print("Config. OK")
		
if reponse == "1":
	print(reponse)
if reponse == "2":
	print(reponse)
if reponse == "3":
	print(reponse)
if reponse == "4":
	path_orig="/home/superuser/Desktop/Scripting/TryOut/ORIG"
	clientID=3
	Comp = Compare(clientID)
	filename="fileZ.txt"
	path_bkp="/home/superuser/Desktop/Scripting/TryOut/BKP"
	absolute_path = path_orig+'/'+filename
	orig_filehash = Comp.sha256_checksum(absolute_path)
	print orig_filehash
	Comp.compareHashesAndCopy(clientID, filename, orig_filehash, path_orig, path_bkp)
