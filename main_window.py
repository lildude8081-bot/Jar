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
        
        self.schimba_limba(self.limba_curenta)
        self.actiune_refresh_liste()

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
        self.strat_sus.actualizeaza_lista()
        self.strat_jos.actualizeaza_lista()

    def afiseaza_despre_tradus(self):
        QMessageBox.information(self, self.traduceri[self.limba_curenta]["titlu_despre"], self.traduceri[self.limba_curenta]["gluma"])

    def incarca_stil_css(self):
        S = 'styles.css' if self.tema_intunecata else 'styles_light.css'
        cale = os.path.join(os.path.dirname(__file__), 'assets', S)
        if os.path.exists(cale):
            with open(cale, 'r') as f: self.setStyleSheet(f.read())

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
