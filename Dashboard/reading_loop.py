def reading_loop(source_handler, root):
    """Background thread for reading data from Arduino."""
    #FRAMETYPES and their IDs
    INIT_STATUS_FRAME =    0x00
    VOLUME_FRAME =         0x01
    TEMPERATURE_FRAME =    0x02
    RADIO_SOURCE_FRAME =   0x03
    RADIO_NAME_FRAME =     0x04
    RADIO_FREQ_FRAME =     0x05
    RADIO_FMTYPE_FRAME =   0x06
    RADIO_DESC_FRAME =     0x07
    INFO_MSG_FRAME =       0x08
    RADIO_STATIONS_FRAME = 0x09
    INFO_TRIP_FRAME =     0x0C
    # INFO_TRIP2_FRAME =     0x0D
    INFO_INSTANT_FRAME =   0x0E
    # TRIP_MODE_FRAME =      0x0F
    AUDIO_SETTINGS_FRAME = 0x10
    REMOTE_COMMAND_FRAME = 0x11  
    OPEN_DOOR_FRAME      = 0x12
    # RADIO_FACE_BUTTON =    0x13
    SHUTDOWN_FRAME    =    0x14

    # Init for the bluetooth command
    B = bluetooth_utils()

    while not stop_reading.is_set():
        time.sleep(.05)
        try:
            frame_id, data = source_handler.get_message()
        except InvalidFrame:
            continue
        except EOFError:
            break

        if frame_id == VOLUME_FRAME:
            temp = str(data[0] & 0b00011111)
            root.Volume.setText(temp)
            root.custom_signals.update_progress_volume_signal.emit()

            if (not (data[0] & 0b11100000 == 0b11100000)) and (not root.Volumewindow.visible):
                root.Volumewindow.moveup()

            elif ((data[0] & 0b11100000 == 0b11100000) and root.Volumewindow.visible):
                root.Volumewindow.movedown()
            
        elif frame_id == INIT_STATUS_FRAME:
            logging.info("Init communication with arduino OK")
            
        elif frame_id == SHUTDOWN_FRAME:
            logging.info("Shut down data : " + data[0])
            #os.system("sudo shutdown -h now")
            
        elif frame_id == REMOTE_COMMAND_FRAME:
            #logging.info("REMOTE_COMMAND_FRAME data : " + str(data[0]))
            if (data[0] & 0b00001100) == 0b00001100 :
                #Both button pressed : Pause/play      
                B.control('playpause')
            elif (data[0] & 0b10000000) == 0b10000000:
                #Next button pressed
                B.control('next')
            elif (data[0] & 0b01000000) == 0b01000000 :
                #Previous button pressed
                B.control('prev')
               
        elif frame_id == OPEN_DOOR_FRAME:
            if (data[0] & 0b10000000) == 0b10000000 :
                #Door Front Left     
                logging.info("Door Front Left")
            if (data[0] & 0b01000000) == 0b01000000 :
                #Door Front Right
                logging.info("Door Front Right")
            if (data[0] & 0b00100000) == 0b00100000 :
                #Door Back Left
                logging.info("Door Back Left")
            if (data[0] & 0b00010000) == 0b00010000 :
                #Door Back Right
                logging.info("Door Back Right")
            if (data[0] & 0b00001000) == 0b00001000 :
                #Door Trunk    
                logging.info("Door Trunk ")
      
        elif frame_id == TEMPERATURE_FRAME:
            temp = str(data[0])
            text= temp + "°C"
            root.Temperature.setText(text)
            root.Temperatureb.setText(text)

        elif frame_id == RADIO_NAME_FRAME:
            root.RadioName.setText(format_data_ascii(data))

        elif frame_id == RADIO_FREQ_FRAME:
            temp = format_data_hex(data)
            root.RadioFreq.setText(str(float(int(temp,16))/10)+ "MHz")                                            

        elif frame_id == RADIO_FMTYPE_FRAME:
            temp = data[0]
            radioFMType ="No Type"
            if temp == 1:
                RadioFMType ="FM1"
            elif temp == 2:
                RadioFMType ="FM2"
            elif temp == 4:
                RadioFMType ="FMAST"
            elif temp == 5 :
                RadioFMType ="AM"
            root.RadioType.setText("Radio "+ RadioFMType)

        elif frame_id == RADIO_SOURCE_FRAME:
            temp = data[0]
            Source = "Aucune source..."
            if temp == 1:
                Source = "Tuner"
                root.tabWidget.setCurrentIndex(0)
            elif temp == 2:
                Source = "cd"
            elif temp == 3:
                Source = "OpenAuto"
                root.tabWidget.setCurrentIndex(1)
            elif temp == 4:
                Source = "AUX1"
            elif temp == 5:
                Source = "AUX2"
            elif temp == 6:
                Source = "USB"
            elif temp == 7:
                Source = "BLUETOOTH"
            audiosettings['source']=Source
                  
        elif frame_id == RADIO_DESC_FRAME:
            temp = format_data_ascii(data)      

            #This one never worked....
            logging.info("Radio desc frame data : %s  " % temp)
                  
        elif frame_id == INFO_MSG_FRAME:
            infomessage = parseInfoMessage(data, root)
            root.AlertMSG.texte.setText(infomessage)
            
            if not (data[0] & 0b01110000) :
               root.show_alert()
            else :
               root.hide_alert()
                  
        elif frame_id == RADIO_STATIONS_FRAME:
            temp = format_data_ascii(data)
            logging.info("station liste : " + temp)
            if '|' in temp:
                radio_list = temp.split("|")
                root.radioList0.setText("1 : "+ radio_list[0])
                root.radioList1.setText("2 : "+ radio_list[1])
                root.radioList2.setText("3 : "+ radio_list[2])
                root.radioList3.setText("4 : "+ radio_list[3])
                root.radioList4.setText("5 : "+ radio_list[4])
                root.radioList5.setText("6 : "+ radio_list[5])

        elif frame_id == INFO_TRIP_FRAME :
            distanceafterresetbyte= bytes([data[1],data[2]])
            distanceafterreset =int((''.join('%02X' % byte for byte in distanceafterresetbyte)),16)
            text="%skm" % distanceafterreset
            root.tripinfo1.setText(text)
            root.tripinfo1b.setText(text)

            averageFuelUsagebyte= bytes([data[3],data[4]])
            averageFuelUsage =int((''.join('%02X' % byte for byte in averageFuelUsagebyte)),16)/10
            text="Conso moyenne : %sL/100km" % averageFuelUsage
            root.tripinfo3.setText(text)
            root.tripinfo3b.setText(text)

            
        elif frame_id == INFO_INSTANT_FRAME :
            fuelleftbyte= bytes([data[3],data[4]])
            fuelleftbyte2=''.join('%02X' % byte for byte in fuelleftbyte)
            text="%skm" % (int(fuelleftbyte2,16))
            root.tripinfo2.setText(text)
            root.tripinfo2b.setText(text)

            if (data[1] & 0b10000000) == 0b10000000 :
              text="conso instantanée : -- "
              root.tripinfo4.setText(text)
              root.tripinfo4b.setText(text)
            else :
              consoinstantbyte= bytes([data[1],data[2]])
              consoinstantbyte2=''.join('%02X' % byte for byte in consoinstantbyte)
              text="conso instantanée : %s " + str(float(int(consoinstantbyte2,16))/10)
              root.tripinfo4.setText(text)
              root.tripinfo4b.setText(text)

            if (data[0] & 0b00001000) == 0b00001000 :
                # if Tripbutton pressed : switch window
                cmd = 'xdotool keydown  alt +Tab keyup alt+Tab'
                os.system(cmd)

        elif frame_id == AUDIO_SETTINGS_FRAME:
            #Active selected mode in audio settings
            if (data[0] & 0b10000000) == 0b10000000 :
                activeMode = 1  # .leftRightBalance
                root.resetaudiosettingselector()
                root.leftRightBalanceselector.setHidden(False)
                root.leftRightBalanceselector_2.setHidden(False)
            elif (data[1] & 0b10000000) == 0b10000000 :
                activeMode = 2  # .frontRearBalance
                root.resetaudiosettingselector()
                root.frontRearBalanceselector.setHidden(False)
                root.frontRearBalanceselector_2.setHidden(False)
            elif (data[2] & 0b10000000) == 0b10000000 :
                activeMode = 3  # .bass
                root.resetaudiosettingselector()
                root.SliderBassesselector.setHidden(False)
                root.SliderBassesselector_2.setHidden(False)
            elif (data[4] & 0b10000000) == 0b10000000 :
                activeMode = 4  # .treble
                root.resetaudiosettingselector()
                root.SliderAigusselector.setHidden(False)
                root.SliderAigusselector_2.setHidden(False)
            elif (data[5] & 0b10000000) == 0b10000000 :
                activeMode = 5  # .loudness
                root.resetaudiosettingselector()
                root.Loudnessselector.setHidden(False)
                root.Loudnessselector_2.setHidden(False)
            elif (data[5] & 0b00010000) == 0b00010000 :
                activeMode = 6  # .automaticVolume
                root.resetaudiosettingselector()
                root.automaticVolumeselector.setHidden(False)
                root.automaticVolumeselector_2.setHidden(False)
            elif (data[6] & 0b01000000) == 0b01000000 :
                activeMode = 7  # .equalizer
                root.resetaudiosettingselector()
                root.equalizerselector.setHidden(False)
                root.equalizerselector_2.setHidden(False)
            else :
                activeMode = 0
                root.resetaudiosettingselector()
            # f there is an activeMode of audio settings, switch to the audiosettings tab

            if activeMode != 0 :
                root.tabWidget.setCurrentIndex(2)
            else :
                if audiosettings['source'] == "OpenAuto":
                    root.tabWidget.setCurrentIndex(1)
                else :
                    root.tabWidget.setCurrentIndex(0)

            #Valeur de l'equalizer Setting
            if (data[6] & 0b10111111) ==  0b00000011 :
                # .none
                root.resetequalizerselector()
                root.equalizernone.setStyleSheet("color: white;")
            elif (data[6] & 0b10111111) ==  0b00000111 :
                # .classical
                root.resetequalizerselector()
                root.equalizerclassical.setStyleSheet("color: white;")
            elif (data[6] & 0b10111111) == 0b00001011 :
                # .jazzBlues
                root.resetequalizerselector()
                root.equalizerjazzBlues.setStyleSheet("color: white;")
            elif (data[6] & 0b10111111) == 0b00001111 :
                # .popRock
                root.resetequalizerselector()
                root.equalizerpopRock.setStyleSheet("color: white;")
            elif (data[6] & 0b10111111) == 0b00010011 :
                # .vocals
                root.resetequalizerselector()
                root.equalizervocal.setStyleSheet("color: white;")
            elif (data[6] & 0b10111111) == 0b00010111 :
                # .techno
                root.resetequalizerselector()
                root.equalizertechno.setStyleSheet("color: white;")  
                  
            #Enregistrement de toutes ces variables dans le dictionnaire audiosettings
            audiosettings['activeMode']         = activeMode
            audiosettings['frontRearBalance']   = int(data[1] & 0b01111111) - 63
            audiosettings['leftRightBalance']   = int(data[0] & 0b01111111) - 63
            audiosettings['automaticVolume']    = (data[5] & 0b00000111) == 0b00000111
            audiosettings['bass']               = int(data[2] & 0b01111111) - 63
            audiosettings['treble']             = int(data[4] & 0b01111111) - 63
            audiosettings['loudness']           = ((data[5] & 0b01000000) == 0b01000000)
             
            #Update de l'affichage dans l'onglet Settings
            root.SliderBasses.setValue(audiosettings['bass'])
            root.SliderAigus.setValue(audiosettings['treble'])
            root.frontRearBalance.setValue(audiosettings['frontRearBalance'])
            root.leftRightBalance.setValue(audiosettings['leftRightBalance'])                      
            root.Loudness.setChecked(audiosettings['loudness'])
            root.automaticVolume.setChecked(audiosettings['automaticVolume'])
            # root.equalizer.setText(str(audiosettings['equalizer']))

        else:
            logging.info ("FRAME ID NON TRAITE : %s  :  %s  %s" % (frame_id, format_data_hex(data), format_data_ascii(data)))


