import os
import logging
import time

from logging import Logger
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
from hoa_insights_surpriseaz import parse_management_data
from hoa_insights_surpriseaz import my_secrets

logger: Logger = logging.getLogger(__name__)

URL = my_secrets.hoa_management_pdf_url
XPATH = "/html/body/div[4]/div/div[2]/div[2]/div[3]/div/div/div[1]/div/div[2]/div[1]/div[2]/div/div/div/div/div[2]/div/div/div/div/div/div/div/div/div/div/div/div[2]/div/ul/li/a"


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
    options.set_preference("browser.download.dir", os.path.abspath("./output/pdf"))
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

    service = FFService(f"{my_secrets.firefox_driver}")

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


if __name__ == "__main__":
    # download()
    file_renamed: bool = rename_files.rename()
    if file_renamed:
        parse_management_data.convert_pdf()
