#!/usr/bin/env python3
import os
import sys
import shutil
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                             QListWidget, QListWidgetItem, QLabel, QPushButton, 
                             QMessageBox, QInputDialog, QMenu)
from PyQt6.QtCore import Qt

class JarFileManager(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Linux Jar File Manager")
        self.resize(520, 780)
        
        self.cale_sus = os.path.expanduser('~')
        self.cale_jos = '/'
        
        # Opțiune configurabilă prin rotiță
        self.arata_fișiere_ascunse = False
        
        self.init_ui()
        self.aplica_stil_borcan()

    def init_ui(self):
        layout_principal = QVBoxLayout()
        layout_principal.setContentsMargins(25, 20, 25, 25)
        layout_principal.setSpacing(15)
        
        # --- CAPACUL BORCANULUI ---
        self.capac_widget = QWidget()
        self.capac_widget.setObjectName("CapacBorcan")
        layout_capac = QHBoxLayout(self.capac_widget)
        layout_capac.setContentsMargins(15, 10, 15, 10)
        
        titlu_capac = QLabel("🫙 JAR OPERATOR")
        titlu_capac.setStyleSheet("font-weight: bold; color: #11111b; font-size: 14px; background: transparent;")
        layout_capac.addWidget(titlu_capac)
        layout_capac.addStretch()
        
        self.btn_move = QPushButton("📦 Move")
        self.btn_move.clicked.connect(self.actiune_mutare)
        
        self.btn_new = QPushButton("📁 New")
        self.btn_new.clicked.connect(self.actiune_folder_nou)
        
        self.btn_del = QPushButton("🗑️ Del")
        self.btn_del.clicked.connect(self.actiune_stergere)
        
        # ROTIȚA DE SETĂRI
        self.btn_settings = QPushButton("⚙️")
        self.btn_settings.setObjectName("BtnSettings")
        self.btn_settings.setToolTip("Setări Borcan")
        self.btn_settings.clicked.connect(self.deschide_meniu_setari)
        
        layout_capac.addWidget(self.btn_move)
        layout_capac.addWidget(self.btn_new)
        layout_capac.addWidget(self.btn_del)
        layout_capac.addWidget(self.btn_settings)
        
        layout_principal.addWidget(self.capac_widget)
        
        # --- STRATUL DE SUS (Home) ---
        self.eticheta_sus = QLabel("🫧 STRATUL SUPERIOR (Home User)")
        self.eticheta_sus.setObjectName("EtichetaStrat")
        layout_principal.addWidget(self.eticheta_sus)
        
        self.lista_sus = QListWidget()
        self.lista_sus.setObjectName("ListaSus")
        self.lista_sus.itemDoubleClicked.connect(self.navigheaza_sus)
        layout_principal.addWidget(self.lista_sus)
        
        # --- STRATUL DE JOS (Sistem /) ---
        self.eticheta_jos = QLabel("🪨 STRATUL INFERIOR (Sistem de Operare /)")
        self.eticheta_jos.setObjectName("EtichetaStrat")
        layout_principal.addWidget(self.eticheta_jos)
        
        self.lista_jos = QListWidget()
        self.lista_jos.setObjectName("ListaJos")
        self.lista_jos.itemDoubleClicked.connect(self.navigheaza_jos)
        layout_principal.addWidget(self.lista_jos)
        
        self.actualizeaza_tot()
        self.setLayout(layout_principal)

    def aplica_stil_borcan(self):
        stil = """
            QWidget {
                background-color: #1e1e2e;
                font-family: 'Segoe UI', sans-serif;
                color: #cdd6f4;
            }
            QWidget#CapacBorcan {
                background-color: #fab387;
                border-radius: 15px;
            }
            QWidget#CapacBorcan QPushButton {
                background-color: #11111b;
                color: #fab387;
                border: 1px solid #11111b;
                border-radius: 8px;
                padding: 6px 12px;
                font-weight: bold;
                font-size: 12px;
            }
            QWidget#CapacBorcan QPushButton:hover {
                background-color: #313244;
                color: #f5c2e7;
            }
            QWidget#CapacBorcan QPushButton#BtnSettings {
                background-color: #313244;
                color: #cdd6f4;
                font-size: 14px;
                padding: 5px 8px;
            }
            QWidget#CapacBorcan QPushButton#BtnSettings:hover {
                background-color: #11111b;
                color: #fab387;
            }
            QLabel#EtichetaStrat {
                font-weight: bold;
                font-size: 12px;
                color: #a6adc8;
                padding-left: 5px;
            }
            QListWidget {
                border: 2px solid #45475a;
                border-radius: 20px;
                padding: 10px;
                font-size: 14px;
            }
            QListWidget#ListaSus {
                background-color: rgba(137, 180, 250, 0.15);
                border: 2px solid #89b4fa;
            }
            QListWidget#ListaJos {
                background-color: rgba(166, 227, 161, 0.1);
                border: 2px solid #a6e3a1;
            }
            QListWidget::item {
                padding: 6px;
                border-radius: 8px;
            }
            QListWidget::item:hover {
                background-color: #313244;
            }
            QListWidget::item:selected {
                background-color: #45475a;
                color: #f5c2e7;
            }
        """
        self.setStyleSheet(stil)
    # --- LOGICA MENIULUI (ROTIȚĂ) ---
    def deschide_meniu_setari(self):
        meniu = QMenu(self)
        meniu.setStyleSheet("background-color: #313244; color: #cdd6f4; font-size: 13px;")
        
        text_ascunse = "✔️ Ascunde fișierele cu punct (.)" if self.arata_fișiere_ascunse else "👁️ Arată fișierele ascunse (.)"
        actiune_ascunse = meniu.addAction(text_ascunse)
        actiune_despre = meniu.addAction("ℹ️ Despre Linux Jar")
        
        actiune_selectata = meniu.exec(self.btn_settings.mapToGlobal(self.btn_settings.rect().bottomLeft()))
        
        if actiune_selectata == actiune_ascunse:
            self.arata_fișiere_ascunse = not self.arata_fișiere_ascunse
            self.actualizeaza_tot()
        elif actiune_selectata == actiune_despre:
            QMessageBox.information(self, "Despre", "Linux Jar Manager v1.0\nO metaforă unică sub formă de borcan pentru sistemul de fișiere.")

    def actualizeaza_tot(self):
        self.actualizeaza_strat(self.lista_sus, self.cale_sus, e_radacina=(self.cale_sus == '/'))
        self.actualizeaza_strat(self.lista_jos, self.cale_jos, e_radacina=(self.cale_jos == '/'))

    def actualizeaza_strat(self, lista_widget, calea, e_radacina=False):
        lista_widget.clear()
        if not e_radacina:
            lista_widget.addItem(QListWidgetItem("📁 .. (Mergi Înapoi)"))
            
        try:
            for element in os.listdir(calea):
                if element.startswith('.') and not self.arata_fișiere_ascunse and element != '..':
                    continue
                cale_completa = os.path.join(calea, element)
                if os.path.isdir(cale_completa):
                    lista_widget.addItem(QListWidgetItem(f"📁 {element}"))
                else:
                    lista_widget.addItem(QListWidgetItem(f"📄 {element}"))
        except PermissionError:
            lista_widget.addItem(QListWidgetItem("❌ Acces interzis (Sistem protejat)"))

    # --- LOGICA OPERAȚIUNILOR ---
    def obtine_element_selectat(self):
        if self.lista_sus.hasFocus() and self.lista_sus.currentItem():
            return self.lista_sus, self.cale_sus, self.lista_sus.currentItem().text()[2:]
        if self.lista_jos.hasFocus() and self.lista_jos.currentItem():
            return self.lista_jos, self.cale_jos, self.lista_jos.currentItem().text()[2:]
        return None, None, None

    def actiune_stergere(self):
        lista, calea, element = self.obtine_element_selectat()
        if not element or ".. (Mergi Înapoi)" in element: return
        cale_completa = os.path.join(calea, element)
        
        raspuns = QMessageBox.question(self, "Ștergere", f"Sigur vrei să ștergi '{element}'?",
                                       QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if raspuns == QMessageBox.StandardButton.Yes:
            try:
                if os.path.isdir(cale_completa): shutil.rmtree(cale_completa)
                else: os.remove(cale_completa)
                self.actualizeaza_tot()
            except Exception as e: QMessageBox.critical(self, "Eroare", f"Eșuat: {e}")

    def actiune_folder_nou(self):
        lista = self.lista_jos if self.lista_jos.hasFocus() else self.lista_sus
        calea = self.cale_jos if self.lista_jos.hasFocus() else self.cale_sus
        
        nume, ok = QInputDialog.getText(self, "Folder Nou", "Numele folderului:")
        if ok and nume:
            try:
                os.makedirs(os.path.join(calea, nume), existence_ok=True)
                self.actualizeaza_tot()
            except Exception as e: QMessageBox.critical(self, "Eroare", f"Eșuat: {e}")

    def actiune_mutare(self):
        lista_sursa, calea_sursa, element = self.obtine_element_selectat()
        if not element or ".. (Mergi Înapoi)" in element: return
        
        calea_dest = self.cale_jos if lista_sursa == self.lista_sus else self.cale_sus
        try:
            shutil.move(os.path.join(calea_sursa, element), os.path.join(calea_dest, element))
            self.actualizeaza_tot()
        except Exception as e: QMessageBox.critical(self, "Eroare", f"Mutare eșuată: {e}")

    # --- NAVIGARE ---
    def navigheaza_sus(self, item):
        text = item.text()
        self.cale_sus = os.path.dirname(self.cale_sus) if ".. (Mergi Înapoi)" in text else os.path.join(self.cale_sus, text[2:])
        self.actualizeaza_strat(self.lista_sus, self.cale_sus, e_radacina=(self.cale_sus == '/'))

    def navigheaza_jos(self, item):
        text = item.text()
        self.cale_jos = os.path.dirname(self.cale_jos) if ".. (Mergi Înapoi)" in text else os.path.join(self.cale_jos, text[2:])
        self.actualizeaza_strat(self.lista_jos, self.cale_jos, e_radacina=(self.cale_jos == '/'))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    manager = JarFileManager()
    manager.show()
    sys.exit(app.exec())
