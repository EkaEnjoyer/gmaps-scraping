from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
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
        # Temukan result pertama dan klik
        result = driver.find_element(By.CLASS_NAME, "hfpxzc") 
        result_href = result.get_attribute("href")
        # Buka link result
        driver.get(result_href) 
 
        # Tunggu sampai web selesai load
        time.sleep(delay)
 
    except Exception as e:
        print(e)
        driver.quit()
        return None
 

    # Mencari nama
    nama_tempat_element = driver.find_element(By.CSS_SELECTOR, 'h1.DUwDvf.lfPIob')
    nama_tempat = nama_tempat_element.text
 
    # Mencari alamat
    alamat_element = driver.find_element(By.CSS_SELECTOR, 'button[data-item-id="address"]')
    alamat = alamat_element.get_attribute("aria-label")
 
    # Mencari website
    website_element = driver.find_element(By.CSS_SELECTOR, 'a[data-item-id="authority"]')
    website = website_element.get_attribute("aria-label")


    # Mencari semua elemen dengan class CsEnBe
    elements_with_class = driver.find_elements(By.CLASS_NAME, 'CsEnBe')

    # Looping semua elemen
    for element in elements_with_class:
        data_item_id = element.get_attribute("data-item-id")
        # Mencari elemen yang memiliki data-item-id phone:tel:
        if "phone:tel:" in data_item_id:
            no_telp = element.get_attribute("aria-label")

    # Mencari rating
    rating_element = driver.find_element(By.CSS_SELECTOR, 'span.ceNzKf')
    rating = rating_element.get_attribute("aria-label")

    # Mencari jam buka
    jam = driver.find_elements(By.CLASS_NAME, "mxowUb")
    hari = ["Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday", "Monday"]
    jadwal = []
    for element, nama_hari in zip(jam, hari):
        jam_buka = element.get_attribute("aria-label")
        jadwal.append(f"{nama_hari}: {jam_buka}")

    # Hasil akhir
    res = {
        "nama_tempat": nama_tempat,
        "alamat": alamat,
        "website": website,
        "no_telp": no_telp,
        "rating": rating,
        "jadwal": jadwal
    }

    # Tutup browser
    driver.quit()

    return res
