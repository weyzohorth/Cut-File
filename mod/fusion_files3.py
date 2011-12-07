#=[site officiel]=====================
#<<<<<fusion_files3 by W3YZOH0RTH>>>>>
#==========[http://progject.free.fr/]=
from mod_file import *
from mod_base import int_base, base_int
from mod_string import int_len
from os import mkdir, remove, rmdir, system, chdir, getcwd
from sys import argv

#=============================================================================================================
def fusion_files(liste, path="", file_fuz=""):
	if type(liste) != type([]) : liste = list(liste)

	if not file_fuz:
		temp = liste[0]
		if "." in temp: temp = ".".join(liste[0].split(".")[:-1])
		fusioned_name = temp+".fuz"
		fusioned = file(try_file(fusioned_name),"wb")
		fusioned.write("0")
	elif type(file_fuz) == type("") or type(file_fuz) == type(u""):
		fusioned_name = file_fuz
		fusioned = file(try_file(fusioned_name),"wb")
		fusioned.write("0")
	else: fusioned = file_fuz

	for i in liste:
		name = i.replace("\\","/").split("/")[-1].encode("cp1252")
		size = 0
		print "\t",name

		fichier = file((path+"/")*bool(len(path))+i,"rb")
		while fichier.readline() != "" : size += 1
		fichier.close()
		fusioned.write(name+"\n"+int_base(size, 254)+"\n")
		fichier = file(path+"/"*bool(len(path))+i,"rb")
		string = fichier.readline()
		while string != "":
			fusioned.write(string)
			string = fichier.readline()
		fichier.close()
		if size: fusioned.write("\n")

	if type(file_fuz) == type("") or type(file_fuz) == type(u""):
		fusioned.close()
		return fusioned_name

#=============================================================================================================
def defusion_files(fichier, appel=0, new_path=""):
	path = "/".join(fichier.replace("\\","/").split("/")[:-1])
	if path != "": path += "/"

	fusioned = file(fichier,"rb")
	fusioned.read(1)
	erreur = 0
	if new_path: dossier = new_path
	else: dossier = try_name(".".join(fichier.replace("\\","/").split(".")[:-1]))
	print dossier
	try: mkdir(dossier)
	except: pass

	if erreur <= 100:
		string = fusioned.readline()
		read = -1

		while string != "":
			if read == -1:
				if string == "\n":
					fichier = file(name,"ab")
					fichier.write("\n")
					fichier.close()
					string = fusioned.readline()

				if string == "" : break
				else:
					name = try_file(dossier+"/"+string[:-1])
					print "\t",name
					fichier = file(name,"wb")

			elif read == -2: read = base_int(string[:-1], 254)
			elif read : fichier.write(string)
			else:
				fichier.write(string[:-1])
				fichier.close()

			string = fusioned.readline()
			read -= 1
		fusioned.close()
	else:
		dossier = None
	return dossier

#=============================================================================================================
def fusion_dirfile(dirs,	files=[], name=""):
	if dirs:
		if not name: name = dirs[0]
		if name[-1] == "/": name = name[ : -1]
		len_ext = len(get_ext(name))
		liste = [get_name(name)]
		paths = [name]
		if get_ext(name) != "fuz": name += ".fuz"

		for dossier in dirs:
			new_paths = get_paths(dossier)
			lim = (len("/".join(new_paths[0][:-1].split("/")[:-1]))+1)*int(bool(new_paths[0][:-1].count("/")))
			for i in new_paths :
				liste.append(liste[0] + "/" + i[lim:-1])
				paths.append(i[:-1])

		nbr_dir = int_base(len(liste))
		len_nbr = len(nbr_dir)
		i=0
		while i < len(paths):
			index = len("/".join(liste[i].split("/")[:-1]))+1
			if not i : index -= 1

			dossier = liste[i].split("/")[-1]
			index_dossier = len(dossier)
			path = liste[i][:index+index_dossier]
			for ind, p in enumerate(liste) :
				if p[ : index+index_dossier] == path:
					liste[ind] = p[ : index] +\
								p[index : index+index_dossier].replace(dossier, int_len(int_base(i), len_nbr)) +\
								p[index+index_dossier : ]
			i+=1
		
		liste[0] = liste[0][-len_nbr*2-1:-len_nbr-1]+(get_name(paths[0])+".")[ : -len_ext *bool(len_ext)-1]
		for i,e in enumerate(liste[1 : ]):
			liste[i+1] = e[-len_nbr*2-1:-len_nbr-1]+get_name(paths[i+1])

		fusioned = file(name,"wb")
		fusioned.write("1"+int_base(len_nbr)+int_len(nbr_dir, len_nbr))

		for i in liste : fusioned.write(i+"\n")

		for i, e in enumerate(liste):
			if i:
				fichiers = get_dirfile(paths[i])[1]
				if fichiers:
					fusioned.write(int_len(int_base(i),len_nbr))
					fusioned.write(int_base(len(fichiers))+"\n")
					print "\n"*2,paths[i]
					print
					fusion_files(fichiers, paths[i], fusioned)
			else:
				fusioned.write("0"*len_nbr)
				if files:
					fusioned.write(int_base(len(files), 254)+"\n")
					fusion_files(files, "", fusioned)
				else: fusioned.write("0\n")

		if files == None:
			fusioned.write(int_len(int_base(len(liste)),len_nbr))
			fusioned.write(int_base(len(files), 254)+"\n")
			fusion_files(files, "", fusioned)
		fusioned.close()
		return name
	else: return fusion_files(files,file_fuz=name)

