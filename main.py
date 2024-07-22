import logging, unicodedata
from datetime import datetime
from telegram import Update
from telegram.ext import filters, ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def getGroupID(alias):
    alias = stripAccents(alias.lower())
    for key, val in aliasesDict.items():
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
    return dicty

def writeTextFile(foutname, dicty):
    ### Aquesta funció escriu el diccionari a l'arxiu corresponent
    with open(foutname, "w") as file:
        file.write("GroupID,aliases...\n")
        for x in dicty:
            line = str(x) + "," +",".join(dicty[x]) + "\n"
            file.write(line)

def validAlias(aliasList):
    validList = list()
    for paraula in aliasList:
        if getGroupID(paraula) != -1: continue #evitem duplicats
        if not paraula.replace("_","").isalnum(): continue #només acceptam caracters alfanumèrics i barres baixes
        validList.append(paraula)
    return validList
        
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    textMess1 = """Hola! Benvingut al SplitBot, el bot restador de proves per a la Telecogresca.
Ara per ara, només té una sola funció: enviar missatges directes a altres grups.
No obstant, estigueu atents, perquè arribaran més eines per a poder sumar i restar al Telegram!"""
    textMess2 = """Instruccions disponibles:
- /start: inicialitzar el bot i tornar a rebre això.
- /help: informació i ajuda per a enviar i rebre missatges
- /msg: enviar un missatge a un altre grup
- /addAlias: afegir un àlies per a un grup perquè s'hi puguin enviar i rebre missatges.
- /rmAlias: eliminar un àlies per a un grup
- /lsAlias: veure tots els grups enregistrats i els seus àlies"""
    
    await context.bot.send_message(chat_id=update.effective_chat.id, text=textMess1)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=textMess2)

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    textMess1 = """Hola! Per a poder enviar o rebre missatges amb el bot, abans necessites complir uns requisits:
1. El bot ha d'estar teu grup, i ser administrador. Basta amb que el bot tingui 1 poder d'admin i que aparegui al llistat d'admins. Això és un requisit de Telegram per als bots.
2. El teu grup ha de tenir, com a mínim, un sol àlies. Els àlies són com el nom d'usuari del teu grup. Per exemple, el grup d'IT té d'àlies "IT".
 - Pots afegit un o múltiples àlies usant la instrucció /addAlias. Per exemple, /addAlias FDD FestaDeDia afegirà dos àlies al grup Festa de Dia.
 - Si vols eliminar un àlies, pots usar la instrucció /rmAlias. Per exemple, en el cas anterior, si faig /rmAlias FDD, només em quedarà l'àlies 'FestaDeDia'. 
 - Els àlies han de ser una sola paraula d'almenys 2 caràcters. Han de ser lletres, números o barres baixes.
 - No es distingeixen minúscules, majúscules o accents, és a dir, "açò" i "Acò" es consideraran el mateix (encara que es mostrarà el 1r).
 - No poden estar duplicats.
 - Només pots modificar els àlies d'un grup des de dintre del grup. No cal ser administrador.
 - Si fas servir /addAlias o /rmAlias sense cap altre paraula, obtindràs una llista dels àlies al grup actual.
 - Amb el comandament /lsAlias, podràs veure tots els grups enregistrats i els seus àlies.
    """
    textMess2 = """De moment, només es poden enviar missatges de text (encara que poden contenir qualsevol símbol o emoji). Per a fer-ho, utilitza la instrucció /msg alies missatge.
Per exemple, si des del grup de FdD vull enviar un missatge a l'EGK, faré:
    /msg EGK Hola! Això és un missatge de prova
I s'enviarà el missatge inmediatament, amb la data i la firma de la persona que l'escriu. En un futur també es podran programar missatges."""
    textMess3 = """Instruccions disponibles:
 - /start: incialitzar el bot i rebre una mica d'informació
 - /help: informació i ajuda per a enviar i rebre missatges
 - /msg: enviar un missatge a un altre grup
 - /addAlias: afegir un àlies per a un grup perquè s'hi puguin enviar i rebre missatges.
 - /rmAlias: eliminar un àlies per a un grup
 - /alias: veure tots els grups enregistrats i els seus àlies"""
    await context.bot.send_message(chat_id=update.effective_chat.id, text=textMess1)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=textMess2)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=textMess3)
             
