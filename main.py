import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from urllib.parse import urlparse
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
import time

# Driver
driver = webdriver.Chrome()
driver.get("https://www.google.com/maps")

# Configs
delay = 7
language = "Bahasa Indonesia"

# Result
result = {"Results": []}

def scrape_data():
    wait = WebDriverWait(driver, delay)
    data = {}

    try:
        xpath = "//div[contains(@jslog, '24393;')]"
        element = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        nama_tempat = element.get_attribute("aria-label")
    except NoSuchElementException:
        nama_tempat = "information not found"
    except Exception as e:
        print("Error while locating 'Nama Tempat' element:", e)
        nama_tempat = "error occurred"

    try:
        rating_element = wait.until(EC.presence_of_element_located((By.XPATH, '//span[@class="ceNzKf"]')))
        label_rating = rating_element.get_attribute("aria-label")
    except NoSuchElementException:
        label_rating = "information not found"
    except Exception as e:
        print("Error while locating 'Rating' element:", e)
        label_rating = "error occurred"

    try:
        xpath = "//button[contains(@jslog, '36622;')]"
        element = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        alamat = element.get_attribute("aria-label")
    except NoSuchElementException:
        alamat = "information not found"
    except Exception as e:
        print("Error while locating 'Alamat' element:", e)
        alamat = "error occurred"

    try:
        xpath = "//button[contains(@jslog, '18491;')]"
        element = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        nomor_telepon = element.get_attribute("aria-label")
    except NoSuchElementException:
        nomor_telepon = "information not found"
    except Exception as e:
        print("Error while locating 'Nomor Telepon' element:", e)
        nomor_telepon = "error occurred"

    try:
        xpath = "//a[contains(@jslog, '3443;')]"
        element = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
        website = element.get_attribute("aria-label")
    except NoSuchElementException:
        website = "information not found"
    except Exception as e:
        print("Error while locating 'Website' element:", e)
        website = "error occurred"

    jam_operasional = []
    try:
        jam = driver.find_elements(By.XPATH, '//div/table/tbody/tr/td[@class="mxowUb"]')
        days = ["Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday", "Monday"]
        for element, day in zip(jam, days):
            label_jam_operasional = element.get_attribute("aria-label")
            jam_operasional.append({day: label_jam_operasional})
    except NoSuchElementException:
        jam_operasional = []
    except Exception as e:
        print("Error while locating 'Jam Operasional' element:", e)
        jam_operasional = "error occurred"

    try:
        current_url = driver.current_url
        url_path = urlparse(current_url).path
        path_components = url_path.split("/")
        latitude = ""
        longitude = ""
        for component in path_components:
            if "," in component:
                latitude, longitude, _ = component.split(",")
                break
    except:
        latitude = "information not found"
        longitude = "information not found"

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

    return data

# Di rename aja function nya kalau butuh
def main(keyword, coordinates):

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
        # Temukan result
        results_div = driver.find_element(By.CSS_SELECTOR, f'div[aria-label="Hasil untuk {keyword}"]')
        # Temukan semua anchor tag di dalam result
        anchor_tags = results_div.find_elements(By.XPATH, './/a')

        # Filter semua anchor tag hanya yang memiliki google.com/maps
        filtered_google_maps_links = []
        for anchor_tag in anchor_tags:
            href = anchor_tag.get_attribute("href")
            if href and "google.com/maps" in href:
                filtered_google_maps_links.append(anchor_tag)

        # Buka semua anchor tag yang ditemukan
        for anchor_tag in filtered_google_maps_links:
            # Buka di tab baru
            actions = ActionChains(driver)
            actions.key_down(Keys.CONTROL).click(anchor_tag).key_up(Keys.CONTROL).perform()
            time.sleep(1)

        for links in anchor_tags:
            driver.switch_to.window(driver.window_handles[-1])
            # Push scrape_data to result
            result["Results"].append(scrape_data())
            print(result)
            time.sleep(delay)
            driver.close()

    except Exception as e:
        print(e)
        driver.quit()
        return None

    # Konversi menjadi JSON dan tampilkan
    json_output = json.dumps(result, indent=2)

    # Tutup WebDriver
    driver.quit()

keyword = "Police"
location = "37.7749, -122.4194"
main(keyword, location)
