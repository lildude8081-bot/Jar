import os
import json
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLabel, QMenu
from PyQt6.QtCore import Qt

class CapacBorcan(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("CapacBorcan")
        self.parent_win = parent
        self.init_ui()

    def init_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 10, 15, 10)

        # Titlul curat din versiunea 1.9.0
        self.btn_titlu = QPushButton("🫙 JAR OPERATOR v1.9.0")
        self.btn_titlu.setObjectName("TitluCapac")
        self.btn_titlu.clicked.connect(self.afiseaza_despre)
        layout.addWidget(self.btn_titlu)

        layout.addStretch()

        # Butoanele tale originale de acțiune
        self.btn_move = QPushButton("📦 Mută")
        self.btn_new = QPushButton("📁 Nou")
        self.btn_rename = QPushButton("✏️ Redenumește")
        self.btn_del = QPushButton("🗑️ Șterge")
        
        # Meniul de Locații
        self.btn_places = QPushButton("📍 Locații")
        self.btn_places.clicked.connect(self.deschide_meniu_locatii)

        # ⭐ BUTONUL: Favorite - cu suport de traducere dinamică
        self.btn_fav = QPushButton("⭐ Favorite")
        self.btn_fav.clicked.connect(self.deschide_meniu_favorite)

        self.btn_lang = QPushButton("🌐 RO")
        self.btn_lang.clicked.connect(self.deschide_meniu_limbi)

        self.btn_settings = QPushButton("⚙️")
        self.btn_settings.setObjectName("BtnSettings")

        # Așezăm butoanele în ordinea ta perfectă
        layout.addWidget(self.btn_move)
        layout.addWidget(self.btn_new)
        layout.addWidget(self.btn_rename)
        layout.addWidget(self.btn_del)
        layout.addWidget(self.btn_places)
        layout.addWidget(self.btn_fav)
        layout.addWidget(self.btn_lang)
        layout.addWidget(self.btn_settings)

    def obtine_calea_fisier_favorite(self):
        os.makedirs("assets", exist_ok=True)
        return "assets/bookmarks.json"

    def incarca_favorite(self):
        cale_json = self.obtine_calea_fisier_favorite()
        if not os.path.exists(cale_json):
            implicit = [os.path.expanduser("~/Lucruri Python")]
            with open(cale_json, "w", encoding="utf-8") as f:
                json.dump(implicit, f, indent=4, ensure_ascii=False)
            return implicit
        try:
            with open(cale_json, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []

    def salveaza_favorite(self, lista_favorite):
        cale_json = self.obtine_calea_fisier_favorite()
        try:
            with open(cale_json, "w", encoding="utf-8") as f:
                json.dump(lista_favorite, f, indent=4, ensure_ascii=False)
        except Exception:
            pass

    def deschide_meniu_favorite(self):
        meniu = QMenu(self)
        meniu.setStyleSheet("background-color: #313244; color: #cdd6f4; font-size: 13px;")
        
        limba = self.parent_win.limba_curenta if self.parent_win else "ro"
        favorite = self.incarca_favorite()
        
        # Detectăm folderul deschis în stratul activ
        cale_curenta = None
        if self.parent_win and hasattr(self.parent_win, 'ultimul_strat_activ') and self.parent_win.ultimul_strat_activ:
            cale_curenta = self.parent_win.ultimul_strat_activ.cale_curenta

        # Traduceri pentru opțiunile de bază
        txt_adauga = {"ro": "➕ Adaugă locația curentă", "en": "➕ Add current location", "it": "➕ Aggiungi posizione corrente"}
        txt_elimina = {"ro": "☆ Elimină locația curentă", "en": "☆ Remove current location", "it": "Rimuovi posizione corrente"}

        # Dacă folderul curent este deja în JSON, arătăm steluța goală (☆) ca să-l scoată instant!
        if cale_curenta in favorite:
            act_toggle = meniu.addAction(txt_elimina[limba])
            mod_actiune = "elimina"
        else:
            act_toggle = meniu.addAction(txt_adauga[limba])
            mod_actiune = "adauga"
            
        meniu.addSeparator()

        # Afișăm restul directoarelor salvate în listă
        actiuni_favorite = {}
        for fav in favorite:
            nume_afisat = f"⭐ {os.path.basename(fav) if os.path.basename(fav) else fav}"
            act = meniu.addAction(nume_afisat)
            act.setToolTip(fav)
            actiuni_favorite[act] = fav

        # Deschidem meniul dropdown direct sub buton
        actiune = meniu.exec(self.btn_fav.mapToGlobal(self.btn_fav.rect().bottomLeft()))
        
        # Executăm acțiunea instantaneu, fără ferestre secundare!
        if actiune == act_toggle:
            if cale_curenta:
                if mod_actiune == "adauga" and cale_curenta not in favorite:
                    favorite.append(cale_curenta)
                elif mod_actiune == "elimina" and cale_curenta in favorite:
                    favorite.remove(cale_curenta)
                self.salveaza_favorite(favorite)
        elif actiune in actiuni_favorite:
            cale_destinatie = actiuni_favorite[actiune]
            if self.parent_win and hasattr(self.parent_win, 'ultimul_strat_activ') and self.parent_win.ultimul_strat_activ:
                strat = self.parent_win.ultimul_strat_activ
                if os.path.exists(cale_destinatie) and os.path.isdir(cale_destinatie):
                    strat.istoric_inapoi.append(strat.cale_curenta)
                    strat.istoric_inainte.clear()
                    strat.cale_curenta = cale_destinatie
                    strat.actualizeaza_lista()
                    strat.cale_schimbata.emit()

    def deschide_meniu_locatii(self):
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
        meniu = QMenu(self)
        meniu.setStyleSheet("background-color: #313244; color: #cdd6f4; font-size: 13px;")
        act_ro = meniu.addAction("🇷🇴 Română")
        act_en = meniu.addAction("🇺🇸 English")
        act_it = meniu.addAction("🇮🇹 Italiano")
        
        actiune = meniu.exec(self.btn_lang.mapToGlobal(self.btn_lang.rect().bottomLeft()))
        
        # Adăugăm traducerea dinamică și pentru noul buton de favorite în funcție de limba aleasă!
        txt_buton_fav = {"ro": "⭐ Favorite", "en": "⭐ Bookmarks", "it": "⭐ Preferiti"}
        
        if actiune == act_ro:
            self.parent_win.schimba_limba("ro")
            self.btn_lang.setText("🌐 RO")
            self.btn_fav.setText(txt_buton_fav["ro"])
        elif actiune == act_en:
            self.parent_win.schimba_limba("en")
            self.btn_lang.setText("🌐 EN")
            self.btn_fav.setText(txt_buton_fav["en"])
        elif actiune == act_it:
            self.parent_win.schimba_limba("it")
            self.btn_lang.setText("🌐 IT")
            self.btn_fav.setText(txt_buton_fav["it"])

    def afiseaza_despre(self):
        self.parent_win.afiseaza_despre_tradus()
