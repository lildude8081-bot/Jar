import os
import subprocess

def proceseaza_salt_locatie(tip_locatie):
    try:
        login_name = os.getlogin()
    except Exception:
        login_name = os.environ.get("USER", "mihai")
        
    if tip_locatie == "home":
        return os.path.expanduser('~')
        
    elif tip_locatie == "media":
        try:
            # Întrebăm sistemul unde este montat exact sda3 (SSD-ul de 240GB)
            rezultat = subprocess.check_output(['findmnt', '-rn', '-o', 'TARGET', '/dev/sda3'], text=True)
            cale_ssd = rezultat.strip()
            if cale_ssd and os.path.exists(cale_ssd):
                return cale_ssd
        except Exception:
            pass
            
        baza_media = f"/media/{login_name}"
        if os.path.exists(baza_media):
            sub_foldere = [f for f in os.listdir(baza_media) if not f.startswith('.')]
            if sub_foldere:
                return os.path.join(baza_media, sub_foldere[0])
            return baza_media
        return "/media"
        
    elif tip_locatie == "mnt":
        # REZOLVARE PROFESIONALĂ: Deoarece /mnt este gol, trimitem utilizatorul în folderul media general
        # Aici Linux Mint afișează toate discurile, stick-urile și partițiile atașate!
        baza_user_media = f"/media/{login_name}"
        return baza_user_media if os.path.exists(baza_user_media) else "/media"
        
    elif tip_locatie == "root":
        return "/"
        
    elif tip_locatie == "network":
        uid = os.getuid() if hasattr(os, 'getuid') else 1000
        cale_gvfs = f"/run/user/{uid}/gvfs"
        if os.path.exists(cale_gvfs):
            return cale_gvfs
        cale_alt = os.path.expanduser('~/.gvfs')
        return cale_alt if os.path.exists(cale_alt) else "/"
        
    return None
