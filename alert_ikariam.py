import os
import requests
from bs4 import BeautifulSoup

# === Configuration ===
ISLAND_URL = "https://s61-fr.ikariam.gameforge.com/?view=island&islandId=4407"
WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")  # stocké dans Render pour sécurité

def send_discord_alert(message: str):
    """Envoie une alerte sur Discord"""
    try:
        payload = {"content": message}
        response = requests.post(WEBHOOK_URL, json=payload)
        if response.status_code == 204:
            print("✅ Alerte envoyée sur Discord")
        else:
            print(f"⚠️ Erreur Discord: {response.status_code}")
    except Exception as e:
        print(f"❌ Exception Discord : {e}")

def check_slots():
    """Vérifie s’il y a des emplacements libres sur l’île"""
    try:
        response = requests.get(ISLAND_URL)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        towns = soup.select(".cityLocationForms")
        free_slots = sum("buildPlace" in t.get("class", []) for t in towns)

        if free_slots > 0:
            send_discord_alert(
                f"🎉 Une place s'est libérée ! ({free_slots} slot(s) dispo)\n{ISLAND_URL}"
            )
        else:
            print("⏳ Pas de place libre pour le moment.")
    except Exception as e:
        print(f"❌ Erreur lors du check: {e}")

if __name__ == "__main__":
    check_slots()
