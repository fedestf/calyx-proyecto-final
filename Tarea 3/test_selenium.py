from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from loggers import logger_debug, logger_error

# La compra debe contener: 5 iPhone, 2 MacBook Pro, 1 MacBook Air y 3 iPods
# clásicos.

compra = {

    'MacBook Pro': 2,
    'MacBook Air': 1,
    'iPhone': 5,
    'iPod Classic': 3,

}


driver = webdriver.Chrome(r'Tarea 1\chromedriver.exe')
driver.get("http://tutorialsninja.com/demo/index.php?route=common/home")
driver.maximize_window()

for key, value in compra.items():

    elem = driver.find_element_by_name("search")
    elem.send_keys(key)
    elem.send_keys(Keys.ENTER)
    elem = driver.find_element_by_link_text(key).click()
    elem = driver.find_element_by_id("input-quantity")
    elem.send_keys(Keys.BACKSPACE)
    elem.send_keys(value)
    elem = driver.find_element_by_id("button-cart").click()
    elem = driver.find_element_by_link_text("Your Store").click()


elem = driver.find_element_by_id("cart").click()
elem = driver.find_element_by_link_text("Checkout").click()

elem = driver.find_elements_by_xpath(
    "/html/body/div[2]/div[2]/div/form/div/table/tbody/tr")

tr = 0
for producto_fuera_stock in elem:
    tr = tr + 1
    if producto_fuera_stock.text.count("*") == 3:
        producto_fuera_stock.find_element_by_xpath(
            f"/html/body/div[2]/div[2]/div/form/div/table/tbody/tr[{tr}]/td[4]/div/span/button[2]").click()

elem = driver.find_element_by_link_text("Your Store").click()
elem = driver.find_element_by_id("cart").click()
elem = driver.find_element_by_link_text("Checkout").click()
# elige que sea como guest
elem = driver.find_element_by_xpath(
    "/html/body/div[2]/div/div/div/div[1]/div[2]/div/div/div[1]/div[2]/label/input").click()
elem = driver.find_element_by_xpath(
    "/html/body/div[2]/div/div/div/div[1]/div[2]/div/div/div[1]/input").click()
# comienza a ingresar datos de facturacion
elem = driver.find_element_by_id("input-payment-firstname")
elem.send_keys("Federico")
elem = driver.find_element_by_id("input-payment-lastname")
elem.send_keys("Lopez")
elem = driver.find_element_by_id("input-payment-email")
elem.send_keys("estemailnoexiste@live.com")
elem = driver.find_element_by_id("input-payment-telephone")
elem.send_keys("0123456789")
elem = driver.find_element_by_id("input-payment-address-1")
elem.send_keys("Calle falsa 123")
elem = driver.find_element_by_id("input-payment-city")
elem.send_keys("Claypole")
elem = driver.find_element_by_id("input-payment-postcode")
elem.send_keys("1849")
elem = driver.find_element_by_id("input-payment-country").click()
elem = driver.find_element_by_xpath(
    "/html/body/div[2]/div/div/div/div[2]/div[2]/div/div[1]/div[2]/fieldset/div[6]/select/option[12]").click()

time.sleep(1)
try:
    elem = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.ID, "input-payment-zone"))
    )
    elem = driver.find_element_by_id("input-payment-zone")
    driver.execute_script("arguments[0].scrollIntoView();", elem)
    elem.click()
    elem = driver.find_element_by_xpath(
        "/html/body/div[2]/div/div/div/div[2]/div[2]/div/div[1]/div[2]/fieldset/div[7]/select/option[3]").click()

except:
    pass


# boton continue de la orden
elem = driver.find_element_by_xpath(
    "/html/body/div[2]/div/div/div/div[2]/div[2]/div/div[3]/div/input").click()

print("")
