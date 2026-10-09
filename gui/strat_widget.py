import os, subprocess, shutil
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QListWidget, QListWidgetItem, QMessageBox, QMenu, QProgressBar, QLabel
from PyQt6.QtCore import pyqtSignal, Qt
CLIPBOARD_CALE_SURSA, CLIPBOARD_ACTIUNE = None, None
class StratBorcan(QWidget):
    cale_schimbata = pyqtSignal()
    def __init__(self, cale, nume, parent=None):
        super().__init__(parent); self.cale_curenta, self.nume_strat, self.istoric_inapoi, self.istoric_inainte, self.arata_ascunse = cale, nume, [], [], False; self.init_ui()
    def init_ui(self):
        layout = QVBoxLayout(self); layout.setContentsMargins(0, 0, 0, 0); layout.setSpacing(5); bara = QHBoxLayout()
        self.btn_back, self.btn_fwd, self.edit_cale = QPushButton("⬅️"), QPushButton("➡️"), QLineEdit(self.cale_curenta)
        self.btn_back.clicked.connect(self.click_inapoi); self.btn_fwd.clicked.connect(self.click_inainte); self.edit_cale.returnPressed.connect(self.schimba_calea_manual)
        bara.addWidget(self.btn_back); bara.addWidget(self.btn_fwd); bara.addWidget(self.edit_cale); layout.addLayout(bara)
        self.edit_filtru = QLineEdit(); self.edit_filtru.setObjectName("EditFiltru"); self.edit_filtru.textChanged.connect(self.filtreaza_fisierele_instant); layout.addWidget(self.edit_filtru)
        self.lista = QListWidget(); self.lista.itemDoubleClicked.connect(self.navigheaza); self.lista.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu); self.lista.customContextMenuRequested.connect(self.deschide_meniu_contextual); layout.addWidget(self.lista)
        lay_sp = QHBoxLayout(); self.lbl_spatiu = QLabel("Disk: --"); self.lbl_spatiu.setStyleSheet("font-size: 11px; color: #a6adc8; font-weight: bold;")
        self.bara_progres_spatiu = QProgressBar(); self.bara_progres_spatiu.setFixedHeight(10); self.bara_progres_spatiu.setTextVisible(False)
        lay_sp.addWidget(self.lbl_spatiu); lay_sp.addWidget(self.bara_progres_spatiu); layout.addLayout(lay_sp); self.actualizeaza_butoane()
    def actualizeaza_butoane(self):
        self.btn_back.setEnabled(len(self.istoric_inapoi) > 0); self.btn_fwd.setEnabled(len(self.istoric_inainte) > 0); self.edit_cale.setText(self.cale_curenta)
        L = self.window().limba_curenta if self.window() and hasattr(self.window(), 'limba_curenta') else "ro"
        P = {"ro": "🔍 Filtreaza instant...", "en": "🔍 Instant filter...", "it": "🔍 Filtra istantaneamente..."}
        self.edit_filtru.setPlaceholderText(P[L])
    def filtreaza_fisierele_instant(self, txt):
        txt = txt.lower().strip()
        for i in range(self.lista.count()):
            it = self.lista.item(i)
            if ".. (Mergi Inapoi)" in it.text(): it.setHidden(False); continue
            it.setHidden(txt not in it.text().lower())
    def actualizeaza_indicator_spatiu(self):
        try:
            st = shutil.disk_usage(self.cale_curenta); tot, lib, oc = st.total/(1024**3), st.free/(1024**3), int((st.used/st.total)*100)
            col = "#a6e3a1" if oc < 60 else ("#fab387" if oc < 85 else "#f38ba8")
            self.bara_progres_spatiu.setStyleSheet(f"QProgressBar {{ border: 1px solid #45475a; border-radius: 5px; background-color: #313244; }} QProgressBar::chunk {{ background-color: {col}; border-radius: 4px; }}")
            self.bara_progres_spatiu.setValue(oc); L = self.window().limba_curenta if self.window() and hasattr(self.window(), 'limba_curenta') else "ro"
            F = {"ro": f"Liber: {lib:.1f} GB ({100-oc}% Free) din {tot:.0f} GB", "en": f"Free: {lib:.1f} GB ({100-oc}% Free) of {tot:.0f} GB", "it": f"Disponibile: {lib:.1f} GB ({100-oc}% Free) di {tot:.0f} GB"}
            self.lbl_spatiu.setText(F[L])
        except Exception: self.lbl_spatiu.setText("Disk: --"); self.bara_progres_spatiu.setValue(0)
    def obtine_dimensiune_formatata(self, cale):
        try:
            if os.path.islink(cale): return "[Link]"
            if not os.access(cale, os.R_OK): return "[Protejat]"
            sz = os.path.getsize(cale)
            for u in ['B', 'KB', 'MB', 'GB']:
                if sz < 1024.0: return f"{sz:.1f} {u}"
                sz /= 1024.0
            return f"{sz:.1f} TB"
        except Exception: return "[Protejat]"
    def actualizeaza_lista(self):
        self.lista.clear(); self.edit_filtru.clear()
        if self.cale_curenta != '/': self.lista.addItem(QListWidgetItem("📁 .. (Mergi Inapoi)"))
        ad = self.window().calculeaza_dimensiuni if self.window() and hasattr(self.window(), 'calculeaza_dimensiuni') else False
        try:
            items = os.listdir(self.cale_curenta); fld, fis = [], []
            for e in items:
                if e.startswith('.') and not self.arata_ascunse and e != '..': continue
                if e == "SSD" and self.cale_curenta.startswith("/media"): continue
                if os.path.isdir(os.path.join(self.cale_curenta, e)): fld.append(e)
                else: fis.append(e)
            fld.sort(key=str.lower); fis.sort(key=str.lower)
            for f in fld: self.lista.addItem(QListWidgetItem(f"📁 {f}"))
            for f in fis:
                d = self.obtine_dimensiune_formatata(os.path.join(self.cale_curenta, f)) if ad else ""
                self.lista.addItem(QListWidgetItem(f"📄 {f}   ({d})" if ad else f"📄 {f}"))
        except PermissionError: self.lista.addItem(QListWidgetItem("❌ Acces interzis (Protejat)"))
        self.actualizeaza_butoane(); self.actualizeaza_indicator_spatiu()
    def deschide_meniu_contextual(self, poz):
        global CLIPBOARD_CALE_SURSA, CLIPBOARD_ACTIUNE; item = self.lista.itemAt(poz); meniu = QMenu(self)
        meniu.setStyleSheet("background-color: #313244; color: #cdd6f4; font-size: 13px;")
        L = self.window().limba_curenta if self.window() and hasattr(self.window(), 'limba_curenta') else "ro"
        C = {"ro": ["📋 Copiaza", "✂️ Taie (Cut)", "🗑️ Sterge", "📥 Lipeste aici"], "en": ["📋 Copy", "✂️ Cut", "🗑️ Delete", "📥 Paste here"], "it": ["📋 Copia", "✂️ Taglia", "🗑️ Elimina", "📥 Incolla qui"]}
        if item and ".. (Mergi Inapoi)" not in item.text():
            tb = item.text()[2:]; el = tb.split("   (").strip() if "   (" in tb else tb; cc = os.path.join(self.cale_curenta, el)
            ac, ax = meniu.addAction(C[L]), meniu.addAction(C[L]); meniu.addSeparator(); ad = meniu.addAction(C[L])
            ap = meniu.addAction(C[L]) if CLIPBOARD_CALE_SURSA and os.path.exists(CLIPBOARD_CALE_SURSA) else None
            sel = meniu.exec(self.lista.mapToGlobal(poz))
            if sel == ac: CLIPBOARD_CALE_SURSA, CLIPBOARD_ACTIUNE = cc, 'copy'
            elif sel == ax: CLIPBOARD_CALE_SURSA, CLIPBOARD_ACTIUNE = cc, 'cut'
            elif sel == ad:
                if self.window(): self.window().actiune_stergere()
            elif ap and sel == ap: self.executa_paste()
        else:
            if CLIPBOARD_CALE_SURSA and os.path.exists(CLIPBOARD_CALE_SURSA):
                ap = meniu.addAction(C[L]); sel = meniu.exec(self.lista.mapToGlobal(poz))
                if sel == ap: self.executa_paste()
    def executa_paste(self):
        global CLIPBOARD_CALE_SURSA, CLIPBOARD_ACTIUNE; 
        if not CLIPBOARD_CALE_SURSA: return
        dc = os.path.join(self.cale_curenta, os.path.basename(CLIPBOARD_CALE_SURSA))
        try:
            if CLIPBOARD_ACTIUNE == 'copy':
                if os.path.isdir(CLIPBOARD_CALE_SURSA): shutil.copytree(CLIPBOARD_CALE_SURSA, dc)
                else: shutil.copy2(CLIPBOARD_CALE_SURSA, dc)
            elif CLIPBOARD_ACTIUNE == 'cut': shutil.move(CLIPBOARD_CALE_SURSA, dc); CLIPBOARD_CALE_SURSA, CLIPBOARD_ACTIUNE = None, None
            if self.window(): self.window().strat_sus.actualizeaza_lista(); self.window().strat_jos.actualizeaza_lista()
        except Exception as e: QMessageBox.critical(self, "Error", f"Paste failed: {e}")
    def schimba_calea_manual(self):
        t = self.edit_cale.text().strip()
        if os.path.exists(t) and os.path.isdir(t): self.istoric_inapoi.append(self.cale_curenta); self.istoric_inainte.clear(); self.cale_curenta = t; self.actualizeaza_lista(); self.cale_schimbata.emit()
        else: QMessageBox.warning(self, "Error", "Path does not exist!"); self.edit_cale.setText(self.cale_curenta)
    def click_inapoi(self):
        if self.istoric_inapoi: self.istoric_inainte.append(self.cale_curenta); self.cale_curenta = self.istoric_inapoi.pop(); self.actualizeaza_lista(); self.cale_schimbata.emit()
    def click_inainte(self):
        if self.istoric_inainte: self.istoric_inapoi.append(self.cale_curenta); self.cale_curenta = self.istoric_inainte.pop(); self.actualizeaza_lista(); self.cale_schimbata.emit()
    def navigheaza(self, item):
        txt = item.text()
        if ".. (Mergi Inapoi)" in txt: self.istoric_inapoi.append(self.cale_curenta); self.istoric_inainte.clear(); self.cale_curenta = os.path.dirname(self.cale_curenta); self.actualizeaza_lista(); self.cale_schimbata.emit()
        else:
            tb = txt[2:]; el = tb.split("   (").strip() if "   (" in tb else tb; cc = os.path.join(self.cale_curenta, el)
            if os.path.isdir(cc): self.istoric_inapoi.append(self.cale_curenta); self.istoric_inainte.clear(); self.cale_curenta = cc; self.actualizeaza_lista(); self.cale_schimbata.emit()
            else: subprocess.Popen(['xdg-open', cc], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
