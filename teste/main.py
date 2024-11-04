from flask import Flask, render_template, send_file, jsonify
import threading
import subprocess
import os

app = Flask(__name__)

# Caminho para o script Python que gera o XML
script = 'GSI_Deteccao_de_Vulnerabilidade-main\\Ferramenta\\FerramentaScan.py'
# Caminho para o arquivo XML gerado
resultado = '.\\templates\\resultado.html'

def executar():
        subprocess.run(['python', script], check=True)
        return send_file('..\\templates\\resultado.html')

@app.route('/')
def home():
    return send_file("../templates/home.html")
        

@app.route('/executar')
def run_script():
    # Executa o script Python que gera o XML
    return executar()

@app.route('/check_xml')
def check_xml():
    file_exists = os.path.isfile('/abc.txt')
    return jsonify({'exists': file_exists})

@app.route('/resultado')
def resultado():
    if os.path.exists(resultado):
        with open (resultado, 'r') as resultado:
            if os.path.exists(cpe):
                with open (cpe, 'w') as cpe:
                    cpeCont = cpe.read()
                    resultado.write(cpeCont)
                    return send_file(resultado)
    else:
        return 'Arquivo XML não encontrado.'

if __name__ == '__main__':
    app.run(debug=True)