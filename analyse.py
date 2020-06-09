import slpp

def loadFile(filename):
	with open(filename, "r") as file:
		test = file.read()
		#print(test)
		theTree = slpp.slpp.decode(test)
	return theTree

def parcoursFR(tree):
	modTable = tree['Mods']
	rez = {"nontraduits": [], "traduits": [], "sansimage": []}
	listeModsEN = []
	indexModFR = [] # juste une liste
	indexModENFR = {} # Association EN -> FR

	attrList = set()

	for modName in modTable.keys():
		mod = modTable[modName]
		listeModsEN.append(mod["NameEN"])
		indexModFR.append(modName)
		indexModENFR[mod["NameEN"]] = modName
		for attr in mod.keys():
			attrList.add(attr)
			if (attr == "Polariy"):
				print(modName)
		# print(modName, end="")
		if (modName == mod["Name"]):
			if (mod["Image"] is None):
				rez["traduits"].append(modName)
				# print(" : traduit; sans image")
			else:
				rez["sansimage"].append(modName)
				# print(" : traduit; avec image")
		else:
			rez["nontraduits"].append(modName)
			# print(" : non traduit")
	print("Liste des attributs : {}".format(attrList))
	return rez, listeModsEN, indexModFR, indexModENFR
	# print(type(tree['Mods']))


def parcoursEN(treeEN, treeFR, rezFR, indexModsFR, indexModsFR_EN):
	blacklistAttribut = ["Image", "Traits", "WeaponAugment", "WarframeAugment", "NameEN", "Name", "Link", "Family", "Stance", "Set", "Archived"]
	modTableEN = treeEN['Mods']
	modTableFR = treeFR['Mods']
	rez = {}
	listeModsEN = []
	for modNameEN in modTableEN.keys(): # Pour chaque mod de la table anglaise
		modEN = modTableEN[modNameEN] # Je récupère le mod concerné (EN)
		listeModsEN.append(modEN["Name"]) # J'ajoute son nom à la liste des mods étudiés
		if modNameEN in indexModsFR_EN: # Si ce mod existe dans la table française
			nomFR = indexModsFR_EN[modNameEN] # Je récupère son nom français
			rez[nomFR] = modTableFR[nomFR] # Je récupère le mod concerné (FR)
			for attribut in modTableEN[modNameEN].keys(): # Pour chaque attribut anglais du mod (EN)
				if attribut not in rez[nomFR]: # Si l'attribut n'existe pas sur la version française
					rez[nomFR][attribut] = modTableEN[modNameEN][attribut] # J'ajoute l'attribut et sa valeur dans la version française
				else: # Si cet attribut existe déjà sur la version française
					if attribut not in blacklistAttribut: # Si cet attribut n'est pas blacklisté (attributs spécifiques au wiki FR)
						rez[nomFR][attribut] = modTableEN[modNameEN][attribut] # On met à jour sa valeur
		else: # Si ce mod n'est pas dans la table française
			rez[modNameEN] = modEN # J'ajoute les informations anglaises dans la table française
	return rez, listeModsEN
	# print(type(tree['Mods']))

if __name__ == '__main__':
	treeFR = loadFile("modsData_light.lua")
	rezFR, listeFRModsEN, indexModFR, indexModENFR = parcoursFR(treeFR)
	if len(set(listeFRModsEN)) != len(listeFRModsEN):
		print("Attention, la liste des mods français contient des doublons en anglais")
	treeEN = loadFile("modsData_en_light.lua")
	rezEN, listeENModsEN = parcoursEN(treeEN, treeFR, rezFR, indexModFR, indexModENFR)
	print(listeFRModsEN)
	print(listeENModsEN)
	print(rezEN)
