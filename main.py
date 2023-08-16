import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from urllib.parse import urlparse
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time

# Configs
delay = 3


# Di rename aja function nya kalau butuh
def main(keyword, coordinates):
    driver = webdriver.Chrome()
    driver.get("https://www.google.com/maps")

    # Temukan search box 
    search_box = driver.find_element(By.ID, "searchboxinput")

    # Masukkan koordinat/titik tengah
    search_box.send_keys(coordinates)
    search_box.send_keys(Keys.RETURN)

    # Tunggu sampai map selesai load
    time.sleep(delay)

    # Masukkan keyword
    search_box.clear()
    search_box.send_keys(keyword)
    search_box.send_keys(Keys.RETURN)

    # Tunggu sampai map selesai load
    time.sleep(delay)

    try:
        for i in range(4):
            jslog_value = f'//div[@class="Nv2PK THOPZb CpccDe "][{i+1}]'
            result_element = driver.find_element(By.XPATH, jslog_value)
            result_href = result_element.get_attribute("href")

            # Buka tautan di tab baru
            actions = ActionChains(driver)
            actions.key_down(Keys.CONTROL).click(result_element).key_up(Keys.CONTROL).perform()

            # Tunggu tab baru selesai load
            time.sleep(delay)

        # Tunggu sebentar untuk memastikan semua tab terbuka
        time.sleep(delay + 3)

    except Exception as e:
        print(e)
        driver.quit()
        return None
    
    # Inisialisasi WebDriverWait
    wait = WebDriverWait(driver, delay)
    for tab_handle in driver.window_handles:
        driver.switch_to.window(tab_handle)

        # Temukan nama tempat (Xpath jslog)
        xpath = "//div[contains(@jslog, '24393;')]"
        element = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        nama_tempat = element.get_attribute("aria-label")

        # Temukan Rating (Xpath span-class)
        rating_element = wait.until(EC.presence_of_element_located((By.XPATH, '//span[@class="ceNzKf"]')))
        label_rating = rating_element.get_attribute("aria-label")

        # Temukan Alamat (Xpath jslog)
        xpath = "//button[contains(@jslog, '36622;')]"
        element = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        alamat = element.get_attribute("aria-label")

        # Temukan nomor telepon (Xpath jslog)
        xpath = "//button[contains(@jslog, '18491;')]"
        element = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        nomor_telepon = element.get_attribute("aria-label")

        # Temukan website (Xpath jslog)
        xpath = "//a[contains(@jslog, '3443;')]"
        element = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        website = element.get_attribute("aria-label")

        # Temukan Jam Operasional (Xpath class)
        jam = driver.find_elements(By.XPATH, '//div/table/tbody/tr/td[@class="mxowUb"]')
        days = ["Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday", "Monday"]
        jam_operasional = []
        for element, day in zip(jam, days):
            label_jam_operasional = element.get_attribute("aria-label")
            jam_operasional.append({day: label_jam_operasional})

        # Temukan titik koordinat
        current_url = driver.current_url
        url_path = urlparse(current_url).path
        path_components = url_path.split("/")
        latitude = ""
        longitude = ""
        for component in path_components:
            if "," in component:
                latitude, longitude, _ = component.split(",")
                break
        
            # Format data dalam bentuk JSON
        data = {
            "Nama Tempat": nama_tempat,
            "Rating": label_rating.replace('Rating: ', ''),
            "Alamat": alamat.replace('Alamat: ', ''),
            "Nomor Telepon": nomor_telepon.replace('Telepon: ', ''),
            "Website": website.replace('Situs Web: ', ''),
            "Jam Operasional": jam_operasional,
            "Koordinat": {
                "Latitude": latitude,
                "Longitude": longitude
            }
        }

        # Konversi menjadi JSON dan tampilkan
        json_output = json.dumps(data, indent=2)
        print(json_output)

    # Tutup WebDriver
    driver.quit()