async def addAlias(update:Update, context: ContextTypes.DEFAULT_TYPE):
    alias = [x.strip() for x in context.args]
    alias = validAlias(alias)
    groupID = update.effective_chat.id
    if alias.__len__() < 1:
        if groupID in aliasesDict: messText = "No s'han fet canvis. Àlies actuals per a aquest grup\n  - " + "\n  - ".join(aliasesDict[update.effective_chat.id])
        else: messText = "No hi ha àlies configurats per a aquest grup. Usa '/addAlias alias' per a afegir un àlies."
    else:
        if groupID in aliasesDict: #Si ja existeix aquest grup:
            aliasesDict[groupID].extend(alias)
        else: #si no, la cream
            aliasesDict[groupID] = list()
            aliasesDict[groupID].extend(alias)
        messText = "Afegit un àlies. Àlies actuals per a aquest grup\n  - " + "\n  - ".join(aliasesDict[update.effective_chat.id])
    writeTextFile("data.txt",aliasesDict)
    print(aliasesDict)
    await context.bot.send_message(chat_id=update.effective_chat.id, text = messText)

async def rmAlias(update:Update, context: ContextTypes.DEFAULT_TYPE):
    aEliminar = [stripAccents(x.strip().lower()) for x in context.args]
    groupID = update.effective_chat.id
    if not(groupID in aliasesDict):  # Comprovem si existeixen àlies per al grup actual
        textMess = "No hi ha cap àlies configurat per a aquest grup."
        await context.bot.send_message(chat_id=update.effective_chat.id, text = textMess)
        return
    if aEliminar.__len__() < 1: # Comprovem si hi ha algun argument. Si no n'hi ha, retornem la llista d'alies
        textMess = "No s'han fet canvis. Àlies actuals per a aquest grup\n  - " + "\n  - ".join(aliasesDict[update.effective_chat.id])
        await context.bot.send_message(chat_id=update.effective_chat.id, text = textMess)
        return

    # Ara, amb un loop 'for' mirarem per a cada paraula que s'ha sol·licitat eliminar, si és possible, i si ho és, ho fem i donem el resultat
    textMess = ""
    for paraula in aEliminar:
        existents = [stripAccents(x.lower()) for x in aliasesDict[groupID]] # obtenim els alias existents per a un grup
        if paraula in existents: # si existeix, la eliminem
            aliasesDict[groupID].pop(existents.index(paraula))
            textMess += "\n- Àlies '" + paraula + "' eliminat."
        else: textMess += "\n- Alies '" + paraula + "' no existeix" #si no, avissem a l'usuari
    
    if aliasesDict[groupID].__len__() < 1: #un cop acabats, comprovem si quede algun àlies al grup
        aliasesDict.pop(groupID)
        textMess += "\nJa no queden àlies per a aquest grup"
    
    writeTextFile("data.txt",aliasesDict)
    textMess += "\nFes servir '/addAlias o /rmAlias sense arguments per a veure la llista d'àlies."
    await context.bot.send_message(chat_id=update.effective_chat.id, text = textMess)

async def lsAlias(update:Update, context: ContextTypes.DEFAULT_TYPE):
    textMess = "Aquests són tots els àlies existents. Fes servir /addAlias o /rmAlias per a afegir-ne o eliminar-ne.\nNomés pots fer-ho des de dintre del grup pertanyent a l'àlies."
    for x in aliasesDict:
        aliasList =  ", ".join(aliasesDict[x])
        textMess += "\n - " + aliasList
        if update.effective_chat.id == x: textMess += " (grup actual)"
    if not(update.effective_chat.id in aliasesDict): textMess +="\n El grup actual no té cap àlies."
    await context.bot.send_message(chat_id=update.effective_chat.id, text = textMess)