#=============================================================================================================
def defusion_dir(fusioned, new_path=""):
	if new_path:
		if is_file(new_path): path = try_name(new_path)
		else: path = new_path[:]
		try: mkdir(path)
		except: pass
	else: path = "/".join(fusioned.replace("\\","/").split("/")[:-1])
	if path[-1] != "/": path += "/"
	len_path = len(path)

	fusioned = file(fusioned,"rb")
	fusioned.read(1)
	dirs = []
	len_nbr = base_int(fusioned.read(1))
	nbr_dir = base_int(fusioned.read(len_nbr))
	for i in range(nbr_dir) : dirs.append(fusioned.readline()[:-1]+"/")
	for i,f in enumerate(dirs):
		if i:
			index = f[:len_nbr]
			dirs[i] = index.replace(index,dirs[base_int(index)])+f[len_nbr:]

		erreur = 0
		temp = try_name(path+dirs[i][:-1])
		mkdir(temp)
		dirs[i] = temp[len_path:]+"/"
		if erreur > 100:break

	string = fusioned.read(len_nbr)
	c_dir = dirs[base_int(string)]
	nbr_file = base_int(fusioned.readline()[:-1])+1
	if erreur <= 100:
		while string != "" and nbr_file:
			print "\n"*2,"\t",c_dir
			print

			string = fusioned.readline()
			read = -1
			while string != "" and nbr_file:
				if read == -1:
					if string == "\n":
						fichier = file(path+c_dir+name,"ab")
						fichier.write("\n")
						fichier.close()
						string = fusioned.readline()

					if string == "":break
					else:
						nbr_file -= 1
						if not nbr_file :break
						name = get_name(try_name(path+c_dir+string[:-1]))
						fichier = file(path+c_dir+name,"wb")
						print "\t"*2,name

				elif read == -2 :read = base_int(string[:-1],254)
				elif read : fichier.write(string)
				else:
					fichier.write(string[:-1])
					fichier.close()

				string = fusioned.readline()
				read -= 1

			if len(string) > len_nbr: c_dir = dirs[base_int(string[ : len_nbr])]
			else:
				string += fusioned.readline()
				c_dir = dirs[base_int(string[ : len_nbr])]
			nbr_file = base_int(string[len_nbr : -1], 254)+1

	fusioned.close()
	return path+dirs[0][:-1]

#=============================================================================================================
def fusion(liste, avancement=False, path=""):
	if type(liste) == type("") : liste = [liste]
	dirsfiles = [[],[]]
	xmax = len(liste)
	unix = bool(getcwd()[0] == "/")
	print "Trie des dossiers et des fichiers :"
	for x,d in enumerate(liste):
		if avancement:
			if unix : system("clear")
			else : system("cls")
			print x+1,"/",xmax,"Entrees triees soit",(x+1)*100./xmax,"%"
		try:
			file(d).close()
			dirsfiles[1].append(d)
		except : dirsfiles[0].append(d)

	print "Trie des dossiers et des fichiers : [ O K ]"

	print "\n"*2,"Fusion :"
	if not dirsfiles[0]: return fusion_files(dirsfiles[1], file_fuz=path)
	elif dirsfiles[0]: return fusion_dirfile(dirsfiles[0], dirsfiles[1], path)

#=============================================================================================================
def defusion(name,defuz=True,suppr=False, path=""):
	fichier = file(name)
	_type_ = int(fichier.read(1))
	fichier.close()
	if _type_:
		print "\n"*2,"Defusion du dossier :"
		dossier = defusion_dir(name, path)
	else:
		print "\n"*2,"Defusion des fichiers :"
		dossier = defusion_files(name, 0, path)
	print dossier

	if defuz:
		for f in get_allfiles(dossier):
			if get_ext(f) == "fuz" : defusion(f,True,True, dossier)

	if suppr:
		print "\n"*2,"Suppression du fichier de fusion :",
		try:
			remove(name)
			print "[ O K ]"
		except Exception, erreur:
			print "[FAIL]", erreur
	return dossier

#=============================================================================================================
def create_autoextract(liste, avancement=False, path=""):
	if not path: path = liste[0]
	ext = get_ext(path)
	path = defusion_files(get_path(argv[0]) + "extract files 3.fuz", new_path=try_name((path+".")[:-(len(ext)+1)*bool(ext)-1]))
	fusion(liste, avancement, path+"/fusion.fuz")
