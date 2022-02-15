from random import randint

framenamedict = {
0x00:    ["INIT_STATUS_FRAME",      "fixed",  "01" ,"00"],
0x01:    ["VOLUME_FRAME",           "random", 1, 0 , 30],
0x02:    ["TEMPERATURE_FRAME",      "random", 1, 0 , 50],
0x03:    ["RADIO_SOURCE_FRAME",     "random", 1, 0 , 3],
0x04:    ["RADIO_NAME_FRAME",       "fixed",  "20.43.55.4C.54.55.52.45", "20.43.55.4C.54.55.52.45"],
0x05:    ["RADIO_FREQ_FRAME",       "random",  2 ,0 , 3],
0x06:    ["RADIO_FMTYPE_FRAME",     "random", 1, 0 , 3],
0x07:    ["RADIO_DESC_FRAME",       "random",  2 ,0 , 3],
0x08:    ["INFO_MSG_FRAME",         "fixed",  "7F.FF.00.FF.FF.FF.FF.FF","20.43.55.4C.54.55.52.45"],
0x09:    ["RADIO_STATIONS_FRAME",   "fixed",  "7F.FF.00.FF.FF.FF.FF.FF","20.43.55.4C.54.55.52.45"],
0x0C:    ["INFO_TRIP_FRAME",        "random", 1 ,0 , 3 ],
0x0E:    ["INFO_INSTANT_FRAME",     "fixed",  "7F.FF","20.43"],
0x10:    ["AUDIO_SETTINGS_FRAME",   "fixed",  "7F.FF","20.43"],
0x11:    ["REMOTE_COMMAND_FRAME",   "fixed",  "7F.FF","20.43"],
0x12:    ["OPEN_DOOR_FRAME",        "fixed",  "7F.FF","20.43"],
0x13:    ["TIME_FRAME",             "random", 2 ,0 , 3],
0x14:    ["SHUTDOWN_FRAME",         "fixed",  "00"]
}

def write_to_file(data_to_write):
    print("Writing file...")    
    print(data_to_write)
    # f = open("/home/pi/lucas/fakedata.txt", "a")
    # f.write(data_to_write)
    # f.close()
    print("Writing OK !")

def run():
    print("Choose frame to send :")
    choice_number =0
    for choice_number in framenamedict :
        print(f"{choice_number}) {framenamedict[choice_number][0]}")
        choice_number+=1
    
    id_choice = None
    data_choice = None
    while id_choice not in framenamedict:
        try :
            id_choice=int(input("Enter frame to send :"))
        except ValueError:
            print ('Entry not valid')
    print(f"Choice : {id_choice} ({hex(id_choice)}) {framenamedict[id_choice][0]}")        
    if framenamedict[id_choice][1] == "fixed":
        number_of_data=len(framenamedict[id_choice])-2
        check = False
        while check is False :
            print("Data sample :")
            for x in range(number_of_data):
                print(f'{x}) {framenamedict[id_choice][x+2]}')
            while data_choice not in range(number_of_data):
                try:
                    data_choice=int(input("Choose data sample to send :"))
                except ValueError:
                    print ('Entry not valid')    
            if data_choice in range(number_of_data):
                check = True
    
        data_to_write = f'{"{:02x}".format(id_choice)} {framenamedict[id_choice][data_choice+2]}'
    
    elif framenamedict[id_choice][1] == "random":
        data_to_write=0
        print(f'Generating a {framenamedict[id_choice][2]} byte data between {framenamedict[id_choice][3]} and {framenamedict[id_choice][4]} in hexadecimal')
        generated_data=randint(framenamedict[id_choice][3],framenamedict[id_choice][4])
    
        if framenamedict[id_choice][2] == 1:
            data=str('{:02x}'.format(generated_data))
        elif  framenamedict[id_choice][2] == 2:   
            data=str('{:04x}'.format(generated_data))
        elif framenamedict[id_choice][2] == 3:
            data=str('{:06x}'.format(generated_data))
        elif  framenamedict[id_choice][2] == 4:
            data=str('{:08x}'.format(generated_data))        
        formated_data = '.'.join(data[i:i + 2] for i in range(0, len(data), 2)).upper()
        data_to_write = f'{"{:02x}".format(id_choice)} {formated_data}'
    
    write_to_file(data_to_write)
    input("press enter to continue")
    
if __name__ == '__main__':
    while True :
        run()
