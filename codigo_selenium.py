from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import time

login = 'YOUR_LOGIN_ACME'
password = 'YOUR_PASSWORD_ACME'
navegador = webdriver.Chrome()
navegador.get("https://acme-test.uipath.com/login")
navegador.maximize_window()
navegador.find_element("name","email").send_keys(login)
navegador.find_element("name","password").send_keys(password)
navegador.find_element(By.XPATH, "/html/body/div/div[2]/div/div/div/form/button").click()
navegador.find_element(By.XPATH, "//*[@id='dashmenu']/div[2]/a/button").click()
# Localizar a tabela de uma vez e capturar todas as linhas
tabela = navegador.find_element(By.CLASS_NAME, "table")
def extrair_tabela():
    tabela = navegador.find_element(By.CLASS_NAME, "table")
    linhas = tabela.find_elements(By.TAG_NAME, "tr")
    dados_pagina = []
    for linha in linhas:
        celulas = linha.find_elements(By.TAG_NAME, "td")
        linha_dados = [celula.text for celula in celulas]
        if linha_dados:  # Ignorar linhas vazias
            dados_pagina.append(linha_dados)
    return dados_pagina

# Inicializar lista para armazenar todos os dados
dados_totais = []

# Loop para navegar por todas as páginas
while True:
    # Extrair os dados da tabela na página atual
    dados_totais.extend(extrair_tabela())
    
    try:
        # Tentar localizar o botão "Próxima Página"
        botao_proxima_pagina = navegador.find_element(By.XPATH, "//a[@rel='next']")
        botao_proxima_pagina.click()  # Ir para a próxima página
    except NoSuchElementException:
        # Se não houver o botão, terminamos de navegar
        print("Última página alcançada.")
        break

# Criar um DataFrame com os dados coletados
colunas = ["Actions","WIID", "Description", "Type", "Status", "Date"]  # Cabeçalhos sem a coluna "Actions"
df = pd.DataFrame(dados_totais, columns=colunas)

# Exportar para um arquivo Excel
df.to_excel("Work Items.xlsx", index=False, sheet_name="Work Items")
for linha in dados_totais:
    print(linha)
time.sleep(6)