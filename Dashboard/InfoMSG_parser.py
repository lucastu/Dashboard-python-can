def parseInfoMessage(data):
    infomessage = "none"
    infomessagedict = {
        0x00: "Diagnostic OK",
        0x01: "STOP: dÃ©faut tempÃ©rature moteur, arrÃªtez le vÃ©hicule",
        0x03: "Ajustez niveau liquide de refroidissement",
        0x04: "Ajustez le niveau d'huile moteur",
        0x05: "STOP: dÃ©faut pression huile moteur, arrÃªtez le vÃ©hicule",
        0x08: "STOP: systÃ¨me de freinage dÃ©faillant",
        0x0A: "Demande non permise (cf photo)",
        0x0D: "Plusieurs roues crevÃ©es",
        0x0F: "Risque de colmatage filtre Ã particules: consultez la notice",
        0x11: "Suspension dÃ©faillante, vitesse max 90km/h",
        0x12: "Suspension dÃ©faillante",
        0x13: "Direction assistÃ©e dÃ©faillante",
        0x14: "WTF?",
        0x2F: "Essuie-vitre automatique activÃ©",
        0x30: "Essuie-vitre automatique dÃ©sactivÃ©",
        0x31: "Allumage automatique des projecteurs activÃ©",
        0x32: "Allumage automatique des projecteurs dÃ©sactivÃ©",
        0x33: "Auto-verrouillage des portes activÃ©",
        0x34: "Auto-verrouillage des portes dÃ©activÃ©",
        0x37: "SÃ©curitÃ© enfant activÃ©e",
        0x38: "SÃ©curitÃ© enfant dÃ©sactivÃ©e",
        0x3D: "Stationnement NON (cf photo)",
        0x61: "Frein de parking serrÃ©",
        0x62: "Frein de parking desserrÃ©",
        0x64: "Commande frein de parking dÃ©faillante, frein de parking auto activÃ©",
        0x67: "Plaquettes de frein usÃ© es",
        0x68: "Frein de parking dÃ©faillant",
        0x69: "Aileron mobile dÃ©faillant, vitesse limitÃ©e, consultez la notice",
        0x6A: "SystÃ¨me de freinage ABS dÃ©faillant",
        0x6B: "SystÃ¨me ESP/ASR dÃ©faillant",
        0x6C: "Suspension dÃ©faillante",
        0x6D: "STOP: direction assistÃ©e dÃ©faillante",
        0x6E: "DÃ©faut boite de vitesse, faites rÃ©parer le vÃ©hicule",
        0x6F: "SystÃ¨me de controle de vitesse dÃ©faillant",
        0x73: "Capteur de luminositÃ© ambiante dÃ©faillant",
        0x74: "Ampoule feu de position dÃ©faillante",
        0x75: "RÃ©glage automatique des projecteurs dÃ©faillant",
        0x76: "Projecteurs directionnels dÃ©faillants",
        0x78: "Airbag(s) ou ceinture(s) Ã prÃ©tensionneur(s) dÃ©faillant(s)",
        0x7A: "DÃ©faut boite de vitesse, faites rÃ©parer le vÃ©hicule",
        0x7B: "Pied sur frein et levier en position \"N\" nÃ©cessaires",
        0x7D: "PrÃ©sence d'eau dans le filtre Ã gasoil, faites rÃ©parer le vÃ©hicule",
        0x7E: "DÃ©faut moteur, faites rÃ©parer le vÃ©hicule",
        0x7F: "DÃ©faut moteur, faites rÃ©parer le vÃ©hicule",
        0x81: "Niveau additif FAP trop faible, faites rÃ©parer le vÃ©hicule",
        0x83: "Antivol Ã©lectronique dÃ©faillant",
        0x88: "SystÃ¨me aide au stationnement dÃ©faillant",
        0x89: "SystÃ¨me de mesure de place dÃ©faillant",
        0x8A: "Charge batterie ou alimentation Ã©lectrique dÃ©faillante",
        0x8D: "Pression pneumatiques insuffisante",
        0x98: "SystÃ¨me STOP START dÃ©faillant",
        0x97: "SystÃ¨me d'alerte de franchissement de ligne dÃ©faillant",
        0x9A: "Ampoule feu de croisement dÃ©faillante",
        0x9B: "Ampoule feu de route dÃ©faillante",
        0x9C: "Ampoule feu stop dÃ©faillante",
        0x9D: "Ampoule anti-brouillard dÃ©faillante",
        0x9E: "Clignotant dÃ©faillant",
        0x9F: "Ampoule feu de recul dÃ©faillante",
        0xA0: "Ampoule feu de position dÃ©faillante",
        0xCD: "RÃ©gulation de vitesse impossible: vitesse trop faible",
        0xCE: "Activation du rÃ©gulateur impossible: saisir la vitesse",
        0xD2: "Ceintures AV non bouclÃ©es",
        0xD3: "Ceintures passagers AR bouclÃ©es",
        0xD7: "Placer boite automatique en position P",
        0xD8: "Risque de verglas",
        0xD9: "Oubli frein Ã main !",
        0xDF: "Niveau liquide lave-glace insuffisant",
        0xE0: "Niveau carburant faible",
        0xE1: "Circuit de carburant neutralisÃ©",
        0xE3: "Pile tÃ©lÃ©commande plip usagÃ©e",
        0xE5: "Pression pneumatique(s) non surveillÃ©e",
        0xE7: "Vitesse Ã©levÃ©e, vÃ©rifier si pression pneumatiques adaptÃ©e",
        0xE8: "Pression pneumatique(s) insuffisante",
        0xEB: "La phase de dÃ©marrage a Ã©chouÃ© (consulter la notice)",
        0xEC: "DÃ©marrage prolongÃ© en cours",
        0xEF: "TÃ©lÃ©commande non dÃ©tectÃ©e",
        0xF0: "Diagnostic en cours",
        0xF1: "Diagnostic terminÃ©",
        0xF6: "Manoeuvre toit impossible: tÂº ext. trop faible",
        0xF7: "Ceinture passager AR gauche dÃ©bouclÃ©e",
        0xF8: "Ceinture passager AR milieu dÃ©bouclÃ©e",
        0xF9: "Ceinture passager AR droit dÃ©bouclÃ©e",
    }

    try:
        infomessage = infomessagedict[data[1]]
    except:
        if data[1] in [0x0B, 0xDE]:
        # Car doors frame
            doorByte1 = data[3]
            doorByte2 = data[4]

            if doorByte1 & 0b00000100 == 0b00000100:
                infomessage ="Capot ouvert"
            if doorByte1 & 0b00001000 == 0b00001000:
                infomessage ="Coffre ouvert"
            if doorByte1 & 0b00010000 == 0b00010000:
                infomessage ="porte arriÃ¨re gauche ouverte"
            if doorByte1 & 0b00100000 == 0b00100000:
                infomessage ="porte arriÃ¨re droite ouverte"
            if doorByte1 & 0b01000000 == 0b01000000:
                infomessage ="porte conducteur ouverte"
            if doorByte1 & 0b10000000 == 0b10000000:
                infomessage ="porte passager ouverte"
            if doorByte2 & 0b01000000 == 0b01000000:
                infomessage ="trappe essence ouverte"

    return infomessage.encode('latin1').decode()

if __name__ == '__main__':
    #go through every message
    for i in range(255) :   
        infomessage=parseInfoMessage(data=[0x00,i,0x00,0x10,0x00])
        if infomessage != "none":
          print(hex(i), infomessage)   
