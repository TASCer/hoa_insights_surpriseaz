import os
import logging
import platform
import time

from logging import Logger
from pathlib import Path
from selenium import webdriver
from selenium.common.exceptions import ElementNotSelectableException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.firefox.service import Service as FFService
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile as FFProfile
from selenium.webdriver.firefox.options import Options as FFOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from hoa_insights_surpriseaz.utils import rename_files
from hoa_insights_surpriseaz import convert_management_data
from hoa_insights_surpriseaz import my_secrets

PDF_DOWNLOADED_FILENAME: str = "HOA Contact List (PDF).pdf"
PDF_NEW_FILENAME: str = "MANAGEMENT.pdf"
CSV_FILENAME: str = "surpriseaz-hoa-management.csv"

PDF_PATH = Path.cwd() / "output" / "pdf"
CSV_PATH = Path.cwd() / "output" / "csv"

logger: Logger = logging.getLogger(__name__)

URL = my_secrets.hoa_management_pdf_url
XPATH = "/html/body/div[4]/div/div[2]/div[2]/div[3]/div/div/div[1]/div/div[2]/div[1]/div[2]/div/div/div/div/div[2]/div/div/div/div/div/div/div/div/div/div/div/div[2]/div/ul/li/a"

if platform.system() == "Windows":
    FF_DRIVER = Path.cwd() / "utils" / "geckodriver.exe"
    FF_BINARY_PATH = Path(r"P:\Firefox\firefox.exe")  # how to with path?
    FF_DOWNLOAD_DIR = r".\output\pdf"
    
if platform.system() == "Linux":
    FF_DRIVER = Path.cwd() / "utils" / "geckodriver"
    FF_BINARY_PATH = None
    FF_DOWNLOAD_DIR = "./output/pdf"


# TODO find way to terminate firefox-esr on linux. Hangs.
# Try to quit browser or terminate process by bash
def download() -> None:
    """
    Function creates a Selenium browser to download hoa management file.
    """
    logger.info("\tDOWNLOADING MANAGEMENT PDF")
    options = FFOptions()
    ff_profile = FFProfile()
    options.set_preference("browser.download.folderList", 2)
    options.set_preference("browser.download.manager.showWhenStarting", False)
    options.set_preference("browser.download.manager.focusWhenStarting", False)
    options.set_preference("browser.download.dir", os.path.abspath(FF_DOWNLOAD_DIR))
    options.set_preference("browser.helperApps.alwaysAsk.force", False)
    options.set_preference("browser.download.manager.alertOnEXEOpen", False)
    options.set_preference("browser.download.manager.closeWhenDone", True)
    options.set_preference("browser.download.manager.showAlertOnComplete", False)
    options.set_preference("browser.download.manager.useWindow", False)
    options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/pdf")
    options.set_preference("pdfjs.disabled", True)  # HEADLESS AND THIS NEEDED
    options.set_preference("browser.download.alwaysOpenPanel", False)
    options.profile = ff_profile
    options.add_argument("-headless")

    service = FFService(f"{FF_DRIVER}")

    ff_browser = webdriver.Firefox(service=service, options=options)
    ff_browser.get(URL)

    try:
        pdf_link = WebDriverWait(ff_browser, 30).until(
            EC.presence_of_element_located((By.XPATH, XPATH))
        )

        pdf_link.click()
        ff_browser.implicitly_wait(20)
        ff_browser.close()

    except (ElementNotSelectableException, TimeoutException) as err:
        print(err)
        logger.error(err)
        ff_browser.close()

    time.sleep(10)

    logger.info("\tDOWNLOADED MANAGEMENT PDF")

    ff_browser.quit()

    return PDF_PATH / PDF_DOWNLOADED_FILENAME, PDF_PATH / PDF_NEW_FILENAME

if __name__ == "__main__":
    download()