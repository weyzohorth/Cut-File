#-*- coding: cp1252 -*-
#=[site officiel]================
#<<<<<cut_file by W3YZOH0RTH>>>>>
#=====[http://progject.free.fr/]=
from mod_file import *
from mod_string import *
from mod_math import tronquer, classer
from os import getcwd,mkdir,remove,rmdir
from sys import argv

def cut_file(name, name_copy="", part=4, unite="", split=False, boss=None):
	"""nom du fichier, nom de la copie, nbr de parti ou parti en unite(o,ko,mo,go) ---> 1 ou 0 si erreur"""
	if unite != "":
		if unite.lower() =="ko":
			size_part = part*1024
		elif unite.lower() =="mo":
			size_part = part*pow(1024,2)
		elif unite.lower() =="go":
			size_part = part*pow(1024,3)
		else:
			size_part = part
	else:
		if boss: size_part = tronquer(boss.size / float(int(part)), _type="c")
		else: size_part = tronquer(file(name).size(True) / float(int(part)), _type="c")
		split = False

	if name_copy == "":
			name_copy = name[:]#pour ne pas prendre la reference de la chaine name comme valeur

	nbr = 0
	size = 0
	name_copy = name_copy.replace("\\","/")
	name = name.replace("\\","/")
	if name_copy.count("/"):
		dossier = name_copy.split("/")[-1].split(".")[0]
		url = "/".join(name_copy.split("/")[:-1])
	else:
		dossier = name_copy.split(".")[0]
		url = getcwd().replace("\\","/")

	if name_copy.count("/"):
		nom = name_copy.split("/")[-1]
	else:
		nom = name_copy

	dossier = try_dir(url+"/"+dossier)
	try:
		mkdir(dossier)
	except:
		pass
	fichier = open(name,"rb")
	name = dossier+"/"+nom+"~part_"+int_len(nbr)+".cut"
	copy = open(name, "wb")
	if boss: nbr_total = boss.size / size_part
	while 1:
		if size + 1024 <= size_part or split and nbr:
			text = fichier.read(1024)
			if text == "":break
			else:
				copy.write(text)
				if not split or not nbr: size += 1024
		else:
			nbr += 1
			if boss: boss.progression.setValue(int(nbr/nbr_total*100))
			valeur = size_part - size
			text = fichier.read(valeur)
			if text == "" and valeur:break
			else:
				copy.write(text)
				copy.close()
				name = dossier+"/"+nom+"~part_"+int_len(nbr)+".cut"
				copy = open(name, "wb")
				size = 0
	copy.close()
	if not file(name).size(True): remove(name)
	if boss: boss.progression.setValue(100)

def stick_file(name, boss=None, path="", suppr=True, eco=False):
	"""Url(des fichiers decoupes)/Nom du fichier de base"""
	name = name.replace("\\","/")
	if name.split("~")[-1].count("part_") and name.split(".")[-1] == "cut":
		name = "~".join(name.split("~")[:-1])

	if name.count("/"):
		url = name.split("/")
		dossier = url[-2]
		url = "/".join(url[:-2])
		name = name.split("/")[-1]
	else:
		url = getcwd().replace("\\","/")
	if url == "":
		url = getcwd().replace("\\","/")

	cut = []
	for i in get_files(url+"/"+dossier):
		if i.split("~")[0].split("/")[-1] == name and i.split("~")[-1].count("part_") and i.split(".")[-1] == "cut":
			cut.append(i)
	cut = classer(cut)
	if boss: nbr_total = len(cut)

	if path:
		if dir_exists(path):
			if path[-1] != "/": path += "/"
			file_name = try_name(path+name)
		else: file_name = try_name(path)
	else: file_name = try_name(url+"/"+name)

	fichier = open(file_name, "wb")
	nbr = 0
	for nbr, i in enumerate(cut):
		original = open(url+"/"+dossier+"/"+i, "rb")
		text = original.readline()
		while text != "":
			fichier.write(text)
			text = original.readline()
		original.close()
		if suppr and eco: remove(url+"/"+dossier+"/"+i)
		if boss: boss.progression.setValue(int((nbr + 1)/nbr_total*100))
	fichier.close()
	if suppr:
		if not eco:
			for i in cut:
				try: remove(url+"/"+dossier+"/"+i)
				except: pass
		try: rmdir(url+"/"+dossier)
		except: pass
	return file_name


if __name__ == "__main__":
	if len(argv) >= 2:
		if argv[1].split(".")[-1] != "cut":
			name_copy = raw_input("url de decoupage/nom du fichier decoupe\nrien pour reprendre l'url et le meme nom le fichier original ne sera pas ecrase :\n\t>>>")
			if input("0-Decoupage en partie de taille definie\n1-Decoupage en un nombre de parties definis\n\n\t>>>"):
				part = input("Nombre de parties :\n\t>>>")
				cut_file(argv[1].replace('"',""),name_copy.replace('"',""),part)
			else:
				size = input("Taille des parties :\n\t>>>")
				cut_file(argv[1].replace('"',""),name_copy.replace('"',""),size=size)
		else:
			stick_file(argv[1], eco=True)
	else:
		name = "///"
		while not file_exists(name): name = raw_input("chemin/nom du fichier :\n\t>>>")
		if name.split(".")[-1] != "cut":
			while 1:
				name_copy = raw_input("chemin de decoupage/nom du fichier decoupe\nrien pour reprendre le chemin et le meme nom, le fichier original ne sera pas ecrase :\n\t>>>")
				if not name_copy: break
				else:
					try:
						if dir_exists(get_path(name_copy)): break
					except: pass
			if input("0-Decoupage en partie de taille definie\n1-Decoupage en un nombre de parties definis\n\n\t>>>"):
				while 1:
					part = raw_input("Nombre de parties :\n\t>>>")
					try:
						if int(part) >= 2: break
					except: pass
				cut_file(decode(name.replace('"',"")),decode(name_copy.replace('"',"")),int(part))
			else:
				unite = ""
				while not unite.lower() in ["o", "ko", "mo", "go"]: unite = raw_input("Unite de memoire des parties (o, ko, mo ou go):\n\t>>>")
				while 1:
					part = raw_input("Taille des parties :\n\t>>>")
					try:
						if int(part) >= 1: break
					except: pass
				split = not bool(input("Splitter le fichier :\n\t0-Oui\n\t1-Non\n\n\t>>>"))
				cut_file(decode(name.replace('"',"")), decode(name_copy.replace('"',"")), int(part), unite, split)
		else:
			while 1:
				name_copy = raw_input("chemin de recollage(/nom du fichier recolle)\nrien pour reprendre le chemin et le meme nom:\n\t>>>")
				if not name_copy: break
				else:
					try:
						if dir_exists(name_copy): break
						elif dir_exists(get_path(name_copy)): break
					except: pass

			print "Supprimer les fichiers .cut"
			suppr = bool(input("0-Non\n1-Oui\n\n\t>>>"))
			eco = False
			if suppr:
				print "Supprimer les fichiers .cut"
				eco = bool(input("0-Pendant le recollage (utile sur les volumes à petite capacité)\n1-A la fin du recollage (plus sûr)\n\n\t>>>"))
			stick_file(name, None, name_copy, suppr, eco)



