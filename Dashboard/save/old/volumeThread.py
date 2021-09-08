def volumethread() :
  positionup = False
  while not stop_thread :
    #Si le flag interne du threald est levé, on enregistre son heure et on descend le flag
    if self.isset() :
      lastchangetime = int(time.time())
      self.clear()

    #Si ça fait moins de 2 secondes qu'il ya eu un changement
    if int(time.time()) - lastchangetime < 2 :
      self.progress.setValue(Volume)
      if positionup == False :
        #Volume.show()
        moveup()
        positionup = True
    #si ça fait plus de 2 secondes mais que la position de la fenêtre est Up, on la descend
    elif positionup == True :
      movedown()
      positionup = False
    #En dehors de ces cas, on attend la levée du flag
    else : 
      self.wait()