async def msg(update:Update, context: ContextTypes.DEFAULT_TYPE):
    if not(update.effective_chat.id in aliasesDict): # Comprovem que el remitent té un àlies
        textMess = "No hi ha cap àlies configurat per a aquest grup.\nAbans d'enviar un missatge, afegeix-ne un amb '/addAlias.\nPer a més informació, fes servir /help."
        await context.bot.send_message(chat_id=update.effective_chat.id, text = textMess)
        return # Acabem això
    if context.args.__len__()<2: # Comprovem que s'ha introduït remitent i missatge
        textMess = "Format incorrecte. Fes servir:\n   /msg alies text\nsubstituint 'alies' pel destinatari"
        await context.bot.send_message(chat_id=update.effective_chat.id, text = textMess)
        return
    
    # Processem el text rebut per a obtenir el cos del missatge i l'àlies del destinatari
    textRebut = update.message.text.strip()
    textRebut = textRebut[textRebut.find(" "):].strip() #Eliminem el comandament
    aliesDestinatari = textRebut[0:textRebut.find(" ")].strip() #agafem la primera paraula (el destinatari)
    aliesRemitent = aliasesDict[update.effective_chat.id]
    cos = textRebut[textRebut.find(" "):].strip() # Eliminem el destinatari, ens queda el cos

    IDestinatari = getGroupID(aliesDestinatari)
    if IDestinatari == -1: # Comprovem que el destinatari existeix
        textMess = "Aquest àlies no està enregistrat! Fes servir '/lsAlias' per a veure quins existeixen" # Error!
        await context.bot.send_message(chat_id=update.effective_chat.id, text = textMess)
        return
    
    # Si tot va bé, "montam" el missatge i l'enviem
    now = datetime.now()
    header = "Missatge de {} per a {}: \n\n ".format(str(aliesRemitent[0]), aliesDestinatari)
    foot = "\n\nFirmat: {} el {} a les {}.".format(update.effective_sender.name, now.strftime('%d/%m/%Y'), now.strftime('%X'))
    textMess = header + cos + foot
    await context.bot.send_message(chat_id=IDestinatari, text = textMess) # Enviem el missatge al destinatari
    await context.bot.send_message(chat_id=update.effective_chat.id, text = textMess) # En qualsevol cas, avissem al remitent

    
if __name__ == '__main__':
    aliasesDict = readTextFile("data.txt")  # Llegim l'arxiu de text per a obtenir tots els àlies
    print("S'ha llegit el fitxer de dades: ")
    print(aliasesDict)
    
    with open("TOKEN.txt") as tokenFile:
        token = tokenFile.readline()
    token = token[1:-1]

    app = ApplicationBuilder().token(token).build()
    
    start_handler = CommandHandler('start', start)
    help_handler = CommandHandler('help', help)
    addAlias_handler = CommandHandler(['add','addAlias','aAlias','adAlias','newAlias', 'addAlies','aAlies','adAlies','newAlies'], addAlias)
    rmAlias_handler = CommandHandler(['rmAlias','rm', 'delAlias', 'elAlias', 'elAlies','rmAlies','delAlies'], rmAlias)
    lsAlias_handler = CommandHandler(['alias', 'alies','al', 'ls','lsAlias','lsAlies'],lsAlias)
    msg_handler = CommandHandler(['send','msg','ms','mg'],msg)

    
    app.add_handler(start_handler)
    app.add_handler(help_handler)
    app.add_handler(rmAlias_handler)
    app.add_handler(addAlias_handler)
    app.add_handler(lsAlias_handler)
    app.add_handler(msg_handler)

    
    app.run_polling()