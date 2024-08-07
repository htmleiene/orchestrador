from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def main():
    try:
        print("Iniciando o script...")
        driver = webdriver.Chrome()
        print("Chrome iniciado...")
        driver.get("https://www.google.com")
        print("Google aberto...")
        search_box = driver.find_element("name", "q")
        print("Campo de pesquisa encontrado...")
        search_box.send_keys("OpenAI ChatGPT")
        search_box.send_keys(Keys.RETURN)
        print("Pesquisa realizada...")
        driver.implicitly_wait(5)
        first_result_title = driver.find_element("tag name", "h3").text
        print(f"Primeiro resultado: {first_result_title}")
        driver.quit()
        print("Navegador fechado...")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
