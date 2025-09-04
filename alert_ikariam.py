import requests
from bs4 import BeautifulSoup
import time

# Configuration
ISLAND_URL = "https://s61-fr.ikariam.gameforge.com/?view=island&id=4407"
WEBHOOK_URL = "https://discord.com/api/webhooks/1413129396444725340/WJ0NiorckGfmFE5OT1f7Z6q38HDS8q0WqV4wgcumHcaB2npkSqN5LoroeQLe21BjaqP"

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

        # On prend tous les liens des emplacements de ville
        slots = soup.select("a.link_img.island_feature_img")

        # On filtre ceux dont le title correspond à un emplacement libre
        free_slots = [s for s in slots if "Voulez-vous bâtir une colonie ici" in s.get("title", "")]

        if free_slots:
            send_discord_alert(f"🎉 Une place LIBRE trouvée ! ({len(free_slots)} dispo) 👉 {ISLAND_URL}")
        else:
            print("⏳ Pas de place libre pour le moment.")
    except Exception as e:
        print(f"❌ Erreur lors du check: {e}")

if __name__ == "__main__":
    while True:
        check_slots()
        time.sleep(15)  # Vérifie toutes les 15 secondes
