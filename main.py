# coding: utf-8
# Automatização da inadimplência do dia
# Abrir o navegador
# Entrar no sistema RadiusNET
# Buscar a inadimplência dos últimos três meses
# Enviar por whatsapp o resultado da pesquisa

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import requests
import time
from datetime import datetime

servico = Service(ChromeDriverManager().install())

navegador = webdriver.Chrome(service=servico)
navegador.maximize_window()

TOKEN = "979041370:AAGCAmZAu-_sBK4KJD-v_Io9H0MK09C1Hmw"
CHATID = "-718957161"

URL = f"https://mxtoolbox.com/SuperTool.aspx?action=blacklist:cloudmail.fibrafaciltelecom.com.br&run=toolpage"
HOST = "/html/body/form/div[3]/div[2]/div[2]/div/div[2]/div[2]/span/div/div[3]/strong[1]"
IP = "/html/body/form/div[3]/div[2]/div[2]/div/div[2]/div[2]/span/div/div[3]/span/strong"
LISTAS = "/html/body/form/div[3]/div[2]/div[2]/div/div[2]/div[2]/span/div/div[3]/strong[2]"
LISTADOS = "/html/body/form/div[3]/div[2]/div[2]/div/div[2]/div[2]/span/div/div[3]/strong[3]"
SEM_RESPOSTA = "/html/body/form/div[3]/div[2]/div[2]/div/div[2]/div[2]/span/div/div[3]/strong[4]"


# Entrar MXTOOLBOX
navegador.get(URL)

time.sleep(3)
VALORHOST = navegador.find_element(By.XPATH, HOST).text

time.sleep(3)
VALORIP = navegador.find_element(By.XPATH, IP).text

time.sleep(3)
VALORLISTA = navegador.find_element(By.XPATH, LISTAS).text

time.sleep(3)
VALORLISTADOS = navegador.find_element(By.XPATH, LISTADOS).text

time.sleep(3)
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

MSG = f'''
{cumprimento}, pessoal. Segue status sobre BlackList do servidor {hostname} em {VALORIP}:
    
HORA: {datehour}
CHECADOS: {VALORLISTA}
LISTADOS: {VALORLISTADOS}
SEM RESPOSTA: {VALORSEMRES}

Clique no link a seguir para ver os detalhes: https://mxtoolbox.com/SuperTool.aspx?action=blacklist:cloudmail.fibrafaciltelecom.com.br&run=toolpage


'''




# todo: enviando a mensagem
try:
    message = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHATID}&text={MSG}"
    sendmsg = requests.get(message)
    sendmsg.raise_for_status()
except requests.exceptions.HTTPError as err:
    raise SystemExit(err)
