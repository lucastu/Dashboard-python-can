class Alert(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.label = QLabel("Another Window")
        layout.addWidget(self.label)
        self.setLayout(layout)
        
        
#Fonction qui appelle la création de la window d'alert        
def show_new_window(self):
    if self.w is None:
        self.w = Alert()
        self.w.show()

    else:
        self.w = None  # Discard reference, close window.    
