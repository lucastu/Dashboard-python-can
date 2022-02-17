from random import randint
import time
framenamedict = {
0x00:    ["INIT_STATUS_FRAME",      "fixed",  "01" ,"00"],
0x01:    ["VOLUME_FRAME",           "random", 1, 0 , 30],
0x02:    ["TEMPERATURE_FRAME",      "random", 1, 0 , 50],
0x03:    ["RADIO_SOURCE_FRAME",     "random", 1, 0 , 3],
0x04:    ["RADIO_NAME_FRAME",       "fixed",  "20.43.55.4C.54.55.52.45", "22.04.35.54.C5.45.55.24"],
0x05:    ["RADIO_FREQ_FRAME",       "random",  2 ,880 , 1060],
0x06:    ["RADIO_FMTYPE_FRAME",     "random", 1, 0 , 3],
0x07:    ["RADIO_DESC_FRAME",       "random",  2 ,0 , 3],
0x08:    ["INFO_MSG_FRAME",         "fixed",  "7F.FF.00.FF.FF.FF.FF.FF","00.DE.C8.40.00.00.00.00"],
0x09:    ["RADIO_STATIONS_FRAME",   "fixed",  "7F.FF.00.FF.FF.FF.FF.FF","20.43.55.4C.54.55.52.45"],
0x0C:    ["INFO_TRIP_FRAME",        "fixed",  "34.0A.83.00.41.0C.33" ],
0x0E:    ["INFO_INSTANT_FRAME",     "fixed",  "00.FF.FF.01.04.FF.FF"],
0x10:    ["AUDIO_SETTINGS_FRAME",   "fixed",  "3F.3F.3F.3F.3F.07.03","3F.3D.40.3F.41.07.03"],
0x11:    ["REMOTE_COMMAND_FRAME",   "fixed",  "00","08","80","40","04","0C"],
0x12:    ["OPEN_DOOR_FRAME",        "fixed",  "00","08","80","40","04"],
0x13:    ["TIME_FRAME",             "random", 5 ,0 , 2400],
0x14:    ["SHUTDOWN_FRAME",         "fixed",  "00"]
}

testing = False
path_of_file = '/home/pi/lucas/other/fakedata.txt'

def write_to_file(data_to_write):
    print("Writing file...")    
    print(data_to_write)
    if not testing :
        f = open(path_of_file, "a")
        f.write(data_to_write)
        f.close()
    print("Writing OK !")

def send_full_data():
    for item in framenamedict :
        if framenamedict[item][1] == "fixed":
            data_to_write = f'{"{:02x}".format(item).upper()} {framenamedict[item][2]}'            
            write_to_file(data_to_write)
            
        elif framenamedict[item][1] == "random":    
            data_to_write=0
            print(f'Generating a {framenamedict[item][2]} byte data between {framenamedict[item][3]} and {framenamedict[item][4]} in hexadecimal')
            generated_data=randint(framenamedict[item][3],framenamedict[item][4])
            data_to_write = format_data(framenamedict[item][2],generated_data, item) 
            write_to_file(data_to_write)
        wait_for_empty_file()   

def send_loop_data() :        
    choice=[0x01,0x02,0x04,0x05,0x13]
    id_choice=None
    while id_choice not in choice :
        for i in choice:
            print(hex(i),') ',framenamedict[i][0])

        id_choice=int(input("Choose data to loop :"),16)

    for i in range (framenamedict[id_choice][3],framenamedict[id_choice][4] ):
        print(f'Generating a {framenamedict[item][2]} byte data between {framenamedict[item][3]} and {framenamedict[item][4]} in hexadecimal')
        generated_data=randint(framenamedict[item][3],framenamedict[item][4])
        data_to_write = format_data(framenamedict[item][2],generated_data, item) 
        write_to_file(data_to_write)
        wait_for_empty_file()

def wait_for_empty_file():
    print("Wainting for emptyness of the file")
    if not testing :
        while os.path.getsize(path_of_file) == 0  :
              continue
    else :
        time.sleep(1)
    print("file empty")    
    
def format_data(number_of_bytes, generated_data,id):  
	if number_of_bytes == 1:
            data=str('{:02x}'.format(generated_data))
        elif  number_of_bytes == 2:   
            data=str('{:04x}'.format(generated_data))
        elif number_of_bytes == 3:
            data=str('{:06x}'.format(generated_data))
        elif number_of_bytes == 4:
            data=str('{:08x}'.format(generated_data))
        elif number_of_bytes == 5:
            data=str('{:10x}'.format(generated_data))
        formated_data = '.'.join(data[i:i + 2] for i in range(0, len(data), 2)).upper()
        data_to_write = f'{"{:02x}".format(id)} {formated_data}'
	return data_to_write

def choose_data():
    can_continue =True
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
        data_to_write = format_data(framenamedict[id_choice][2],generated_data, id_choice)
   
    write_to_file(data_to_write)

    if input("press enter to continue, q to stop : ") =='q':
        can_continue =False
        print("stoping...")
    return can_continue    
    
if __name__ == '__main__':
    print('1) send_full_data') 
    print('2) choose_data_to_send') 
    print('3) send_loop_data')    
    choice = input("Enter option :")
    if choice == "1" :
        send_full_data()
    elif choice == "2" :
        active = True
        while active :
            active = choose_data()
    elif choice == "3" :
        send_loop_data()
