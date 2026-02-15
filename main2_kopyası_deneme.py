import random
from flask import Flask, render_template, request, jsonify, session

app = Flask(__name__)
app.secret_key = "linguavox_gizli_anahtar_degistir"

kelime_db = {
    "kolay": [
        {"tr": "Elma",  "en": "Apple"}, {"tr": "Kedi",   "en": "Cat"},
        {"tr": "Su",    "en": "Water"}, {"tr": "Masa",   "en": "Table"},
        {"tr": "Mavi",  "en": "Blue"},  {"tr": "Kapı",   "en": "Door"},
        {"tr": "Süt",   "en": "Milk"},  {"tr": "Mutlu",  "en": "Happy"},
        {"tr": "Kitap", "en": "Book"},  {"tr": "Okul",   "en": "School"},
    ],
    "orta": [
        {"tr": "Bahçe",       "en": "Garden"},    {"tr": "Hava Durumu", "en": "Weather"},
        {"tr": "Macera",      "en": "Adventure"}, {"tr": "Tehlikeli",   "en": "Dangerous"},
        {"tr": "Yarın",       "en": "Tomorrow"},  {"tr": "Kütüphane",   "en": "Library"},
        {"tr": "Sincap",      "en": "Squirrel"},  {"tr": "Başarılı",    "en": "Successful"},
        {"tr": "Çarşamba",    "en": "Wednesday"}, {"tr": "Dil",         "en": "Language"},
    ],
    "zor": [
        {"tr": "Albay",      "en": "Colonel"},     {"tr": "Kuyruk",    "en": "Queue"},
        {"tr": "Vicdan",     "en": "Conscience"},  {"tr": "Kaos",      "en": "Chaos"},
        {"tr": "Program",    "en": "Schedule"},    {"tr": "Girişimci", "en": "Entrepreneur"},
        {"tr": "Psikoloji",  "en": "Psychology"},  {"tr": "Koro",      "en": "Choir"},
        {"tr": "Kapsamlı",   "en": "Thorough"},    {"tr": "Hiyerarşi", "en": "Hierarchy"},
    ],
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/kelime-listesi", methods=["POST"])
def kelime_listesi_getir():
    data   = request.get_json()
    zorluk = data.get("zorluk", "kolay")
    if zorluk not in kelime_db:
        return jsonify({"hata": "Geçersiz zorluk seviyesi"}), 400
    liste = kelime_db[zorluk].copy()
    random.shuffle(liste)
    session["puan"]   = 0
    session["dogru"]  = 0
    session["yanlis"] = 0
    session["zorluk"] = zorluk
    return jsonify({"kelimeler": liste})

@app.route("/kontrol", methods=["POST"])
def kontrol():
    data         = request.get_json()
    tanilan      = data.get("tanilan", "").strip()
    dogru_kelime = data.get("dogru_kelime", "").strip()
    if not dogru_kelime:
        return jsonify({"hata": "dogru_kelime parametresi eksik"}), 400
    dogru_mu = tanilan.lower() == dogru_kelime.lower()
    if dogru_mu:
        session["puan"]  = session.get("puan",  0) + 10
        session["dogru"] = session.get("dogru", 0) + 1
    else:
        session["yanlis"] = session.get("yanlis", 0) + 1
    return jsonify({
        "sonuc":         "dogru" if dogru_mu else "yanlis",
        "puan":          session.get("puan",  0),
        "dogru_sayisi":  session.get("dogru", 0),
        "yanlis_sayisi": session.get("yanlis", 0),
    })

@app.route("/ozet", methods=["GET"])
def ozet():
    return jsonify({
        "puan":   session.get("puan",   0),
        "dogru":  session.get("dogru",  0),
        "yanlis": session.get("yanlis", 0),
        "zorluk": session.get("zorluk", "—"),
    })

if __name__ == "__main__":
    app.run(debug=True)