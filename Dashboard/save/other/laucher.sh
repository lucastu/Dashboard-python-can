#!/bin/bash
  # le premier grep est celui du nom du processus (.py normalement)
  if (ps aux | grep Dashboard_main.py | grep -v grep > /dev/null)
  then
  #si le nom du script est trouvé dans les processus qui tournent:
  #on demande à la fenêtre "______"de se mettre en avant sur le display 0
DISPLAY=:0.0 XAUTHORITY=/home/pi/.Xauthority xdotool search --desktop 0 --name "MainWindow" windowactivate

  else
  #Sinon on lance le script /home/pi/... .py    & (et en même temps)
  #tant que la fenêtre n'est pas ouverte on attend
DISPLAY=:0.0 XAUTHORITY=/home/pi/.Xauthority python3 /home/pi/lucas/Dashboard_main.py &
while [[ ! DISPLAY=:0.0 XAUTHORITY=/home/pi/.Xauthority wmctrl -l|grep MainWindow ]] ; do
  true
done
  #Après ça, on demande à la fenêtre "______"de se mettre devant
DISPLAY=:0.0 XAUTHORITY=/home/pi/.Xauthority xdotool search --desktop 0 --name "MainWindow" windowactivate

  fi
