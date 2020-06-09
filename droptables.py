import pickle

#Root
#|-Missions
#  |_<list elem>
#     |-Type str
#     |-Tier ?
#     |-Ignore ?
#     |-Rewards dict
#        |_ "" / "A" / "B" / "C" dict
#           |_ <list elem>
#               |_<list elem> => Objet;Type;Rate[;Amount]
#     |-Alias ?
#     |-Name ?
#     |_ShortName ?
#|-Syndicates
#|_Ennemies

class DropTableUtils():
	associationENFR = {}
	result = {}

	def init(self):
		pass

	def loadENFRAssociation(self, filename):
		with open(filename, "rb") as file:
			self.associationENFR = pickle.load(file)

	def parcoursFR(self, fileName):
		compteur = 0
		with open(fileName, "r") as file:
			test = file.read()
		self.result = test
		for mod in self.associationENFR:
			tempString = '"'+str(mod)+'"'
			tempReplacement = '"'+self.associationENFR[mod][0]+'"'
			newString = self.result.replace(tempString, tempReplacement)
			if newString != self.result:
				compteur += 1
			self.result = newString
		print("Le parcours a traduit {} mods".format(compteur))

	def saveResult(self, fileName):
		with open(fileName, "w") as file:
			file.write(self.result)



if __name__ == '__main__':
	dropTableUtils = DropTableUtils()
	dropTableUtils.loadENFRAssociation("traductionENFR.dat")
	dropTableUtils.parcoursFR("datas/droptables_fr_light.lua")
	dropTableUtils.saveResult("droptables_fr_new.lua")


