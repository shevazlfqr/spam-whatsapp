from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import logging

# Konfigurasi logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def initiate_driver():
    try:
        # Inisialisasi driver Chrome
        driver = webdriver.Chrome()
        logging.info("Driver Chrome berhasil diinisialisasi.")
        return driver
    except Exception as e:
        logging.error(f"Gagal menginisialisasi driver Chrome: {e}")

def scan_whatsapp(driver):
    try:
        # Membuka WhatsApp Web
        driver.get("https://web.whatsapp.com")
        logging.info("WhatsApp Web berhasil dibuka.")
        # Menunggu pengguna untuk memindai kode QR
        print("Silakan pindai kode QR di WhatsApp Web.")
        time.sleep(50)  # Sesuaikan waktu tunggu sesuai kebutuhan
    except Exception as e:
        logging.error(f"Gagal membuka WhatsApp Web: {e}")

def find_contact_and_send_messages(driver, contact_name, message, count):
    try:
        # Mencari kontak
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]'))
        )
        search_box.click()
        search_box.send_keys(contact_name)
        logging.info(f"Mencari kontak: {contact_name}")
        time.sleep(10)  # Menunggu kontak muncul

        # Memilih kontak
        contact = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f'//span[@title="{contact_name}"]'))
        )
        contact.click()
        logging.info(f"Kontak {contact_name} berhasil dipilih.")

        # Mengirim pesan
        message_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true" and @data-tab="10"]'))
        )
        for _ in range(count):
            message_box.send_keys(message)
            send_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//span[@data-icon="send"]'))
            )
            send_button.click()
            logging.info(f"Mengirim pesan ke {contact_name}: {message}")
    except Exception as e:
        logging.error(f"Gagal mengirim pesan: {e}")

def main():
    driver = initiate_driver()
    if driver:
        scan_whatsapp(driver)
        
        contact_name = "contact_name"  # Ganti dengan nama kontak yang sebenarnya
        message = "input message"  # Ganti dengan pesan yang sebenarnya
        count = 10  # Ganti dengan jumlah pesan yang akan dikirim

        find_contact_and_send_messages(driver, contact_name, message, count)

        driver.quit()
        logging.info("Driver Chrome berhasil ditutup.")
    else:
        logging.error("Driver Chrome tidak tersedia.")

if __name__ == "__main__":
    main()
