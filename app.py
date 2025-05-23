from flask import Flask, request, jsonify
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

clientes_emails = {
    "Gustavo": "suporte@proprinter.com.br",
    "Suporte": "suporte@proprinter.com.br",
    "Impressora": "impressoras@proprinter.com.br",
    "Felipe": "felipe@proprinter.com.br"
}

# Variável para guardar a última localização do técnico
localizacao_tecnico = {"latitude": None, "longitude": None}

@app.route("/")
def index():
    return "API ProPrinter rodando."

@app.route("/avisar", methods=["POST"])
def avisar():
    nome_cliente = request.form.get("nome_cliente")
    email_cliente = clientes_emails.get(nome_cliente)

    if not email_cliente:
        return f"Cliente {nome_cliente} não encontrado.", 400

    email_user = os.getenv("EMAIL_USER")
    email_pass = os.getenv("EMAIL_PASS")

    if not email_user or not email_pass:
        return "Configurações de email não encontradas.", 500

    # Construir mensagem incluindo link para localização se disponível
    lat = localizacao_tecnico.get("latitude")
    lng = localizacao_tecnico.get("longitude")

    msg = MIMEMultipart()
    msg['From'] = email_user
    msg['To'] = email_cliente
    msg['Subject'] = "Técnico a caminho - ProPrinter"

    if lat is not None and lng is not None:
        mapa_link = f"https://www.google.com/maps?q={lat},{lng}"
        body = f"O técnico está a caminho do cliente: {nome_cliente}.\nLocalização atual do técnico: {mapa_link}"
    else:
        body = f"O técnico está a caminho do cliente: {nome_cliente}.\nLocalização do técnico não disponível no momento."

    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email_user, email_pass)
        server.sendmail(email_user, email_cliente, msg.as_string())
        server.quit()
    except Exception as e:
        return f"Erro ao enviar email: {e}", 500

    return f"Notificação enviada para {nome_cliente} no email {email_cliente}!"

@app.route("/atualizar_localizacao", methods=["POST"])
def atualizar_localizacao():
    data = request.json
    lat = data.get("latitude")
    lng = data.get("longitude")
    if lat is None or lng is None:
        return jsonify({"error": "Faltando latitude ou longitude"}), 400
    
    localizacao_tecnico["latitude"] = lat
    localizacao_tecnico["longitude"] = lng
    return jsonify({"message": "Localização atualizada!"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
