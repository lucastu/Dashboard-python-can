def parseInfoMessage(data, root) :
    infomessage = "none"
    # print("Data : %s" % data)
    if data[1] == 0x2F:
        infomessage = "Essuie-vitre automatique activÃ©"
    elif data[1] == 0x30:
        infomessage = "Essuie-vitre automatique dÃ©sactivÃ©"
    elif data[1] == 0x31:
        infomessage = "Allumage automatique des projecteurs activÃ©"
    elif data[1] == 0x32:
        infomessage = "Allumage automatique des projecteurs dÃ©sactivÃ©"
    elif data[1] == 0x33:
        infomessage = "Auto-verrouillage des portes activÃ©"
    elif data[1] == 0x34:
        infomessage = "Auto-verrouillage des portes dÃ©activÃ©"
    elif data[1] == 0x37:
        infomessage = "SÃ©curitÃ© enfant activÃ©e"
    elif data[1] == 0x38:
        infomessage = "SÃ©curitÃ© enfant dÃ©sactivÃ©e"
    elif data[1] == 0x3D:
        infomessage = "Stationnement NON (cf photo)"
    elif data[1] == 0x98:
        infomessage = "SystÃ¨me STOP START dÃ©faillant"
    elif data[1] == 0xF6:
        infomessage = "Manoeuvre toit impossible: tÂº ext. trop faible"
    elif data[1] == 0xF7:
        infomessage = "Manoeuvre toit impossible: vitesse trop Ã©levÃ©e"
    elif data[1] == 0xF8:
        infomessage = "Manoeuvre toit impossible: coffre ouvert"
    elif data[1] == 0xFA:
        infomessage = "Manoeuvre toit impossible: rideau coffre non dÃ©ployÃ©"
    elif data[1] == 0xFB:
        infomessage = "Manoeuvre toit terminÃ©e"
    elif data[1] == 0xFC:
        infomessage = "Terminer immÃ©diatement la manoeuvre de toit"
    elif data[1] == 0xFD:
        infomessage = "Manoeuvre impossible: toit verrouillÃ©"
    elif data[1] == 0xFE:
        infomessage = "MÃ©canisme toit escamotable dÃ©faillant"
    elif data[1] == 0xFF:
        infomessage = ""
    elif data[1] == 0x00:
        infomessage = "Diagnostic OK"
    elif data[1] == 0x01:
        infomessage = "STOP: dÃ©faut tempÃ©rature moteur, arrÃªtez le vÃ©hicule"
    elif data[1] == 0x03:
        infomessage = "Ajustez niveau liquide de refroidissement"
    elif data[1] == 0x04:
        infomessage = "Ajustez le niveau d'huile moteur"
    elif data[1] == 0x05:
        infomessage = "STOP: dÃ©faut pression huile moteur, arrÃªtez le vÃ©hicule"
    elif data[1] == 0x08:
        infomessage = "STOP: systÃ¨me de freinage dÃ©faillant"
    elif data[1] == 0x0A:
        infomessage = "Demande non permise (cf photo)"
    elif data[1] == 0x0D:
        infomessage = "Plusieurs roues crevÃ©es"
    elif data[1] == 0x0F:
        infomessage = "Risque de colmatage filtre Ã  particules: consultez la notice"
    elif data[1] == 0x11:
        infomessage = "Suspension dÃ©faillante, vitesse max 90km/h"
    elif data[1] == 0x12:
        infomessage = "Suspension dÃ©faillante"
    elif data[1] == 0x13:
        infomessage = "Direction assistÃ©e dÃ©faillante"
    elif data[1] == 0x14:
        infomessage = "WTF?"
    elif data[1] == 0x61:
        infomessage = "Frein de parking serrÃ©"
    elif data[1] == 0x62:
        infomessage = "Frein de parking desserrÃ©"
    elif data[1] == 0x64:
        infomessage = "Commande frein de parking dÃ©faillante, frein de parking auto activÃ©"
    elif data[1] == 0x67:
        infomessage = "Plaquettes de frein usÃ©es"
    elif data[1] == 0x68:
        infomessage = "Frein de parking dÃ©faillant"
    elif data[1] == 0x69:
        infomessage = "Aileron mobile dÃ©faillant, vitesse limitÃ©e, consultez la notice"
    elif data[1] == 0x6A:
        infomessage = "SystÃ¨me de freinage ABS dÃ©faillant"
    elif data[1] == 0x6B:
        infomessage = "SystÃ¨me ESP/ASR dÃ©faillant"
    elif data[1] == 0x6C:
        infomessage = "Suspension dÃ©faillante"
    elif data[1] == 0x6D:
        infomessage = "STOP: direction assistÃ©e dÃ©faillante"
    elif data[1] == 0x6E:
        infomessage = "DÃ©faut boite de vitesse, faites rÃ©parer le vÃ©hicule"
    elif data[1] == 0x6F:
        infomessage = "SystÃ¨me de controle de vitesse dÃ©faillant"
    elif data[1] == 0x73:
        infomessage = "Capteur de luminositÃ© ambiante dÃ©faillant"
    elif data[1] == 0x74:
        infomessage = "Ampoule feu de position dÃ©faillante"
    elif data[1] == 0x75:
        infomessage = "RÃ©glage automatique des projecteurs dÃ©faillant"
    elif data[1] == 0x76:
        infomessage = "Projecteurs directionnels dÃ©faillants"
    elif data[1] == 0x78:
        infomessage = "Airbag(s) ou ceinture(s) Ã  prÃ©tensionneur(s) dÃ©faillant(s)"
    elif data[1] == 0x7A:
        infomessage = "DÃ©faut boite de vitesse, faites rÃ©parer le vÃ©hicule"
    elif data[1] == 0x7B:
        infomessage = "Pied sur frein et levier en position \"N\" nÃ©cessaires"
    elif data[1] == 0x7D:
        infomessage = "PrÃ©sence d'eau dans le filtre Ã  gasoil, faites rÃ©parer le vÃ©hicule"
    elif data[1] == 0x7E:
        infomessage = "DÃ©faut moteur, faites rÃ©parer le vÃ©hicule"
    elif data[1] == 0x7F:
        infomessage = "DÃ©faut moteur, faites rÃ©parer le vÃ©hicule"
    elif data[1] == 0x81:
        infomessage = "Niveau additif FAP trop faible, faites rÃ©parer le vÃ©hicule"
    elif data[1] == 0x83:
        infomessage = "Antivol Ã©lectronique dÃ©faillant"
    elif data[1] == 0x88:
        infomessage = "SystÃ¨me aide au stationnement dÃ©faillant"
    elif data[1] == 0x89:
        infomessage = "SystÃ¨me de mesure de place dÃ©faillant"
    elif data[1] == 0x8A:
        infomessage = "Charge batterie ou alimentation Ã©lectrique dÃ©faillante"
    elif data[1] == 0x8D:
        infomessage = "Pression pneumatiques insuffisante"
    elif data[1] == 0x97:
        infomessage = "SystÃ¨me d'alerte de franchissement de ligne dÃ©faillant"
    elif data[1] == 0x9A:
        infomessage = "Ampoule feu de croisement dÃ©faillante"
    elif data[1] == 0x9B:
        infomessage = "Ampoule feu de route dÃ©faillante"
    elif data[1] == 0x9C:
        infomessage = "Ampoule feu stop dÃ©faillante"
    elif data[1] == 0x9D:
        infomessage = "Ampoule anti-brouillard dÃ©faillante"
    elif data[1] == 0x9E:
        infomessage = "Clignotant dÃ©faillant"
    elif data[1] == 0x9F:
        infomessage = "Ampoule feu de recul dÃ©faillante"
    elif data[1] == 0xA0:
        infomessage = "Ampoule feu de position dÃ©faillante"
    elif data[1] == 0xCD:
        infomessage = "RÃ©gulation de vitesse impossible: vitesse trop faible"
    elif data[1] == 0xCE:
        infomessage = "Activation du rÃ©gulateur impossible: saisir la vitesse"
    elif data[1] == 0xD2:
        infomessage = "Ceintures AV non bouclÃ©es"
    elif data[1] == 0xD3:
        infomessage = "Ceintures passagers AR bouclÃ©es"
    elif data[1] == 0xD7:
        infomessage = "Placer boite automatique en position P"
    elif data[1] == 0xD8:
        infomessage = "Risque de verglas"
    elif data[1] == 0xD9:
        infomessage = "Oubli frein Ã  main !"
    elif data[1] == 0xDE or data[1] == 0x0B:
    # Car doors frame
        doorByte1 = data[3]
        doorByte2 = data[4]
    
        if doorByte1 & 0b00000100 == 0b00000100:
            # decodedCarDoors.insert(.Hood)
            infomessage ="Capot ouvert"
        if doorByte1 & 0b00001000 == 0b00001000:
            # decodedCarDoors.insert(.Trunk)
            infomessage ="Coffre ouvert"
        if doorByte1 & 0b00010000 == 0b00010000:
            # decodedCarDoors.insert(.RearLeft)
            infomessage ="porte arriÃ¨re gauche ouverte"
        if doorByte1 & 0b00100000 == 0b00100000:
            # decodedCarDoors.insert(.RearRight)
            infomessage ="porte arriÃ¨re droite ouverte"
        if doorByte1 & 0b01000000 == 0b01000000:
            # decodedCarDoors.insert(.FrontLeft)
            infomessage ="porte conducteur ouverte"
        if doorByte1 & 0b10000000 == 0b10000000:
            # decodedCarDoors.insert(.FrontRight)
            infomessage ="porte passager ouverte"
        if doorByte2 & 0b01000000 == 0b01000000:
            # decodedCarDoors.insert(.FuelFlap)
            infomessage ="trappe essence ouverte"

    elif data[1] == 0xDF:
        infomessage = "Niveau liquide lave-glace insuffisant"
    elif data[1] == 0xE0:
        infomessage = "Niveau carburant faible"
    elif data[1] == 0xE1:
        infomessage = "Circuit de carburant neutralisÃ©"
    elif data[1] == 0xE3:
        infomessage = "Pile tÃ©lÃ©commande plip usagÃ©e"
    elif data[1] == 0xE5:
        infomessage = "Pression pneumatique(s) non surveillÃ©e"
    elif data[1] == 0xE7:
        infomessage = "Vitesse Ã©levÃ©e, vÃ©rifier si pression pneumatiques adaptÃ©e"
    elif data[1] == 0xE8:
        infomessage = "Pression pneumatique(s) insuffisante"
    elif data[1] == 0xEB:
        infomessage = "La phase de dÃ©marrage a Ã©chouÃ© (consulter la notice)"
    elif data[1] == 0xEC:
        infomessage = "DÃ©marrage prolongÃ© en cours"
    elif data[1] == 0xEF:
        infomessage = "TÃ©lÃ©commande non dÃ©tectÃ©e"
    elif data[1] == 0xF0:
        infomessage = "Diagnostic en cours"
    elif data[1] == 0xF1:
        infomessage = "Diagnostic terminÃ©"
    elif data[1] == 0xF7:
        infomessage = "Ceinture passager AR gauche dÃ©bouclÃ©e"
    elif data[1] == 0xF8:
        infomessage = "Ceinture passager AR central dÃ©bouclÃ©e"
    elif data[1] == 0xF9:
        infomessage = "Ceinture passager AR droit dÃ©bouclÃ©e"
    else:
        infomessage = "Aucun message"
        
    return infomessage.encode('latin1').decode()
