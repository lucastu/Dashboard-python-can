def isInfoMessage(data, b1 , b2, b3 ):
    # Fonction qui compare les trois bytes du premier parametre avec les trois bytes des autres parametres en omettant le premier quartet et le dernier
    return (data[0] & 0b00001111) == b1 & (data[1] & 0b11111111) == b2 & (data[2] & 0b11110000) == (b3 & 0b11110000)

def parseInfoMessage(data, root):
    infomessage = "none"
    if isInfoMessage(data, 0x01, 0x2F, 0xC4):
        infomessage = "Essuie-vitre automatique activÃ©"
    elif isInfoMessage(data, 0x01, 0x30, 0xC4):
        infomessage = "Essuie-vitre automatique dÃ©sactivÃ©"
    elif isInfoMessage(data, 0x01, 0x31, 0xC4):
        infomessage = "Allumage automatique des projecteurs activÃ©"
    elif isInfoMessage(data, 0x01, 0x32, 0xC4):
        infomessage = "Allumage automatique des projecteurs dÃ©sactivÃ©"
    elif isInfoMessage(data, 0x01, 0x33, 0xC4):
        infomessage = "Auto-verrouillage des portes activÃ©"
    elif isInfoMessage(data, 0x01, 0x34, 0xC4):
        infomessage = "Auto-verrouillage des portes dÃ©activÃ©"
    elif isInfoMessage(data, 0x01, 0x37, 0xC4):
        infomessage = "SÃ©curitÃ© enfant activÃ©e"
    elif isInfoMessage(data, 0x01, 0x38, 0xC4):
        infomessage = "SÃ©curitÃ© enfant dÃ©sactivÃ©e"
    elif isInfoMessage(data, 0x01, 0x3D, 0xC4):
        infomessage = "Stationnement NON (cf photo)"
    elif isInfoMessage(data, 0x01, 0x98, 0xC4):
        infomessage = "SystÃ¨me STOP START dÃ©faillant"
    elif isInfoMessage(data, 0x01, 0xF6, 0xC4):
        infomessage = "Manoeuvre toit impossible: tÂº ext. trop faible"
    elif isInfoMessage(data, 0x01, 0xF7, 0xC4):
        infomessage = "Manoeuvre toit impossible: vitesse trop Ã©levÃ©e"
    elif isInfoMessage(data, 0x01, 0xF8, 0xC4):
        infomessage = "Manoeuvre toit impossible: coffre ouvert"
    elif isInfoMessage(data, 0x01, 0xFA, 0xC4):
        infomessage = "Manoeuvre toit impossible: rideau coffre non dÃ©ployÃ©"
    elif isInfoMessage(data, 0x01, 0xFB, 0xC4):
        infomessage = "Manoeuvre toit terminÃ©e"
    elif isInfoMessage(data, 0x01, 0xFC, 0xC4):
        infomessage = "Terminer immÃ©diatement la manoeuvre de toit"
    elif isInfoMessage(data, 0x01, 0xFD, 0xC4):
        infomessage = "Manoeuvre impossible: toit verrouillÃ©"
    elif isInfoMessage(data, 0x01, 0xFE, 0xC4):
        infomessage = "MÃ©canisme toit escamotable dÃ©faillant"
    elif isInfoMessage(data, 0x01, 0xFF, 0xC4):
        infomessage = "Manoeuvre impossible: lunette ouverte"
    elif isInfoMessage(data, 0x00, 0x00, 0xC8):
        infomessage = "Diagnostic OK"
    elif isInfoMessage(data, 0x00, 0x01, 0xC8):
        infomessage = "STOP: dÃ©faut tempÃ©rature moteur, arrÃªtez le vÃ©hicule"
    elif isInfoMessage(data, 0x00, 0x03, 0xC8):
        infomessage = "Ajustez niveau liquide de refroidissement"
    elif isInfoMessage(data, 0x00, 0x04, 0xC8):
        infomessage = "Ajustez le niveau d'huile moteur"
    elif isInfoMessage(data, 0x00, 0x05, 0xC8):
        infomessage = "STOP: dÃ©faut pression huile moteur, arrÃªtez le vÃ©hicule"
    elif isInfoMessage(data, 0x00, 0x08, 0xC8):
        infomessage = "STOP: systÃ¨me de freinage dÃ©faillant"
    elif isInfoMessage(data, 0x00, 0x0A, 0xC8):
        infomessage = "Demande non permise (cf photo)"
    elif isInfoMessage(data, 0x00, 0x0D, 0xC8):
        infomessage = "Plusieurs roues crevÃ©es"
    elif isInfoMessage(data, 0x00, 0x0F, 0xC8):
        infomessage = "Risque de colmatage filtre Ã  particules: consultez la notice"
    elif isInfoMessage(data, 0x00, 0x11, 0xC8):
        infomessage = "Suspension dÃ©faillante, vitesse max 90km/h"
    elif isInfoMessage(data, 0x00, 0x12, 0xC8):
        infomessage = "Suspension dÃ©faillante"
    elif isInfoMessage(data, 0x00, 0x13, 0xC8):
        infomessage = "Direction assistÃ©e dÃ©faillante"
    elif isInfoMessage(data, 0x00, 0x14, 0xC8):
        infomessage = "WTF?"
    elif isInfoMessage(data, 0x00, 0x61, 0xC8):
        infomessage = "Frein de parking serrÃ©"
    elif isInfoMessage(data, 0x00, 0x62, 0xC8):
        infomessage = "Frein de parking desserrÃ©"
    elif isInfoMessage(data, 0x00, 0x64, 0xC8):
        infomessage = "Commande frein de parking dÃ©faillante, frein de parking auto activÃ©"
    elif isInfoMessage(data, 0x00, 0x67, 0xC8):
        infomessage = "Plaquettes de frein usÃ©es"
    elif isInfoMessage(data, 0x00, 0x68, 0xC8):
        infomessage = "Frein de parking dÃ©faillant"
    elif isInfoMessage(data, 0x00, 0x69, 0xC8):
        infomessage = "Aileron mobile dÃ©faillant, vitesse limitÃ©e, consultez la notice"
    elif isInfoMessage(data, 0x00, 0x6A, 0xC8):
        infomessage = "SystÃ¨me de freinage ABS dÃ©faillant"
    elif isInfoMessage(data, 0x00, 0x6B, 0xC8):
        infomessage = "SystÃ¨me ESP/ASR dÃ©faillant"
    elif isInfoMessage(data, 0x00, 0x6C, 0xC8):
        infomessage = "Suspension dÃ©faillante"
    elif isInfoMessage(data, 0x00, 0x6D, 0xC8):
        infomessage = "STOP: direction assistÃ©e dÃ©faillante"
    elif isInfoMessage(data, 0x00, 0x6E, 0xC8):
        infomessage = "DÃ©faut boite de vitesse, faites rÃ©parer le vÃ©hicule"
    elif isInfoMessage(data, 0x00, 0x6F, 0xC8):
        infomessage = "SystÃ¨me de controle de vitesse dÃ©faillant"
    elif isInfoMessage(data, 0x00, 0x73, 0xC8):
        infomessage = "Capteur de luminositÃ© ambiante dÃ©faillant"
    elif isInfoMessage(data, 0x00, 0x74, 0xC8):
        infomessage = "Ampoule feu de position dÃ©faillante"
    elif isInfoMessage(data, 0x00, 0x75, 0xC8):
        infomessage = "RÃ©glage automatique des projecteurs dÃ©faillant"
    elif isInfoMessage(data, 0x00, 0x76, 0xC8):
        infomessage = "Projecteurs directionnels dÃ©faillants"
    elif isInfoMessage(data, 0x00, 0x78, 0xC8):
        infomessage = "Airbag(s) ou ceinture(s) Ã  prÃ©tensionneur(s) dÃ©faillant(s)"
    elif isInfoMessage(data, 0x00, 0x7A, 0xC8):
        infomessage = "DÃ©faut boite de vitesse, faites rÃ©parer le vÃ©hicule"
    elif isInfoMessage(data, 0x00, 0x7B, 0xC8):
        infomessage = "Pied sur frein et levier en position \"N\" nÃ©cessaires"
    elif isInfoMessage(data, 0x00, 0x7D, 0xC8):
        infomessage = "PrÃ©sence d'eau dans le filtre Ã  gasoil, faites rÃ©parer le vÃ©hicule"
    elif isInfoMessage(data, 0x00, 0x7E, 0xC8):
        infomessage = "DÃ©faut moteur, faites rÃ©parer le vÃ©hicule"
    elif isInfoMessage(data, 0x00, 0x7F, 0xC8):
        infomessage = "DÃ©faut moteur, faites rÃ©parer le vÃ©hicule"
    elif isInfoMessage(data, 0x00, 0x81, 0xC8):
        infomessage = "Niveau additif FAP trop faible, faites rÃ©parer le vÃ©hicule"
    elif isInfoMessage(data, 0x00, 0x83, 0xC8):
        infomessage = "Antivol Ã©lectronique dÃ©faillant"
    elif isInfoMessage(data, 0x00, 0x88, 0xC8):
        infomessage = "SystÃ¨me aide au stationnement dÃ©faillant"
    elif isInfoMessage(data, 0x00, 0x89, 0xC8):
        infomessage = "SystÃ¨me de mesure de place dÃ©faillant"
    elif isInfoMessage(data, 0x00, 0x8A, 0xC8):
        infomessage = "Charge batterie ou alimentation Ã©lectrique dÃ©faillante"
    elif isInfoMessage(data, 0x00, 0x8D, 0xC8):
        infomessage = "Pression pneumatiques insuffisante"
    elif isInfoMessage(data, 0x00, 0x97, 0xC8):
        infomessage = "SystÃ¨me d'alerte de franchissement de ligne dÃ©faillant"
    elif isInfoMessage(data, 0x00, 0x9A, 0xC8):
        infomessage = "Ampoule feu de croisement dÃ©faillante"
    elif isInfoMessage(data, 0x00, 0x9B, 0xC8):
        infomessage = "Ampoule feu de route dÃ©faillante"
    elif isInfoMessage(data, 0x00, 0x9C, 0xC8):
        infomessage = "Ampoule feu stop dÃ©faillante"
    elif isInfoMessage(data, 0x00, 0x9D, 0xC8):
        infomessage = "Ampoule anti-brouillard dÃ©faillante"
    elif isInfoMessage(data, 0x00, 0x9E, 0xC8):
        infomessage = "Clignotant dÃ©faillant"
    elif isInfoMessage(data, 0x00, 0x9F, 0xC8):
        infomessage = "Ampoule feu de recul dÃ©faillante"
    elif isInfoMessage(data, 0x00, 0xA0, 0xC8):
        infomessage = "Ampoule feu de position dÃ©faillante"
    elif isInfoMessage(data, 0x00, 0xCD, 0xC8):
        infomessage = "RÃ©gulation de vitesse impossible: vitesse trop faible"
    elif isInfoMessage(data, 0x00, 0xCE, 0xC8):
        infomessage = "Activation du rÃ©gulateur impossible: saisir la vitesse"
    elif isInfoMessage(data, 0x00, 0xD2, 0xC8):
        infomessage = "Ceintures AV non bouclÃ©es"
    elif isInfoMessage(data, 0x00, 0xD3, 0xC8):
        infomessage = "Ceintures passagers AR bouclÃ©es"
    elif isInfoMessage(data, 0x00, 0xD7, 0xC8):
        infomessage = "Placer boite automatique en position P"
    elif isInfoMessage(data, 0x00, 0xD8, 0xC8):
        infomessage = "Risque de verglas"
    elif isInfoMessage(data, 0x00, 0xD9, 0xC8):
        infomessage = "Oubli frein Ã  main !"
    elif isInfoMessage(data, 0x00, 0xDE, 0xC8) or isInfoMessage(data, 0x00, 0x0B, 0xC8):
    # Car doors frame
        doorByte1 = data[3]
        doorByte2 = data[4]
    
        if doorByte1 & 0b00000100 == 0b00000100:
            # decodedCarDoors.insert(.Hood)
            print("Capot ouvert")
        if doorByte1 & 0b00001000 == 0b00001000:
            # decodedCarDoors.insert(.Trunk)
            print("Coffre ouvert")
        if doorByte1 & 0b00010000 == 0b00010000:
            # decodedCarDoors.insert(.RearLeft)
            print("porte arriÃ¨re gauche ouverte")
        if doorByte1 & 0b00100000 == 0b00100000:
            # decodedCarDoors.insert(.RearRight)
            print("porte arriÃ¨re droite ouverte")
        if doorByte1 & 0b01000000 == 0b01000000:
            # decodedCarDoors.insert(.FrontLeft)
            print("porte conducteur ouverte")
        if doorByte1 & 0b10000000 == 0b10000000:
            # decodedCarDoors.insert(.FrontRight)
            print("porte passager ouverte")
        if doorByte2 & 0b01000000 == 0b01000000:
            # decodedCarDoors.insert(.FuelFlap)
            print("trappe essence ouverte")

    elif isInfoMessage(data, 0x00, 0xDF, 0xC8):
        infomessage = "Niveau liquide lave-glace insuffisant"
    elif isInfoMessage(data, 0x00, 0xE0, 0xC8):
        infomessage = "Niveau carburant faible"
    elif isInfoMessage(data, 0x00, 0xE1, 0xC8):
        infomessage = "Circuit de carburant neutralisÃ©"
    elif isInfoMessage(data, 0x00, 0xE3, 0xC8):
        infomessage = "Pile tÃ©lÃ©commande plip usagÃ©e"
    elif isInfoMessage(data, 0x00, 0xE5, 0xC8):
        infomessage = "Pression pneumatique(s) non surveillÃ©e"
    elif isInfoMessage(data, 0x00, 0xE7, 0xC8):
        infomessage = "Vitesse Ã©levÃ©e, vÃ©rifier si pression pneumatiques adaptÃ©e"
    elif isInfoMessage(data, 0x00, 0xE8, 0xC8):
        infomessage = "Pression pneumatique(s) insuffisante"
    elif isInfoMessage(data, 0x00, 0xEB, 0xC8):
        infomessage = "La phase de dÃ©marrage a Ã©chouÃ© (consulter la notice)"
    elif isInfoMessage(data, 0x00, 0xEC, 0xC8):
        infomessage = "DÃ©marrage prolongÃ© en cours"
    elif isInfoMessage(data, 0x00, 0xEF, 0xC8):
        infomessage = "TÃ©lÃ©commande non dÃ©tectÃ©e"
    elif isInfoMessage(data, 0x00, 0xF0, 0xC8):
        infomessage = "Diagnostic en cours"
    elif isInfoMessage(data, 0x00, 0xF1, 0xC8):
        infomessage = "Diagnostic terminÃ©"
    elif isInfoMessage(data, 0x00, 0xF7, 0xC8):
        infomessage = "Ceinture passager AR gauche dÃ©bouclÃ©e"
    elif isInfoMessage(data, 0x00, 0xF8, 0xC8):
        infomessage = "Ceinture passager AR central dÃ©bouclÃ©e"
    elif isInfoMessage(data, 0x00, 0xF9, 0xC8):
        infomessage = "Ceinture passager AR droit dÃ©bouclÃ©e"
    else:
        infomessage = "Aucun message"
    root.InfoMSG.setText(infomessage)
