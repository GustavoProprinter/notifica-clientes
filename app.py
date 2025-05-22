from flask import Flask, render_template, request
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/avisar", methods=["POST"])
def avisar():
    nome = request.form["nome_cliente"]
    
    destinatario_cliente = f"{nome.lower()}@proprinter.com.br"
    destinatarios = [destinatario_cliente, "felipe@proprinter.com.br"]

    corpo = f"""
    Olá {nome},

    O técnico da ProPrinter está a caminho para atender ao chamado.

    Por favor, esteja disponível para recebê-lo.

    Att,
    Equipe ProPrinter
    """

    msg = MIMEText(corpo)
    msg['Subject'] = "Técnico a caminho - ProPrinter"
    msg['From'] = "seu-email@dominio.com"  # Altere para seu e-mail remetente
    msg['To'] = ", ".join(destinatarios)

    try:
        with smtplib.SMTP("smtp.seudominio.com", 587) as server:  # Ajuste para seu SMTP
            server.starttls()
            server.login("seu-usuario", "sua-senha")  # Substitua por suas credenciais
            server.send_message(msg)
        return f"Notificação enviada para {nome} e cópia para gestor!"
    except Exception as e:
        return f"Erro ao enviar e-mail: {str(e)}"

if __name__ == "__main__":
    app.run(debug=True)
