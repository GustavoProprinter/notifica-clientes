import os
from flask import Flask, render_template, request, redirect, url_for, flash
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'

# Variáveis de ambiente para e-mail
EMAIL = os.getenv('EMAIL_USER', 'impressoras@proprinter.com.br')
PASSWORD = os.getenv('EMAIL_PASS', 'senha_falsa_aqui')

def enviar_email(destinatario, assunto, corpo):
    msg = MIMEText(corpo, 'html')
    msg['Subject'] = assunto
    msg['From'] = EMAIL
    msg['To'] = destinatario

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(EMAIL, PASSWORD)
            server.sendmail(EMAIL, destinatario, msg.as_string())
        return True
    except Exception as e:
        print(f"Erro ao enviar email: {e}")
        return False

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/avisar', methods=['POST'])
def avisar():
    nome_cliente = request.form['nome_cliente']

    # Nome → E-mail
    clientes = {
        'Gustavo': 'g7761273@gmail.com',
        'Suporte': 'suporte@proprinter.com.br',
        'Impressora': 'impressoras@proprinter.com.br'
    }

    email_cliente = clientes.get(nome_cliente)

    assunto = 'Técnico a caminho'
    corpo = f'''
    <h2>Técnico a caminho</h2>
    <p>Olá <strong>{nome_cliente}</strong>,</p>
    <p>Seu técnico já está a caminho para atender o chamado.</p>
    <p>Atenciosamente,<br>Equipe ProPrinter.</p>
    '''

    if enviar_email(email_cliente, assunto, corpo):
        flash('E-mail enviado com sucesso!')
    else:
        flash('Erro ao enviar e-mail.')

    return redirect(url_for('home'))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
