from fastapi import FastAPI
from pydantic import BaseModel
import google.generativeai as genai
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os

# 1. SUNUCU VE BAĞLANTI AYARLARI
app = FastAPI(title="Spor Toto Chatbot Merkezi")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. YAPAY ZEKA BEYNİNİ BAĞLA
# DİKKAT: Aşağıdaki tırnakların içine çalışan kendi VIP anahtarını (AQ.Ab8...) yapıştır!
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)
sohbet_yapay_zekasi = genai.GenerativeModel('gemini-3.5-flash')

# 3. CHAT GİRİŞ MODELİ
class ChatIstegi(BaseModel):
    mesaj: str

# 4. WEB CHAT EKRANINI AÇMA KOMUTU
@app.get("/")
def ana_sayfayi_ac():
    return FileResponse("index.html")

# 5. CHAT ANALİZ MOTORU
@app.post("/chat-et")
def chat_et(istek: ChatIstegi):
    
    gizli_talimat = f"""
    Sen acımasız, gerçekçi ve son derece profesyonel bir Spor Toto ve İddaa analistisin.
    Kullanıcı sana doğrudan bir sohbet ortamında mesaj yazıyor. Mesajında bahsettiği maçları, sakatlıkları veya fikirleri analiz etmelisin.
    
    Kullanıcının Mesajı: "{istek.mesaj}"
    
    SOHBET VE ANALİZ KURALLARIN:
    1. Kullanıcıya doğrudan bir sohbet arkadaşı gibi hitap et ama analizlerinde ciddiyetten ve rasyonellikten ödün verme.
    2. Eğer bir maç tahmini isteniyorsa; kesinlikle maçı taktiksel olarak yorumla, ev sahibi/beraberlik/deplasman yüzdelerini (%) açıkça ver.
    3. Spor Toto için en mantıklı net tercihi (1, 0 veya 2) gerekçesiyle yaz.
    4. Mutlaka alternatif bir profesyonel kupon tavsiyesi (Çifte şans, alt/üst veya kg var/yok gibi) ekle.
    5. Eğer kullanıcı maç harici sporla ilgili bir soru sorduysa, profesyonel analist kimliğini bozmadan sohbeti sürdür.
    """
    
    cevap = sohbet_yapay_zekasi.generate_content(gizli_talimat)
    return {"analiz": cevap.text}
