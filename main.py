
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests, smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BYBIT_API_KEY = "PfSsUrmzKN5yZsHH1Y"
BYBIT_API_SECRET = "iQKSKXQjFf3sKaHNxQ6E2itj2qrhNOPERIiu"
ADMIN_WALLET = "1Je1Mk9YBCBk4JaHixw4KKs2iYJjv9x88Y"
CUENTA_QIK_ADMIN = "1005285212"

class RetiroBTC(BaseModel):
    wallet: str
    monto: float

class RetiroQik(BaseModel):
    wallet: str
    montoRD: str
    montoBTC: str

@app.post("/retirar")
def retirar_btc(data: RetiroBTC):
    if data.monto < 0.000075:
        return {"error": "Monto mínimo no alcanzado"}

    comision = round(data.monto * 0.05, 8)
    monto_final = round(data.monto - comision, 8)

    # Simulación de envío real con Bybit Spot API (transferencia interna)
    # Aquí deberías usar la API real con firma HMAC SHA256 y endpoint correcto

    # Devolver respuesta simulada
    return {
        "msg": "Transacción enviada",
        "enviado": monto_final,
        "comision": comision,
        "wallet_destino": data.wallet,
        "wallet_admin": ADMIN_WALLET
    }

@app.post("/retirar-qik")
def retirar_qik(data: RetiroQik):
    msg = MIMEMultipart()
    msg['From'] = "btcminero@notificaciones.com"
    msg['To'] = "teudy58@gmail.com"
    msg['Subject'] = "📤 Retiro solicitado a Qik Banco"

    body = f"""
    Se ha solicitado un retiro en pesos dominicanos (RD$) vía Qik Banco:

    🧾 Wallet BTC del usuario: {data.wallet}
    🏦 Cuenta Qik (fija): {CUENTA_QIK_ADMIN}
    💰 Monto en BTC: {data.montoBTC}
    🇩🇴 Monto en RD$: {data.montoRD}

    👉 Esta transferencia debe ser procesada manualmente por el administrador.
    """
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login("teudy58@gmail.com", "clave-app-o-token")  # Cambiar por clave de app
        server.sendmail(msg['From'], msg['To'], msg.as_string())
        server.quit()
        return {"msg": "Correo enviado al administrador."}
    except Exception as e:
        return {"error": f"Error al enviar correo: {str(e)}"}
