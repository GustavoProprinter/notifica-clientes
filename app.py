from flask import Flask, render_template, request

app = Flask(__name__)

# Dicionário para mapear nome do cliente para email
clientes_emails = {
    "Gustavo": "gustavo@proprinter.com.br",
    "Suporte": "suporte@proprinter.com.br",
    "Impressora": "impressora@proprinter.com.br",
    "Felipe": "felipe@proprinter.com.br"
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/avisar", methods=["POST"])
def avisar():
    nome_cliente = request.form.get("nome_cliente")
    email_cliente = clientes_emails.get(nome_cliente)

    if not email_cliente:
        return f"Cliente {nome_cliente} não encontrado.", 400

    # Aqui você colocaria a lógica para enviar o email, por exemplo.
    # Por enquanto só vai retornar uma mensagem simples.
    return f"Notificação enviada para {nome_cliente} no email {email_cliente}!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
