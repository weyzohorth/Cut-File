#-*- coding:cp1252 -*-
#=[site officiel]===========
#<<<<<gui by W3YZOH0RTH>>>>>
#=[http://progject.free.fr/]
import PyQt4.Qt as qt
from cut_file import *
from mod_oct import conv_oct
from mod_file import file
from fusion_files3 import fusion_dirfile, defusion
import sys
from os import remove

class Gui(qt.QWidget):
	def __init__(__):
		qt.QWidget.__init__(__)
		if len(sys.argv) > 1: __.path = unicode(" ".join(sys.argv[1:]), "cp1252")
		else: __.path = ""
		__.fuz = False
		__.validator = qt.QIntValidator(__)
		__.Vlayout = qt .QVBoxLayout()
		__.Hlayout = qt .QHBoxLayout()
		__.groupbox = qt.QGroupBox("Fichier à coupé:")
		__.groupbox.layout = qt .QVBoxLayout()

		__.Menu_layout = qt .QHBoxLayout()
		__.path_bout = qt.QPushButton("ouvrir fichier", __)
		__.fuz_bout = qt.QPushButton("Fusionner dossier", __)

		__.label1 = qt.QLabel("chemin du fichier :")
		__.file_path = qt.QLineEdit()
		__.file_path.setReadOnly(True)

		__.label2 = qt.QLabel("nom du fichier :")
		__.file_name = qt.QLineEdit()
		__.file_name.setReadOnly(True)

		__.label3 = qt.QLabel("taille du fichier :")
		__.file_size = qt.QLineEdit()
		__.file_size.setText("")
		__.file_size.setReadOnly(True)

		__.widget = qt.QGroupBox("Fichier découpé :")

		__.widget.layout = qt .QVBoxLayout()
		__.widget.label = qt.QLabel("chemin du fichier découpé :")
		__.widget.copy_path = qt.QPushButton()
		__.widget.label1 = qt.QLabel("nom du fichier découpé :")
		__.widget.vlayout = qt.QVBoxLayout()
		__.widget.copy_name = qt.QLineEdit()
		__.widget.hlayout = qt.QHBoxLayout()

		__.widget.groupbox1 = qt.QGroupBox("taille des parties :")
		__.widget.groupbox1.setCheckable(True)
		__.widget.groupbox1.layout = qt .QVBoxLayout()
		__.widget.groupbox1.part_size = qt.QLineEdit()
		__.widget.groupbox1.part_size.setValidator(__.validator)
		__.widget.groupbox1.part_unit = []
		for i in ("o", "Ko", "Mo", "Go"): __.widget.groupbox1.part_unit.append(qt.QRadioButton(i, __))
		__.widget.groupbox1.part_unit[0].setChecked(True)
		__.widget.groupbox1.split = qt.QCheckBox("Couper en 2 le fichier", __)

		__.widget.groupbox2 = qt.QGroupBox("nombre de parties :")
		__.widget.groupbox2.setCheckable(True)
		__.widget.groupbox2.setChecked(False)
		__.widget.groupbox2.layout = qt .QVBoxLayout()
		__.widget.groupbox2.nbr_part = qt.QLineEdit()
		__.widget.groupbox2.nbr_part.setValidator(__.validator)

		__.widget2 = qt.QGroupBox("Fichier recollé :")
		__.widget2.layout = qt .QVBoxLayout()
		__.widget2.label1 = qt.QLabel("Chemin du fichier recollé :")
		__.widget2.copy_path = qt.QPushButton()
		__.widget2.label2 = qt.QLabel("Nom du fichier recollé :")
		__.widget2.copy_name = qt.QLineEdit()
		__.widget2.groupbox = qt.QGroupBox("Supprimer les fichiers .cut :")
		__.widget2.groupbox.setCheckable(True)
		__.widget2.groupbox.layout = qt .QVBoxLayout()
		__.widget2.groupbox.checkbox = qt.QCheckBox("pendant le recollage\n(dangereux mais utile pour les petits volumes)")
		__.widget2.checkbox = qt.QCheckBox("défusionner le dossier")
		__.widget2.checkbox.setChecked(True)
		__.widget2.checkbox.setVisible(False)

		__.ok_bout = qt.QPushButton(__)
		__.ok_bout.setText("Valider")

		__.progression = qt.QProgressBar(__)

		__.setLayout(__.Vlayout)
		__.Menu_layout.addWidget(__.path_bout)
		__.Menu_layout.addWidget(__.fuz_bout)
		__.Vlayout.addLayout(__.Menu_layout)
		__.Vlayout.addLayout(__.Hlayout)

		__.Hlayout.addWidget(__.groupbox)
		__.groupbox.setLayout(__.groupbox.layout)
		__.groupbox.layout.addWidget(__.label1)
		__.groupbox.layout.addWidget(__.file_path)
		__.groupbox.layout.addWidget(__.label2)
		__.groupbox.layout.addWidget(__.file_name)
		__.groupbox.layout.addWidget(__.label3)
		__.groupbox.layout.addWidget(__.file_size)


		__.Vlayout.addWidget(__.ok_bout)
		__.Vlayout.addWidget(__.progression)

		__.widget.setLayout(__.widget.layout)
		__.widget.layout.addWidget(__.widget.label)
		__.widget.layout.addWidget(__.widget.copy_path)

		__.widget.layout.addLayout(__.widget.hlayout)
		__.widget.hlayout.addLayout(__.widget.vlayout)
		__.widget.vlayout.addWidget(__.widget.label1)
		__.widget.vlayout.addWidget(__.widget.copy_name)

		__.widget.vlayout.addWidget(__.widget.groupbox2)
		__.widget.groupbox2.setLayout(__.widget.groupbox2.layout)
		__.widget.groupbox2.layout.addWidget(__.widget.groupbox2.nbr_part)

		__.widget.hlayout.addWidget(__.widget.groupbox1)
		__.widget.groupbox1.setLayout(__.widget.groupbox1.layout)
		__.widget.groupbox1.layout.addWidget(__.widget.groupbox1.part_size)
		__.widget.groupbox1.layout.Hlayout = qt.QHBoxLayout()
		__.widget.groupbox1.layout.addLayout(__.widget.groupbox1.layout.Hlayout)
		for i in __.widget.groupbox1.part_unit: __.widget.groupbox1.layout.Hlayout.addWidget(i)
		__.widget.groupbox1.layout.addWidget(__.widget.groupbox1.split)

		__.setLayout(__.Vlayout)
		__.widget.setVisible(False)

		__.widget2.layout.addWidget(__.widget2.label1)
		__.widget2.layout.addWidget(__.widget2.copy_path)
		__.widget2.layout.addWidget(__.widget2.label2)
		__.widget2.layout.addWidget(__.widget2.copy_name)
		__.widget2.layout.addWidget(__.widget2.groupbox)
		__.widget2.groupbox.layout.addWidget(__.widget2.groupbox.checkbox)
		__.widget2.layout.addWidget(__.widget2.checkbox)
		__.widget2.setLayout(__.widget2.layout)
		__.widget2.groupbox.setLayout(__.widget2.groupbox.layout)
		__.widget2.setVisible(False)

		__.Hlayout.addWidget(__.widget)
		__.Hlayout.addWidget(__.widget2)

		if __.path: __.ouvrir(False)
		qt.qApp.connect(__.widget.groupbox1, qt.SIGNAL("clicked()"), __.slot_groupbox)
		qt.qApp.connect(__.widget.groupbox2, qt.SIGNAL("clicked()"), lambda: __.slot_groupbox(True))
		qt.qApp.connect(__.path_bout, qt.SIGNAL("clicked()"), lambda: __.ouvrir(True))
		qt.qApp.connect(__.ok_bout, qt.SIGNAL("clicked()"), __.slot_couper)
		qt.qApp.connect(__.widget2.copy_path, qt.SIGNAL("clicked()"), __.slot_change_path)
		qt.qApp.connect(__.widget.copy_path, qt.SIGNAL("clicked()"), __.slot_change_path)
		qt.qApp.connect(__.fuz_bout, qt.SIGNAL("clicked()"), __.slot_fuz)

	def ouvrir(__, bout=True):
		if bout: __.path = unicode(qt.QFileDialog.getOpenFileName(__, "Ouvrir fichier", get_path(sys.argv[0])*bool(not __.path)+__.path), "cp1252")
		if __.path:
			__.file_path.setText(get_path(__.path))
			__.file_name.setText(get_name(__.path))
			if get_ext(__.path) != "cut":
				__.size = file(__.path).size(True)
				size = conv_oct(__.size)
				__.file_size.setText(size)
				__.widget.groupbox1.part_unit[["o", "ko","mo", "go"].index(size.split(" ")[-1].lower())].setChecked(True)
				__.widget.copy_path.setText(get_path(__.path))
				__.widget.copy_name.setText(get_name(__.path))
				__.ok_bout.setText("Couper")
				__.groupbox.setTitle("Fichier à coupé:")
				__.widget2.setVisible(False)
				__.widget.setVisible(True)
			else:
				__.file_size.setText("")
				__.widget2.copy_path.setText("/".join(__.path.split("/")[:-2])+"/")
				__.widget2.copy_name.setText("~".join(get_name(__.path).split("~")[:-1]))
				__.ok_bout.setText("Recoller")
				__.groupbox.setTitle("Fichier à recollé:")
				__.widget.setVisible(False)
				__.widget2.setVisible(True)
				if get_ext(__.widget2.copy_name.text()) == "fuz": __.widget2.checkbox.setVisible(True)
				else: __.widget2.checkbox.setVisible(False)

	def slot_fuz(__):
		__.path = qt.QFileDialog.getExistingDirectory(__, "Choix du dossier à fusionner")
		if __.path:
			__.path = fusion_dirfile([unicode(__.path, "cp1252")])
			__.fuz = True
			__.ouvrir(False)

	def slot_change_path(__):
		path = qt.QFileDialog.getExistingDirectory(__, "Choix du dossier dans lequel sera recollé le fichier")
		__.widget2.copy_path.setText(path)
		__.widget.copy_path.setText(path)

	def slot_groupbox(__, num=False):
		if num:
			__.widget.groupbox1.setChecked(not __.widget.groupbox1.isChecked())
			__.widget.groupbox2.setChecked(not __.widget.groupbox1.isChecked())
		else:
			__.widget.groupbox2.setChecked(not __.widget.groupbox2.isChecked())
			__.widget.groupbox1.setChecked(not __.widget.groupbox2.isChecked())

	def slot_couper(__):
		if __.ok_bout.text() == "Couper":
			if __.widget.groupbox1.isChecked(): taille = __.widget.groupbox1.part_size.text()
			else: taille = __.widget.groupbox2.nbr_part.text()

			if taille != "":
				taille = int(taille)
				if __.widget.groupbox1.isChecked():
					for i in __.widget.groupbox1.part_unit:
						if i.isChecked(): unit = str(i.text()); break
				else: unit = ""
			else: taille = 0

			if taille:
				name = ""
				if __.widget.copy_path.text(): name += unicode(__.widget.copy_path.text(), "cp1252")
				else: name += get_path(__.file_path.text())
				if __.widget.copy_name.text(): name += unicode(__.widget.copy_name.text(), "cp1252")
				else: name += unicode(__.file_name.text(), "cp1252")
				cut_file(__.path, name, taille, unit, __.widget.groupbox1.split.isChecked(), __)
				if __.fuz: remove(__.path)
		elif __.ok_bout.text() == "Recoller":
			path = ""
			if __.widget2.copy_path.text(): path += __.widget2.copy_path.text()
			if __.widget2.copy_name.text(): path += __.widget2.copy_name.text()
			file_name = stick_file(__.path, __, unicode(path, "cp1252"),
								__.widget2.groupbox.isChecked(), __.widget2.groupbox.checkbox.isChecked())
			if __.widget2.checkbox.isVisible() and __.widget2.checkbox.isChecked() and get_ext(file_name) == "fuz":
				defusion(file_name)
				remove(file_name)
