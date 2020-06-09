import collections
import slpp




class ModUtils():
	listeModsFR = {}
	associationENFR = {}
	classementMods = {"nontraduits": [], "traduits": [], "sansimage": [], "ajoutesEN": [], "erreurTraduction": [], "sansNomEN": []}
	nouvelleListe = {}

	# blacklistAttribut = ["Image", "Traits", "WeaponAugment", "WarframeAugment", "NameEN", "Name", "Link", "Family",
	#                      "Stance", "Set", "Archived", "Link"]
	# Je laisse ça, en attendant
	whitelistAttributs = ['PvP', 'Introduced', 'Transmutable'] # 'Rarity', 'Polarity',
	# Traduction de la rareté
	rarityTraduction = {}
	rarityTraduction["Uncommon/Rare"] = "Rare"  # Cas particulier de "Focus Critique" (erreur du wiki EN)
	rarityTraduction["Peculiar"] = "Atypique"
	rarityTraduction["Common"] = "Commun"
	rarityTraduction["Common < br > Uncommon < br > Rare"] = "Commun<br>Inhabituel<br>Rare"
	rarityTraduction["Rare"] = "Rare"
	rarityTraduction["Legendary"] = "Légendaire"
	rarityTraduction["Uncommon"] = "Inhabituel"
	rarityTraduction["Amalgam"] = "Amalgame"
	rarityTraduction["N/A"] = "Commun"  # Cas spécial des stances exaltées => Commun par convention
	polarityTraduction = {}
	polarityTraduction["N/A"] = "Aucune"
	polarityTraduction["None"] = "Aucune"
	polarityTraduction["Ward"] = "Unairu"
	polarityTraduction["Sentinel"] = "Penjaga"
	polarityTraduction["Naramon/Madurai"] = "Madurai"  # Cas particulier de "Focus Critique" (erreur du wiki EN)


	def __init__(self):
		pass

	def parcoursFR(self, fileName):
		with open(fileName, "r") as file:
			test = file.read()
			tree = slpp.slpp.decode(test)
		tableMods = tree['Mods']

		compteurDoublons = 0

		for nomMod in tableMods.keys():  # Pour chaque mod dans la table française
			modActuel = tableMods[nomMod] # Je récupère le mod
			result = self.addModFR(nomMod, modActuel, force=True) # J'ajoute le mod à la base
			if not result: # Ce mod a un nom anglais qui était déjà dans la base
				compteurDoublons += 1 # C'est donc un doublon
		print("Doublons rencontrés : {}".format(compteurDoublons))

	def addModFR(self, name, val, force=False):
		flag = True
		if name in self.listeModsFR:
			if not force:
				return False
			flag = False
		self.listeModsFR[name] = val
		self.nouvelleListe[name] = val
		nomEN = val["NameEN"]
		nomEN_clean = nomEN.replace(" (Stance)", "")
		if nomEN_clean is None:
			self.classementMods["sansNomEN"].append(name)
		else:
			if nomEN_clean in self.associationENFR:
				print("Attention, un mod EN ({}) est en doublon : ".format(nomEN_clean), end="")
				self.associationENFR[nomEN_clean].append(name)
				for e in self.associationENFR[nomEN_clean]:
					print(e, end="; ")
				print()
				flag = False
			else:
				self.associationENFR[nomEN_clean] = [name]

		if name == val["Name"]:
			if val["Name"] != val["Name"].strip():
				self.classementMods["erreurTraduction"].append(name)
			if val["Image"] is None:
				self.classementMods["traduits"].append(name)
			else:
				self.classementMods["sansimage"].append(name)
		else:
			self.classementMods["nontraduits"].append(name)
		return flag

	def modAnglaisPresent(self, name):
		if name in self.associationENFR:
			return self.associationENFR[name]
		return None

	def getModFR(self, name):
		if name in self.listeModsFR:
			return self.listeModsFR[name]
		return None

	def traductionAttributs(self, entreeFR, entreeEN):
		newEntree = entreeFR
		for attribut in entreeEN.keys():  # Pour chaque attribut anglais du mod (EN)
			if attribut == "Polarity": # Cas particulier des polarités
				if entreeEN[attribut] in self.polarityTraduction:
					newEntree[attribut] = self.polarityTraduction[entreeEN[attribut]]
				else:
					newEntree[attribut] = entreeEN[attribut]  # On met à jour sa valeur
			elif attribut == "Rarity": # Cas particulier des raretés
				if entreeEN[attribut] in self.rarityTraduction:
					newEntree[attribut] = self.rarityTraduction[entreeEN[attribut]]
				else:
					newEntree[attribut] = entreeEN[attribut]  # On met à jour sa valeur
			elif attribut in entreeFR:  # Si cet attribut existe déjà sur la version française
				if attribut in self.whitelistAttributs:  # Si cet attribut est whitelisté (autorisé à etre mis à jour)
					newEntree[attribut] = entreeEN[attribut]  # On met à jour sa valeur
			else:  # Si l'attribut n'existe pas sur la version française
				newEntree[attribut] = entreeEN[attribut]  # J'ajoute l'attribut et sa valeur dans la version française
		return newEntree

	def parcoursEN(self, fileName):
		with open(fileName, "r") as file:
			test = file.read()
			treeEN = slpp.slpp.decode(test)
		tableModsEN = treeEN['Mods']

		for nomModEN in tableModsEN.keys(): # Pour chaque mod de la table anglaise
			modActuelEN = tableModsEN[nomModEN] # Je récupère le mod
			nomModEN_clean = nomModEN.replace(" (Stance)", "")
			# if nomModEN != nomModEN_clean:
			# 	print("{} => {}".format(nomModEN, nomModEN_clean))
			nomModFR = self.modAnglaisPresent(nomModEN_clean)
			if nomModFR is not None: # Si le mod existe déjà dans la base de données FR
				nomModFR = nomModFR[0] # On suppose qu'il n'y en a qu'un seul
				modActuelFR = self.getModFR(nomModFR) # On récupère la version FR du mod
				self.nouvelleListe[nomModFR] = self.traductionAttributs(modActuelFR, modActuelEN)
				# self.nouvelleListe[nomModFR] = modActuelFR # On s'en sert comme base, et on met à jour ses attributs
				# for attribut in modActuelEN.keys():  # Pour chaque attribut anglais du mod (EN)
				# 	if attribut not in self.nouvelleListe[nomModFR]:  # Si l'attribut n'existe pas sur la version française
				# 		self.nouvelleListe[nomModFR][attribut] = modActuelEN[attribut]  # J'ajoute l'attribut et sa valeur dans la version française
				# 	else:  # Si cet attribut existe déjà sur la version française
				#
				# 		if attribut == "Polarity":
				# 			if modActuelEN[attribut] in self.polarityTraduction:
				# 				self.nouvelleListe[nomModFR][attribut] = self.polarityTraduction[modActuelEN[attribut]]
				# 			else:
				# 				self.nouvelleListe[nomModFR][attribut] = modActuelEN[attribut]  # On met à jour sa valeur
				# 		if attribut == "Rarity":
				# 			if modActuelEN[attribut] in self.rarityTraduction:
				# 				self.nouvelleListe[nomModFR][attribut] = self.rarityTraduction[modActuelEN[attribut]]
				# 			else:
				# 				self.nouvelleListe[nomModFR][attribut] = modActuelEN[attribut]  # On met à jour sa valeur
				# 		elif attribut in self.whitelistAttributs:  # Si cet attribut est whitelisté (autorisé à etre mis à jour)
				# 			self.nouvelleListe[nomModFR][attribut] = modActuelEN[attribut]  # On met à jour sa valeur
				# 		else:
				# 			pass
			else: # Si ce mod n'existe pas encore dans la base de données FR
				self.classementMods["ajoutesEN"].append(nomModEN_clean) # On classe ce mod dans la catégorie "ajoutes via le wiki EN"
				newMod = modActuelEN # On ajoute le mod anglais dans la base FR
				newMod['Image'] = None # On retire son image
				if "Link" in newMod:
					newMod['NameEN'] = newMod['Link']  # On change son nom en nom EN (via le lien)
				else:
					newMod['NameEN'] = newMod['Name']  # On change son nom en nom EN
				newMod['Name'] = "" # On retire son nom (pour indiquer qu'il n'est pas traduit)
				self.nouvelleListe[nomModEN_clean] = self.traductionAttributs(newMod, newMod)

	def listeAttributs(self):
		attrList = set()
		for modName in self.listeModsFR:
			mod = self.listeModsFR[modName]
			for attr in mod.keys():
				attrList.add(attr)
		print("Liste des attributs : {}".format(attrList))

	def analyseAttributs(self, attrName):
		valsPossibles = set()
		for modName in self.listeModsFR:
			mod = self.listeModsFR[modName]
			if attrName in mod:
				valsPossibles.add(mod[attrName])
		print("Valeurs possibles de l'attribut \"{}\" : ".format(attrName), end="")
		for e in valsPossibles:
			print(e, end="; ")
		print()

	def getModsWithAttributs(self, attrName, attrVal):
		print("Mods ayant l'attribut \"{}\" à la valeur \"{}\" : ".format(attrName, attrVal), end="")
		for modName in self.listeModsFR:
			mod = self.listeModsFR[modName]
			if attrName in mod:
				if mod[attrName] == attrVal:
					print(modName, end="; ")
		print()

	def getNewTable(self):
		return self.nouvelleListe

	def getClassement(self):
		return self.classementMods

	def saveNewTable(self, fileName):
		temp = {}
		tempo = sorted(self.nouvelleListe)
		for modName in tempo:
			newName = "[\""+modName+"\"]"
			temp[newName] = self.nouvelleListe[modName]
		with open(fileName, "w") as file:
			file.write(slpp.slpp.encode(temp))



