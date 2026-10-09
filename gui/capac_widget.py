from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLabel

class CapacBorcan(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("CapacBorcan")
        self.parent_win = parent
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 10, 15, 10)
        
        self.btn_titlu = QPushButton("🫙 JAR OPERATOR")
        self.btn_titlu.setObjectName("TitluCapac")
        self.btn_titlu.clicked.connect(self.afiseaza_despre)
        layout.addWidget(self.btn_titlu)
        
        layout.addStretch()
        
        self.btn_move = QPushButton("📦 Mută")
        self.btn_new = QPushButton("📁 Nou")
        self.btn_rename = QPushButton("✏️ Redenumește") # BUTONUL NOU PE CAPAC!
        self.btn_del = QPushButton("🗑️ Șterge")
        self.btn_places = QPushButton("📍 Locații")
        self.btn_places.clicked.connect(self.deschide_meniu_locatii)
        
        self.btn_lang = QPushButton("🌐 RO")
        self.btn_lang.clicked.connect(self.deschide_meniu_limbi)
        
        self.btn_settings = QPushButton("⚙️")
        self.btn_settings.setObjectName("BtnSettings")
        
        layout.addWidget(self.btn_move)
        layout.addWidget(self.btn_new)
        layout.addWidget(self.btn_rename) # Îl așezăm în linie
        layout.addWidget(self.btn_del)
        layout.addWidget(self.btn_places)
        layout.addWidget(self.btn_lang)
        layout.addWidget(self.btn_settings)

    def deschide_meniu_locatii(self):
        from PyQt6.QtWidgets import QMenu
        meniu = QMenu(self)
        meniu.setStyleSheet("background-color: #313244; color: #cdd6f4; font-size: 13px;")
        limba = self.parent_win.limba_curenta if self.parent_win else "ro"
        
        txt_locatii = {
            "ro": ["🏠 Director Personal (Home)", "💾 SSD / Volume Stocare", "🔌 Unități Montate (/mnt)", "💻 Rădăcină Sistem (/)", "🌐 Locații Rețea (Samba/NAS)"],
            "en": ["🏠 Home Directory", "💾 SSD / Storage Volumes", "🔌 Mounted Drives (/mnt)", "💻 System Root (/)", "🌐 Network Locations (Samba/NAS)"],
            "it": ["🏠 Directory Personale (Home)", "💾 SSD / Volumi Memoria", "🔌 Unità Montate (/mnt)", "💻 Radice Sistema (/)", "🌐 Posizioni di Rete (Samba/NAS)"]
        }
        
        act_home = meniu.addAction(txt_locatii[limba][0])
        act_media = meniu.addAction(txt_locatii[limba][1])
        act_mnt = meniu.addAction(txt_locatii[limba][2])
        act_root = meniu.addAction(txt_locatii[limba][3])
        act_net = meniu.addAction(txt_locatii[limba][4])
        
        actiune = meniu.exec(self.btn_places.mapToGlobal(self.btn_places.rect().bottomLeft()))
        if actiune == act_home: self.parent_win.schimba_calea_strat_activ("home")
        elif actiune == act_media: self.parent_win.schimba_calea_strat_activ("media")
        elif actiune == act_mnt: self.parent_win.schimba_calea_strat_activ("mnt")
        elif actiune == act_root: self.parent_win.schimba_calea_strat_activ("root")
        elif actiune == act_net: self.parent_win.schimba_calea_strat_activ("network")

    def deschide_meniu_limbi(self):
        from PyQt6.QtWidgets import QMenu
        meniu = QMenu(self)
        meniu.setStyleSheet("background-color: #313244; color: #cdd6f4; font-size: 13px;")
        act_ro = meniu.addAction("🇷🇴 Română")
        act_en = meniu.addAction("🇺🇸 English")
        act_it = meniu.addAction("🇮🇹 Italiano")
        
        actiune = meniu.exec(self.btn_lang.mapToGlobal(self.btn_lang.rect().bottomLeft()))
        if actiune == act_ro:
            self.parent_win.schimba_limba("ro")
            self.btn_lang.setText("🌐 RO")
        elif actiune == act_en:
            self.parent_win.schimba_limba("en")
            self.btn_lang.setText("🌐 EN")
        elif actiune == act_it:
            self.parent_win.schimba_limba("it")
            self.btn_lang.setText("🌐 IT")

    def afiseaza_despre(self):
        self.parent_win.afiseaza_despre_tradus()
