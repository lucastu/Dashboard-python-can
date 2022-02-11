class Ui(QtWidgets.QMainWindow):
  ''' Define the main window of the app '''
   def update_progress_bluetooth_track(self):
       try:
           self.Bluetooth_progressBar.setValue(int(float(self.percent.text())))
       except:
           logging.info("Wrong type of value for track position")

   def update_progress_volume(self):
       try:
           self.Volumewindow.progress.setValue(int(self.Volume.text()))
       except:
           logging.info("Wrong type of value for Volume")

   def __init__(self):
        super(Ui, self).__init__()  # Call the inherited classes __init__ method
        uic.loadUi('/home/pi/lucas/interface.ui', self)  # Load the .ui Mainwindow file
        self.setWindowFlags(Qt.Widget | Qt.FramelessWindowHint)

        #Initialisation of the alert window
        self.init_alert_window()
        #Initialisation of the volume window
        self.Volumewindow=volumewindow()

        # Init both tabs
        self.tabWidget.setCurrentIndex(0)
        self.tabWidget.setCurrentIndex(1)

        self.showMaximized()  # Show the GUI

        # Init of the custom signals that connects to the progress bars
        self.custom_signals = Communicate()
        self.custom_signals.update_progress_bluetooth_track_signal.connect(self.update_progress_bluetooth_track)
        self.custom_signals.update_progress_volume_signal.connect(self.update_progress_volume)

        # Init radio list
        self.radioList0.setText('')
        self.radioList1.setText('')
        self.radioList2.setText('')
        self.radioList3.setText('')
        self.radioList4.setText('')
        self.radioList5.setText('')

   def init_alert_window(self):
        self.Ombre = ombre()
        self.AlertMSG = alertmsg()

   def show_alert(self):
         self.Ombre.showMaximized()
         self.AlertMSG.show()

   def hide_alert(self):
         self.Ombre.hide()
         self.AlertMSG.hide()

   def resetaudiosettingselector(self) :
         #Each selelctor display go hidden
         #Ugly but the best way to avoid repainting every selector and crashing program
         if self.SliderBassesselector.isVisible():
            self.SliderBassesselector.setHidden(True)
         if self.SliderBassesselector_2.isVisible():
            self.SliderBassesselector_2.setHidden(True)
         if self.SliderAigusselector.isVisible():
            self.SliderAigusselector.setHidden(True)
         if self.SliderAigusselector_2.isVisible():
            self.SliderAigusselector_2.setHidden(True)
         if self.frontRearBalanceselector.isVisible():
            self.frontRearBalanceselector.setHidden(True)
         if self.frontRearBalanceselector_2.isVisible():
            self.frontRearBalanceselector_2.setHidden(True)
         if self.leftRightBalanceselector.isVisible():
            self.leftRightBalanceselector.setHidden(True)
         if self.leftRightBalanceselector_2.isVisible():
            self.leftRightBalanceselector_2.setHidden(True)
         if self.Loudnessselector.isVisible():
            self.Loudnessselector.setHidden(True)
         if self.Loudnessselector_2.isVisible():
            self.Loudnessselector_2.setHidden(True)
         if self.automaticVolumeselector.isVisible():
            self.automaticVolumeselector.setHidden(True)
         if self.automaticVolumeselector_2.isVisible():
            self.automaticVolumeselector_2.setHidden(True)
         if self.equalizerselector.isVisible():
            self.equalizerselector.setHidden(True)
         if self.equalizerselector_2.isVisible():
            self.equalizerselector_2.setHidden(True)

   def resetequalizerselector(self) :
         #Each equalizer selector display go grey
         self.equalizernone.setStyleSheet("color: grey;")
         self.equalizerclassical.setStyleSheet("color: grey;")
         self.equalizerjazzBlues.setStyleSheet("color: grey;")
         self.equalizerpopRock.setStyleSheet("color: grey;")
         self.equalizertechno.setStyleSheet("color: grey;")
         self.equalizervocal.setStyleSheet("color: grey;")

#    def update_bluetooth_track(self):
#          try:
#              B = bluetooth_utils()
#              track_info = B.run()
#              self.Bluetooth_track.setText(track_info[0])
#              self.Bluetooth_artist.setText(track_info[1])
#              # self.Bluetooth_album.setText(track_info[2])
#              self.Bluetooth_timing.setText(track_info[3])
#              self.Bluetooth_duration.setText(track_info[4])
#              self.percent.setText(str(track_info[5]))
#              self.custom_signals.update_progress_bluetooth_track_signal.emit()
#          except:
#              pass

   def close_all(self):
        # set flag off
        if reading_thread.is_alive():
            stop_reading.set()
            reading_thread.join()
        if source_handleris_alive():
            source_handler.close()
        logging.info("Fermeture de l'application")
        #After closing threads, closing the window
        self.close()
