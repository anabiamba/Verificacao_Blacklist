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
from datetime import datetime
import telegram_send
import requests
import time

servico = Service(ChromeDriverManager().install)

navegador = webdriver.Chrome(service=servico)
navegador.maximize_window()

URL = f"https://www.walledgarden.global/"
ASN = "/html/body/div[2]/header/div[2]/div[2]/form/input"
ENTER = "/html/body/div[2]/header/div[2]/div[2]/form/button/span"
RISCO = "/html/body/div[2]/header/div[2]/div[2]/div/div[2]/span[2]"

# Entrar Walled Garden
navegador.get(URL)

time.sleep(3)
VALORASN = navegador.find_element(By.XPATH, ASN).send_keys(263299)

time.sleep(3)
PENTER = navegador.find_element(By.XPATH, ENTER).click()

time.sleep(15)
NIVELR = navegador.find_element(By.XPATH, RISCO).text

date = datetime.now()
datehour = date.strftime("%d/%m/%Y %H:%M")
horaatual = datetime.now()

if horaatual.hour < 12:
    cumprimento = "Bom dia"
elif 12 <= horaatual.hour < 18:
    cumprimento = "Boa tarde"
else:
    cumprimento = "Boa noite"

MSG = f'''
Nível de segurança do bloco IP 191.6.224.0/21: <b>{NIVELR} </b>
'''
print(MSG)
# todo: enviando a mensagem
try:
    telegram_send.send(messages=[f'{MSG}'],parse_mode='HTML',disable_web_page_preview=True)
    # message = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHATID}&text={MSG}"
    # sendmsg = requests.get(message)
    # sendmsg.raise_for_status()

except requests.exceptions.HTTPError as err:
    raise SystemExit(err)
