import os
import json

SAVE_FAIL = "savegame.json"

def salvesta_mang(mängija, olek, kaart):
    """Salvestab mängu oleku JSON faili."""
    andmed = {
        "pix_x": mängija.pix_x,
        "pix_y": mängija.pix_y,
        "olek":  olek,
        "kaart": kaart if olek == "mäng" else None,
    }
    with open(SAVE_FAIL, "w") as f:
        json.dump(andmed, f)
    print("Mäng salvestatud!")

def lae_mang(mängija):
    """Laeb mängu oleku JSON failist. Tagastab (olek, kaart) või None kui faili pole."""
    if not os.path.exists(SAVE_FAIL):
        print("Salvestust ei leitud!")
        return None

    with open(SAVE_FAIL, "r") as f:
        andmed = json.load(f)

    mängija.pix_x = float(andmed["pix_x"])
    mängija.pix_y = float(andmed["pix_y"])

    print("Mäng laetud!")
    return andmed["olek"], andmed.get("kaart")