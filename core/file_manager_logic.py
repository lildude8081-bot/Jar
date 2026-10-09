import os
import shutil

def obtine_element_selectat(lista_sus, lista_jos, cale_sus, cale_jos):
    if lista_sus.hasFocus() and lista_sus.currentItem():
        return lista_sus, cale_sus, lista_sus.currentItem().text()[2:]
    if lista_jos.hasFocus() and lista_jos.currentItem():
        return lista_jos, cale_jos, lista_jos.currentItem().text()[2:]
    return None, None, None

def sterge_element(calea, element):
    cale_completa = os.path.join(calea, element)
    if os.path.isdir(cale_completa):
        shutil.rmtree(cale_completa)
    else:
        os.remove(cale_completa)

def creeaza_folder_nou(calea, nume):
    os.makedirs(os.path.join(calea, nume), existence_ok=True)

def muta_element(calea_sursa, calea_dest, element):
    shutil.move(os.path.join(calea_sursa, element), os.path.join(calea_dest, element))

def redenumeste_element(calea, nume_vechi, nume_nou):
    vechi_complet = os.path.join(calea, nume_vechi)
    nou_complet = os.path.join(calea, nume_nou)
    os.rename(vechi_complet, nou_complet)
