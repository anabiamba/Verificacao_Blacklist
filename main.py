# coding: utf-8
# Automatização da inadimplência do dia
# Abrir o navegador
# Entrar no sistema RadiusNET
# Buscar a inadimplência dos últimos três meses
# Enviar por whatsapp o resultado da pesquisa
import option as option
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from datetime import datetime
import telegram_send
import requests
import time

#driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

servico = Service(ChromeDriverManager().install())

navegador = webdriver.Chrome(service=servico)
navegador.maximize_window()

TOKEN = "1023306274:AAGRg6kUTLkYfe97jf5GRreLbw3oG4ZbHLE"
#CHATID = "-718957161"
#CHATID = "-529875532"
CHATID = "-1001801395887"

URL = f"https://mxtoolbox.com/SuperTool.aspx?action=blacklist:cloudmail.fibrafaciltelecom.com.br&run=toolpage"
#HOST = "/html/body/form/div[3]/div[2]/div[2]/div/div[2]/div[2]/span/div/div[3]/strong[1]"
HOST = "/html/body/form/div[3]/div[2]/div[2]/div/div[2]/div[2]/span/div/div[3]/strong[1]"
IP = "/html/body/form/div[3]/div[2]/div[2]/div/div[2]/div[2]/span/div/div[3]/span/strong"
LISTAS = "/html/body/form/div[3]/div[2]/div[2]/div/div[2]/div[2]/span/div/div[3]/strong[2]"
LISTADOS = "/html/body/form/div[3]/div[2]/div[2]/div/div[2]/div[2]/span/div/div[3]/strong[3]"
SEM_RESPOSTA = "/html/body/form/div[3]/div[2]/div[2]/div/div[2]/div[2]/span/div/div[3]/strong[4]"


# Entrar MXTOOLBOX
navegador.get(URL)

time.sleep(10)
VALORHOST = navegador.find_element(By.XPATH, HOST).text

time.sleep(10)
VALORIP = navegador.find_element(By.XPATH, IP).text

time.sleep(10)
VALORLISTA = navegador.find_element(By.XPATH, LISTAS).text

time.sleep(10)
VALORLISTADOS = navegador.find_element(By.XPATH, LISTADOS).text

time.sleep(10)
VALORSEMRES = navegador.find_element(By.XPATH, SEM_RESPOSTA).text

server = VALORHOST.upper().split(".")
hostname = server[0]

date = datetime.now()
datehour = date.strftime("%d/%m/%Y %H:%M")
horaatual = datetime.now()
#separar = datehour.split(" ")
#hora = separar[1]
#separar_min = hora.split(":")
#min = separar_min[0]

if horaatual.hour < 12:
    cumprimento = "Bom dia"
elif 12 <= horaatual.hour < 18:
    cumprimento = "Boa tarde"
else:
    cumprimento = "Boa noite"

LISTADO = "ESTÁ LISTADO" if int(VALORLISTADOS) > 0 else "NÃO ESTÁ LISTADO"


MSG = f'''
{cumprimento}, pessoal! Segue status sobre BlackList do servidor <a href='https://cloudmail.fibrafaciltelecom.com.br' >{hostname}</a> em <a href='https://cloudmail.fibrafaciltelecom.com.br/iredadmin' >{VALORIP}</a>:
    
LISTAS: {VALORLISTA}
CONTIDO EM: {VALORLISTADOS}
SEM RESPOSTA: {VALORSEMRES}

O servidor <b>{LISTADO}</b> em <b>BLACKLISTS</b>. Ver detalhes <a href='https://mxtoolbox.com/SuperTool.aspx?action=blacklist:cloudmail.fibrafaciltelecom.com.br&run=toolpage' ><b>AQUI</b></a>

'''
# todo: enviando a mensagem
try:
    telegram_send.send(messages=[f'{MSG}'],parse_mode='HTML',disable_web_page_preview=True)
    # message = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHATID}&text={MSG}"
    # sendmsg = requests.get(message)
    # sendmsg.raise_for_status()

except requests.exceptions.HTTPError as err:
    raise SystemExit(err)
