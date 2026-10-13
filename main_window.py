#!/usr/bin/env python3
import os
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QMessageBox, QInputDialog, QMenu
from PyQt6.QtCore import Qt, QSettings
from PyQt6.QtGui import QIcon, QKeySequence, QShortcut

from gui.capac_widget import CapacBorcan
from gui.strat_widget import StratBorcan
from core.translations import TRADUCERI
import core.file_manager_logic as logic
import core.places_handler as places

class JarFileManager(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Linux Jar File Manager")
        self.resize(550, 850)
        
        self.setari_sistem = QSettings("MihaiAura", "JarFileManager")
        self.limba_curenta = self.setari_sistem.value("limba", "ro")
        self.ultimul_strat_activ = None
        self.traduceri = TRADUCERI
        
        # Injectăm manual cheile necesare pentru meniul README
        for L in ["ro", "en", "it"]:
            self.traduceri[L]["btn_readme"] = "📖 README" if L=="en" else ("📖 ManualUtente" if L=="it" else "📖 Ghid Utilizare")
            self.traduceri[L]["readme_text"] = "Ghidul se afla in folderul readme/README.md"
        
        self.calculeaza_dimensiuni = False
        self.tema_intunecata = True
        self.init_ui()
        self.incarca_stil_css()
        
        cale_iconita = os.path.join(os.path.dirname(__file__), 'assets', 'icons', 'borcan.png')
        if os.path.exists(cale_iconita): self.setWindowIcon(QIcon(cale_iconita))
        self.configureaza_scurtaturi_tastatura()

    def init_ui(self):
        self.layout_principal = QVBoxLayout(self)
        self.layout_principal.setContentsMargins(25, 20, 25, 25)
        self.layout_principal.setSpacing(10)

        self.capac = CapacBorcan(self)
        self.capac.btn_move.clicked.connect(self.actiune_mutare)
        self.capac.btn_new.clicked.connect(self.actiune_folder_nou)
        self.capac.btn_rename.clicked.connect(self.actiune_redenumire)
        self.capac.btn_del.clicked.connect(self.actiune_stergere)
        self.capac.btn_settings.clicked.connect(self.deschide_meniu_setari)
        self.layout_principal.addWidget(self.capac)

        self.lbl_sus = QLabel()
        self.layout_principal.addWidget(self.lbl_sus)
        self.strat_sus = StratBorcan(os.path.expanduser('~'), "ListaSus", self)
        self.strat_sus.lista.itemSelectionChanged.connect(lambda: self.set_strat_activ(self.strat_sus))
        self.layout_principal.addWidget(self.strat_sus)

        self.lbl_jos = QLabel()
        self.layout_principal.addWidget(self.lbl_jos)
        self.strat_jos = StratBorcan("/", "ListaJos", self)
        self.strat_jos.lista.itemSelectionChanged.connect(lambda: self.set_strat_activ(self.strat_jos))
        self.layout_principal.addWidget(self.strat_jos)

        # --- COMPONENTĂ NOUĂ: WIDGET-UL DE CAMUFLAJ (v1.9.0) ---
        from PyQt6.QtWidgets import QListWidget
        self.lista_camuflaj = QListWidget(self)
        self.lista_camuflaj.setStyleSheet("""
            QListWidget {
                background-color: #11111b;
                color: #fab387;
                font-size: 14px;
                font-weight: bold;
                border: 2px dashed #fab387;
                border-radius: 8px;
                padding: 10px;
            }
        """)
        self.lista_camuflaj.itemClicked.connect(self.actiune_afiseaza_reteta_detaliata)
        # Umplem lista cu rețete fictive de murături ca să pară o aplicație inofensivă
        retete = [
            "📋 REȚETAR OFICIAL - CĂMARA LUI MIHAI (CECINAS)",
            "🫙 1. Rețetă Castraveți murați în oțet cu boabe de muștar",
            "🫙 2. Secretul gogonelelor tari și crocante pentru iarnă",
            "🫙 3. Gogoșari umpluți cu conopidă în saramură fiartă",
            "🫙 4. Varză roșie tocată cu hrean și ardei iute",
            "🫙 5. Conopidă murată cu morcov și foi de dafin",
            "📌 SFAT DE GOSPODAR: Păstrați butoiul la temperatură constantă în pivniță!"
        ]
        self.lista_camuflaj.addItems(retete)
        self.layout_principal.addWidget(self.lista_camuflaj)
        self.lista_camuflaj.hide() # Ascunsă implicit la pornire

        self.camuflaj_activ = False

        self.schimba_limba(self.limba_curenta)
        self.actiune_refresh_liste()

    def keyPressEvent(self, event):
        """ Prinde tasta F2 pentru a activa/dezactiva camuflajul instant (v1.9.0) """
        from PyQt6.QtCore import Qt
        if event.key() == Qt.Key.Key_F2:
            self.actiune_toggle_camuflaj()
        else:
            super().keyPressEvent(event)

    def actiune_toggle_camuflaj(self):
        """ Schimbă starea dintre fișierele reale și modul murături tradus dinamic (v1.9.0) """
        self.camuflaj_activ = not self.camuflaj_activ
        
        # Baza de date locală autonomă pentru titluri
        titluri_camuflaj = {
            "ro": [
                "🫙 1. Castraveți murați în oțet cu boabe de muștar",
                "🫙 2. Secretul gogonelelor tari și crocante pentru iarnă",
                "🫙 3. Gogoșari umpluți cu conopidă în saramură fiartă",
                "🫙 4. Varză roșie tocată cu hrean și ardei iute",
                "🫙 5. Conopidă murată cu morcov și foi de dafin"
            ],
            "en": [
                "🫙 1. Pickled Cucumbers in vinegar with mustard seeds",
                "🫙 2. The secret of crunchy pickled green tomatoes for winter",
                "🫙 3. Bell peppers stuffed with cauliflower in hot brine",
                "🫙 4. Shredded red cabbage with horseradish and chili pepper",
                "🫙 5. Pickled cauliflower with carrots and bay leaves"
            ],
            "it": [
                "🫙 1. Cetrioli sott'aceto con semi di senape",
                "🫙 2. Il segreto dei pomodori verdi sott'aceto croccanti per l'inverno",
                "🫙 3. Peperoni ripieni di cavolfiore in salamoia calda",
                "🫙 4. Cavolo rosso tritato con rafano e peperoncino",
                "🫙 5. Cavolfiore sott'aceto con carote e foglie di alloro"
            ]
        }
        
        limba = self.limba_curenta if hasattr(self, 'limba_curenta') else 'ro'
        
        if self.camuflaj_activ:
            # --- ACTIVĂM MODUL GOSPODĂRIE ---
            self.strat_sus.hide()
            self.strat_jos.hide()
            self.lbl_sus.hide()
            self.lbl_jos.hide()
            
            if hasattr(self.capac, 'btn_move'): self.capac.btn_move.hide()
            if hasattr(self.capac, 'btn_new'): self.capac.btn_new.hide()
            if hasattr(self.capac, 'btn_rename'): self.capac.btn_rename.hide()
            if hasattr(self.capac, 'btn_del'): self.capac.btn_del.hide()
            if hasattr(self.capac, 'btn_places'): self.capac.btn_places.hide()
            if hasattr(self.capac, 'btn_fav'): self.capac.btn_fav.hide()
            
            # Încărcăm elementele direct din dicționarul local în funcție de limbă
            self.lista_camuflaj.clear()
            self.lista_camuflaj.addItems(titluri_camuflaj.get(limba, titluri_camuflaj['ro']))
            
            if hasattr(self.capac, 'btn_titlu'): 
                txt_titlu = {"ro": "📋 REȚETE BORCAN v1.9.0", "en": "📋 JAR RECIPES v1.9.0", "it": "📋 RICETTE BARATTOLO v1.9.0"}
                self.capac.btn_titlu.setText(txt_titlu.get(limba, txt_titlu['ro']))
            
            self.lista_camuflaj.show()
        else:
            # --- DESCAMUFLARE INSTANTANEE ---
            self.lista_camuflaj.hide()
            self.strat_sus.show()
            self.strat_jos.show()
            self.lbl_sus.show()
            self.lbl_jos.show()
            
            if hasattr(self.capac, 'btn_move'): self.capac.btn_move.show()
            if hasattr(self.capac, 'btn_new'): self.capac.btn_new.show()
            if hasattr(self.capac, 'btn_rename'): self.capac.btn_rename.show()
            if hasattr(self.capac, 'btn_del'): self.capac.btn_del.show()
            if hasattr(self.capac, 'btn_places'): self.capac.btn_places.show()
            if hasattr(self.capac, 'btn_fav'): self.capac.btn_fav.show()
            
            if hasattr(self.capac, 'btn_titlu'): 
                self.capac.btn_titlu.setText("🫙 JAR OPERATOR v1.9.0")

    def actiune_afiseaza_reteta_detaliata(self, item):
        """ Afișează conținutul complet al rețetei selectate la click (v1.9.0) """
        text_element = item.text()
        numar_reteta = None
        if '1.' in text_element: numar_reteta = '1'
        elif '2.' in text_element: numar_reteta = '2'
        elif '3.' in text_element: numar_reteta = '3'
        elif '4.' in text_element: numar_reteta = '4'
        elif '5.' in text_element: numar_reteta = '5'
        
        if numar_reteta:
            continut_retete = {
                'ro': {
                    '1': '🥒 CASTRAVEȚI MURAȚI ÎN OȚET\n\nSe spală castraveții și se așază strâns în borcan. Se adaugă căței de usturoi și boabe de muștar. Se fierbe compoziția de apă cu oțet (1 la 3), sare și zahăr, apoi se toarnă fierbinte în borcan. Se închide ermetic!',
                    '2': '🍅 SECRETUL GOGONELELOR TARI\n\nHreanul din belșug este secretul pentru a le păstra tari! Se pun gogonelele alternativ cu feliile de morcov și bucățile de hrean în butoi. Se toarnă saramura caldă (1 lingură sare la 1L apă).',
                    '3': '🫑 GOGOȘARI UMPLUȚI CU CONOPIDĂ\n\nSe curăță gogoșarii de cotor. În interiorul fiecăruia se pune câte o bucată de conopidă crudă. Se așază frumos în borcan și se toarnă compoziția fiartă de oțet dulce-acrișor.',
                    '4': '🥬 VARZĂ ROȘIE CU HREAN\n\nVarza se toacă mărunt, se freacă bine cu sare grunjoasă și se amestecă cu hreanul iute dat pe răzătoare. Se presează extrem de bine în borcan până își lasă zeama proprie.',
                    '5': '🥦 CONOPIDĂ MURATĂ CU MORCOV\n\nBucățile de conopidă se spală și se aranjează estetic alături de rondele de morcov și foi de dafin. Se adaugă saramura simplă fiartă și se pune capacul.'
                },
                'en': {
                    '1': '🥒 PICKLED CUCUMBERS IN VINEGAR\n\nWash the cucumbers and pack tightly into the jar. Add garlic cloves and mustard seeds. Boil water and vinegar mixture (1:3) with salt and sugar, pour hot into the jar. Seal tightly!',
                    '2': '🍅 THE SECRET OF CRUNCHY GREEN TOMATOES\n\nPlenty of horseradish is the secret to keeping them crunchy! Layer tomatoes with carrot slices and horseradish. Pour warm brine (1 tbsp salt per 1L water) and let it ferment.',
                    '3': '🫑 BELL PEPPERS STUFFED WITH CAULIFLOWER\n\nCore the red peppers. Place a raw cauliflower floret inside each pepper. Pack into the jar and pour the boiled sweet and sour vinegar mixture over them.',
                    '4': '🥬 SHREDDED RED CABBAGE WITH HORSERADISH\n\nShred the cabbage finely, rub well with rock salt, and mix with spicy horseradish. Press down extremely hard in the jar until it releases its own juice.',
                    '5': '🥦 PICKLED CAULIFLOWER WITH CARROTS\n\nWash cauliflower florets and arrange with carrot rounds and bay leaves. Add boiled simple brine and close the lid.'
                },
                'it': {
                    '1': '🥒 CETRIOLI SOTT\'ACETO\n\nLavare i cetrioli e metterli stretti nel barattolo. Aggiungere aglio e semi di senape. Far bollire acqua e aceto (3:1) con sale e zucchero, versare caldo e chiudere ermeticamente!',
                    '2': '🍅 IL SEGRETO DEI POMODORI VERDI SOTT\'ACETO\n\nIl rafano in abbondanza è il segreto per mantenerli sodi! Mettere i pomodori alternati a fette di carota e pezzi di rafano. Versare la salamoia tiepida (1 cucchiaio di sale per 1L d\'acqua).',
                    '3': '🫑 PEPERONI RIPIENI DI CAVOLFIORE\n\nSvuotare i peperoni dal torsolo. Mettere una cimetta di cavolfiore crudo dentro ogni peperone. Sistemarli nel barattolo e versare la miscela bollente di aceto agrodolce.',
                    '4': '🥬 CAVOLO ROSSO TRITATO CON RAFANO\n\nTritare il cavolo, strofinarlo con sale grosso e mescolarlo con il rafano piccante. Premerlo molto bene nel barattolo finché non rilascia il proprio succo.',
                    '5': '🥦 CAVOLFIORE SOTT\'ACETO CON CAROTE\n\nLavare le cimette di cavolfiore e sistemarle con le carote e le foglie di alloro. Aggiungere la salamoia semplice bollente e chiudere il tappo.'
                }
            }
            
            limba = self.limba_curenta if hasattr(self, 'limba_curenta') else 'ro'
            continut = continut_retete.get(limba, continut_retete['ro']).get(numar_reteta, '')
            
            from PyQt6.QtWidgets import QMessageBox
            msg = QMessageBox(self)
            msg.setWindowTitle(item.text())
            msg.setText(continut)
            msg.setIcon(QMessageBox.Icon.Information)
            msg.setStyleSheet("background-color: #1e1e2e; color: #cdd6f4; font-size: 14px;")
            msg.exec()

    def set_strat_activ(self, strat):
        self.ultimul_strat_activ = strat

    def schimba_limba(self, cod_limba):
        self.limba_curenta = cod_limba
        self.setari_sistem.setValue("limba", cod_limba)
        self.lbl_sus.setText(self.traduceri[cod_limba]["strat_sus"])
        self.lbl_jos.setText(self.traduceri[cod_limba]["strat_jos"])
        self.capac.btn_places.setText(self.traduceri[cod_limba]["btn_places"])
        
        D = {
            "ro": ["📦 Mută", "📁 Nou", "✏️ Redenumește", "🗑️ Șterge", "🌐 RO"],
            "en": ["📦 Move", "📁 New", "✏️ Rename", "🗑️ Del", "🌐 EN"],
            "it": ["📦 Sposta", "📁 Nuovo", "✏️ Rinomina", "🗑️ Elimina", "🌐 IT"]
        }
        self.capac.btn_move.setText(D[cod_limba][0])
        self.capac.btn_new.setText(D[cod_limba][1])
        self.capac.btn_rename.setText(D[cod_limba][2])
        self.capac.btn_del.setText(D[cod_limba][3])
        self.capac.btn_lang.setText(D[cod_limba][4])
        self.strat_sus.actualizeaza_butoane()
        self.strat_jos.actualizeaza_butoane()

    def configureaza_scurtaturi_tastatura(self):
        QShortcut(QKeySequence("F5"), self).activated.connect(self.actiune_refresh_liste)
        QShortcut(QKeySequence("Ctrl+N"), self).activated.connect(self.actiune_folder_nou)

    def actiune_refresh_liste(self):
        """ Readuce instantaneu straturile la starea de pornire (Sus la User, Jos la Sistem) """
        import os
        
        # 1. Resetăm stratul de sus în folderul User (/home/mihai)
        cale_user = os.path.expanduser('~')
        self.strat_sus.istoric_inapoi.append(self.strat_sus.cale_curenta)
        self.strat_sus.istoric_inainte.clear()
        self.strat_sus.cale_curenta = cale_user
        self.strat_sus.actualizeaza_lista()
        self.strat_sus.cale_schimbata.emit()

        # 2. Resetăm stratul de jos în folderul de Sistem (/)
        self.strat_jos.istoric_inapoi.append(self.strat_jos.cale_curenta)
        self.strat_jos.istoric_inainte.clear()
        self.strat_jos.cale_curenta = "/"
        self.strat_jos.actualizeaza_lista()
        self.strat_jos.cale_schimbata.emit()

    def afiseaza_despre_tradus(self):
        QMessageBox.information(self, self.traduceri[self.limba_curenta]["titlu_despre"], self.traduceri[self.limba_curenta]["gluma"])

    def incarca_stil_css(self):
        import json
        cale_setari = os.path.join(os.path.dirname(__file__), 'assets', 'settings.json')
        
        # Verificăm dacă apelul vine din inițializare (când citim de pe disc)
        # sau din interfață (când utilizatorul tocmai a schimbat bifa)
        if not hasattr(self, '_stil_initializat'):
            self._stil_initializat = True
            if os.path.exists(cale_setari):
                try:
                    with open(cale_setari, 'r', encoding='utf-8') as f:
                        setari = json.load(f)
                        self.tema_intunecata = setari.get('tema_intunecata', True)
                except:
                    self.tema_intunecata = True
        else:
            # Dacă utilizatorul a schimbat tema din meniu, salvăm noua stare pe disc
            try:
                os.makedirs(os.path.dirname(cale_setari), exist_ok=True)
                with open(cale_setari, 'w', encoding='utf-8') as f:
                    json.dump({'tema_intunecata': self.tema_intunecata}, f, indent=4)
            except:
                pass

        # Aplicăm fișierul corespunzător conform valorii finale
        S = 'styles.css' if self.tema_intunecata else 'styles_light.css'
        cale = os.path.join(os.path.dirname(__file__), 'assets', S)
        if os.path.exists(cale):
            with open(cale, 'r', encoding='utf-8') as f: 
                self.setStyleSheet(f.read())

    def schimba_calea_strat_activ(self, tip):
        T = self.ultimul_strat_activ if self.ultimul_strat_activ else self.strat_jos
        N = places.proceseaza_salt_locatie(tip)
        if N and os.path.exists(N):
            T.istoric_inapoi.append(T.cale_curenta)
            T.istoric_inainte.clear()
            T.cale_curenta = N
            self.actiune_refresh_liste()

    def deschide_meniu_setari(self):
        meniu = QMenu(self)
        meniu.setStyleSheet("background-color: #313244; color: #cdd6f4; font-size: 13px;")
        A = self.strat_sus.arata_ascunse

        # RECONSTRUIT ȘI ADĂUGAT OPȚIUNEA 4 (Dezinstalare Purge) COMPLETĂ PENTRU TOATE LIMBILE
        TXT = {
            "ro": [
                "✔️ Ascunde fișierele (.)" if A else "👁️ Arată fișierele (.)", 
                "🔄 Reîmprospătează (F5)", 
                "🌙 Mod Întunecat" if not self.tema_intunecata else "☀️ Mod Luminos", 
                "❌ Ascunde dimensiunile" if self.calculeaza_dimensiuni else "📊 Afișează dimensiunile",
                "🗑️ Dezinstalează complet aplicația (Purge)"
            ],
            "en": [
                "✔️ Hide hidden files (.)" if A else "👁️ Show hidden files (.)", 
                "🔄 Refresh (F5)", 
                "🌙 Dark Mode" if not self.tema_intunecata else "☀️ Light Mode", 
                "❌ Hide sizes" if self.calculeaza_dimensiuni else "📊 Show sizes",
                "🗑️ Completely uninstall this app (Purge)"
            ],
            "it": [
                "✔️ Nascondi file nascosti (.)" if A else "👁️ Mostra file nascosti (.)", 
                "🔄 Aggiorna (F5)", 
                "🌙 Modalità Scura" if not self.tema_intunecata else "☀️ Modalità Chiara", 
                "❌ Nascondi dimensioni" if self.calculeaza_dimensiuni else "📊 Mostra dimensioni",
                "🗑️ Disinstalla completamente l'app (Purge)"
            ]
        }

        act_ascunse = meniu.addAction(TXT[self.limba_curenta][0])
        act_dim = meniu.addAction(TXT[self.limba_curenta][3])
        act_readme = meniu.addAction(self.traduceri[self.limba_curenta]["btn_readme"])
        act_tema = meniu.addAction(TXT[self.limba_curenta][2])
        
        # Injectăm butonul de autodistrugere în meniul grafic dropdown
        act_uninstall = meniu.addAction(TXT[self.limba_curenta][4])
        
        act_ref = meniu.addAction(TXT[self.limba_curenta][1])

        sel = meniu.exec(self.capac.btn_settings.mapToGlobal(self.capac.btn_settings.rect().bottomLeft()))

        if sel == act_ascunse:
            self.strat_sus.arata_ascunse = not A
            self.strat_jos.arata_ascunse = not A
            self.actiune_refresh_liste()
        elif sel == act_dim:
            self.calculeaza_dimensiuni = not self.calculeaza_dimensiuni
            self.actiune_refresh_liste()
        elif sel == act_readme:
            cale_rm = os.path.join(os.path.dirname(__file__), 'readme', 'README.md')
            txt = ""
            if os.path.exists(cale_rm):
                try:
                    with open(cale_rm, 'r', encoding='utf-8') as f: cont = f.read()
                    ts, te = f"<!-- LANG_{self.limba_curenta.upper()} -->", "<!-- LANG_END -->"
                    if ts in cont: txt = cont.split(ts)[1].split(te)[0].strip()
                except Exception: pass
            if not txt: txt = self.traduceri[self.limba_curenta]["readme_text"]
            QMessageBox.information(self, self.traduceri[self.limba_curenta]["btn_readme"], txt)
            
        elif sel == act_uninstall:
            # Sistemul secret de dezinstalare automată independentă
            titluri = {"ro": "Autodistrugere", "en": "Uninstall", "it": "Disinstallazione"}
            intrebari = {
                "ro": "Sigur vrei să ștergi complet 'Borcanul' și toate alias-urile din sistem?",
                "en": "Are you sure you want to completely remove 'Jar Manager' and its aliases?",
                "it": "Sei sicuro di voler rimuovere completamente 'Jar Manager' e i suoi alias?"
            }
            
            raspuns = QMessageBox.question(self, titluri[self.limba_curenta], intrebari[self.limba_curenta], 
                                            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if raspuns == QMessageBox.StandardButton.Yes:
                import subprocess
                # Chemăm pkexec grafic de la Linux Mint pentru a rula APT Purge cu drepturi ridicate
                try:
                    subprocess.Popen(["pkexec", "apt", "purge", "-y", "linux-jar-file-manager"])
                    QApplication.quit()
                except Exception as e:
                    QMessageBox.critical(self, "Eroare / Error", f"Action failed: {e}")
                    
        elif sel == act_tema:
            self.tema_intunecata = not self.tema_intunecata
            self.incarca_stil_css()
        elif sel == act_ref:
            self.actiune_refresh_liste()

    def obtine_strat_activ(self):
        if self.strat_sus.lista.hasFocus() and self.strat_sus.lista.currentItem(): return self.strat_sus, self.strat_jos
        if self.strat_jos.lista.hasFocus() and self.strat_jos.lista.currentItem(): return self.strat_jos, self.strat_sus
        if self.ultimul_strat_activ: return self.ultimul_strat_activ, (self.strat_jos if self.ultimul_strat_activ == self.strat_sus else self.strat_sus)
        return self.strat_jos, self.strat_sus

    def actiune_stergere(self):
        sa, _ = self.obtine_strat_activ()
        if not sa or not sa.lista.currentItem(): return
        el = sa.lista.currentItem().text()[2:].split("   (")[0].strip()
        if ".. (Mergi Înapoi)" in el: return
        if QMessageBox.question(self, "Ștergere", f"Sigur ștergi '{el}'?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No) == QMessageBox.StandardButton.Yes:
            try: logic.sterge_element(sa.cale_curenta, el); sa.actualizeaza_lista()
            except Exception as e: QMessageBox.critical(self, "Eroare", str(e))

    def actiune_folder_nou(self):
        sa, _ = self.obtine_strat_activ()
        st = sa if sa else self.strat_sus
        nume, ok = QInputDialog.getText(self, "Folder Nou", "Nume:")
        if ok and nume:
            try: os.makedirs(os.path.join(st.cale_curenta, nume), exist_ok=True); st.actualizeaza_lista()
            except Exception as e: QMessageBox.critical(self, "Eroare", str(e))

    def actiune_redenumire(self):
        sa, _ = self.obtine_strat_activ()
        if not sa or not sa.lista.currentItem(): return
        el = sa.lista.currentItem().text()[2:].split("   (")[0].strip()
        if ".. (Mergi Înapoi)" in el: return
        nume, ok = QInputDialog.getText(self, "Rename", "Nume nou:", text=el)
        if ok and nume and nume != el:
            try: logic.redenumeste_element(sa.cale_curenta, el, nume); sa.actualizeaza_lista()
            except Exception as e: QMessageBox.critical(self, "Eroare", str(e))

    def actiune_mutare(self):
        strat_sursa, strat_dest = self.obtine_strat_activ()
        if not strat_sursa or not strat_sursa.lista.currentItem(): return
        text_brut = strat_sursa.lista.currentItem().text()[2:]
        element = text_brut.split("   (")[0].strip() if "   (" in text_brut else text_brut
        if ".. (Mergi Înapoi)" in element: return
        try:
            logic.muta_element(strat_sursa.cale_curenta, strat_dest.cale_curenta, element)
            strat_sursa.actualizeaza_lista()
            strat_dest.actualizeaza_lista()
        except Exception as e: QMessageBox.critical(self, "Eroare", str(e))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    manager = JarFileManager()
    manager.show()
    sys.exit(app.exec())
