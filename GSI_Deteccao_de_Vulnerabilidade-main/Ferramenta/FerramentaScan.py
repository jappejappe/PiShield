from ipaddress import IPv4Network as enderecoValido
from os import system
import xml.etree.ElementTree as ET
import requests
import json
from time import sleep

def varreduraRede():


    while True:
        endereco_ip = str(input("Digite um endereco IP valido: "))
        try:
            endereco_valido = enderecoValido(endereco_ip)
            print(endereco_valido)
            break
        except ValueError:
            print("Endereco IP não existe!")

    sistema = system(f'nmap -sV {endereco_ip} -oX {endereco_ip}.xml')


def tratamentoXML():

    global dictCPE
    dictCPE = {}

    # Carregar o arquivo XML gerado pelo Nmap
    tree = ET.parse('127.0.0.1.xml')
    root = tree.getroot()


    for host in root.findall('host'):
        endereco_host = host.find('address').attrib['addr'] 

        dispositivo = 'N/A'

        for address in host.findall('address'):
            if 'vendor' in address.attrib:
                dispositivo = address.attrib['vendor']
                break 

        print(f"|> Endereço IP: {endereco_host} <|")
        print(f"Dispositivo: {dispositivo}")
        print('▽▽▽▽▽▽▽▽▽▽▽▽▽▽▽▽▽▽▽▽▽▽▽▽▽▽▽▽▽▽▽▽▽▽▽▽▽▽▽▽▽')


        for port in host.findall('ports/port'):
            portid = port.attrib['portid']
            protocol = port.attrib['protocol']
            service = port.find('service') 
            statePort = port.find('state')


            if service is not None:
                name = service.attrib.get('name', 'N/A')
                version = service.attrib.get('version', 'N/A')
                extrainfo = service.attrib.get('extrainfo', 'N/A')
                product = service.attrib.get('product', 'N/A')
                ostype = service.attrib.get('ostype', 'N/A')
                cpe = service.find('cpe')

                if cpe is not None:
                    cpe = cpe.text
                    if endereco_host not in dictCPE: 
                        dictCPE[endereco_host] = []
                    dictCPE[endereco_host].append(cpe)



            if statePort is not None:
                state = statePort.attrib.get('state', 'N/A')


            print(f"Porta: {portid} | Status: {state} |  Protocolo: {protocol} | Serviço: {name} | Produto: {product} | Versão: {version} | Sistema Operacional: {ostype} | CPE: {cpe} | Informação Extra: {extrainfo} |")
        print('△△△△△△△△△△△△△△△△△△△△△△△△△△△△△△△△△△△△△△△△△')

def apiNVD(dictCPE):
    lista_nao_encontrado = []

    with open('.//templates/resultado.html', 'w') as resultado:
         resultado.write("""
    <!DOCTYPE html>
    <html lang='pt-BR'>
    <head>
        <meta charset='UTF-8'>
        <title>Resultado CPE</title>
        <style>
            body {
                font-family: 'Arial', sans-serif;
                margin: 0;
                padding: 20px;
                background-color: #f9f9f9;
                color: #333;
            }
            h1 {
                text-align: center;
                color: #4CAF50;
                margin-bottom: 20px;
                font-size: 2.5em;
            }
            h2 {
                text-align: center;
                color: #333;
                margin-top: 40px;
                font-size: 2em;
            }
            pre {
                display: block;
                white-space: pre-wrap; /* Permite que o conteúdo quebre a linha */
                word-wrap: break-word; /* Quebra palavras muito longas, se necessário */
                font-size: 16px; /* Ajuste para um tamanho de fonte confortável */
                overflow-x: auto; /* Adiciona uma barra de rolagem horizontal se o conteúdo exceder a largura */
                max-width: 100%; /* Garante que o conteúdo não ultrapasse a largura da tela */
            }

        </style>
    </head>
    <body>
        <h1>Resultados da Varredura de CPE</h1>
    """)
    for ip, cpe_list in dictCPE.items():
        for cpe_old in cpe_list:
            cpe_new = cpe_old.replace("/", "2.3:")
            cpe_new_texto = cpe_new.replace(":", "_")

            try:
                nvd = requests.get(f"https://services.nvd.nist.gov/rest/json/cves/2.0?cpeName={cpe_new}:*")
                nvd.raise_for_status()
                nvd_json = nvd.json()


                with open(f'{cpe_new_texto}.json', 'w') as arquivo:
                    json.dump(nvd_json, arquivo, indent=4)

                dados_formatados = json.dumps(nvd_json, indent=4, ensure_ascii=False)
                

                with open('.//templates/resultado.html', 'a') as resultado:
                    resultado.write(f"<h2>Resultados para {cpe_new}</h2>\n")
                    resultado.write(f"<pre>{dados_formatados}</pre>\n")

            except requests.RequestException as e:
                print(f"Falha na solicitação para {cpe_new}: {e}")
                lista_nao_encontrado.append(cpe_new)

            except Exception as e:
                print(f"Erro inesperado ao processar {cpe_new}: {e}")

            sleep(5)

    # Fechar o corpo do HTML
    with open('.//templates/resultado.html', 'a') as resultado:
        resultado.write("</body>\n</html>")

    print("CPES não encontrados:", lista_nao_encontrado)
    print("Lista criada e finalizado!")

varreduraRede()
tratamentoXML()
apiNVD(dictCPE)