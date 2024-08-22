import unicodedata, datetime


def getGroupID(alias, dicty):
    alias = stripAccents(alias.lower())
    for key, val in dicty.items():
        for paraula in val:
            paraula = stripAccents(paraula.lower())
            if paraula.lower() == alias.lower(): return key
    return -1 # Si no existeix aquest alies

def stripAccents(s):
   return ''.join(c for c in unicodedata.normalize('NFD', s)
                  if unicodedata.category(c) != 'Mn')
   
   
def readTextFile(finName):
    ### Aquesta funció llegeix l'arxiu a finName i retorna un diccionari amb els àlies
    dicty = dict()
    with open(finName, "r") as file:
        file.readline() # Ignorem la primera línia
        for line in file:
            line = line.split(",")
            line = [x.strip() for x in line]
            groupID = int(line[0].strip())
            alias = line[1:]
            if groupID in dicty: # Si la entrada ja existeix al diccionari,
                print("ALERTA: ID repetida... algú ha editat manualment l'arxiu? Aquesta entrada serà ignorada-> Avisa a IT\n" + line)
            else:
                dicty[groupID] = list()
                for x in alias: dicty[groupID].append(x)
    now = datetime.datetime.now()
    print("{} - {} S'ha llegit l'arxiu '{}' amb èxit".format(now.strftime('%d/%m/%Y'), now.strftime('%X'), finName))
    print(dicty)
    return dicty

def writeTextFile(foutname, dicty):
    ### Aquesta funció escriu el diccionari a l'arxiu corresponent
    with open(foutname, "w") as file:
        file.write("GroupID,aliases...\n")
        for x in dicty:
            line = str(x) + "," +",".join(dicty[x]) + "\n"
            file.write(line)
    now = datetime.now()
    print("{} - {} S'ha actualitzat l'arxiu '{}' amb èxit".format(now.strftime('%d/%m/%Y'), now.strftime('%X'), foutname))
    print(dicty)

def validAlias(aliasList):
    validList = list()
    for paraula in aliasList:
        if getGroupID(paraula) != -1: continue #evitem duplicats
        if not paraula.replace("_","").isalnum(): continue #només acceptam caracters alfanumèrics i barres baixes
        validList.append(paraula)
    return validList

def readCumFile(finName):
        ### Aquesta funció llegeix l'arxiu a finName i retorna un diccionari amb els cumples
    dicty = dict()
    with open(finName, "r") as file:
        file.readline() # Ignorem la primera línia
        for line in file:
            line = line.split(",")
            line = [x.strip() for x in line]

            mote = line[0]
            cumInt = [int(x) for x in line[1].split("-")]
            cumple = datetime.date(cumInt[2], cumInt[1], cumInt[0])
            
            dicty[mote] = cumple
    now = datetime.datetime.now()
    print("{} - {} S'ha llegit l'arxiu '{}' amb èxit".format(now.strftime('%d/%m/%Y'), now.strftime('%X'), finName))
    return dicty