if __name__ == '__main__':
	modUtils = ModUtils()
	modUtils.parcoursFR("datas/modsData_light.lua")
	# modUtils.listeAttributs()
	# modUtils.analyseAttributs("Rarity")
	# modUtils.getModsWithAttributs("Rarity", "N/A")
	# modUtils.analyseAttributs("Polarity")
	modUtils.parcoursEN("datas/modsData_en_light.lua")
	#print(modUtils.getNewTable())
	modUtils.saveNewTable("modsData_newFR_light.lua")
	classement = modUtils.getClassement()
	print("Mods non traduits :")
	print(classement["nontraduits"])
	print("Mods sans Image (ne donne que les mods avec comme image \"nil\"")
	print(classement["sansimage"])
	print("Mods Traduits")
	print(classement["traduits"])
	print("Mods ajoutés depuis le Wiki EN")
	print(classement["ajoutesEN"])
	print("Mods ayant une erreur de traduction (si vous voyez des mods listés ci-dessous, ce n'est pas normal)")
	print(classement["erreurTraduction"])
	print("Mods n'ayant pas de nom anglais (si vous voyez des mods listés ci-dessous, ce n'est pas normal)")
	print(classement["sansNomEN"])
	# modUtils.analyseAttributs("Polarity")
	# modUtils.analyseAttributs("Rarity")
	# modUtils.getModsWithAttributs("Rarity", "N/A")


