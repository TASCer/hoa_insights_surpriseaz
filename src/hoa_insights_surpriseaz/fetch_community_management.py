import os
import logging
import time

from dotenv import load_dotenv
from logging import Logger
from pathlib import Path

from selenium import webdriver
from selenium.common.exceptions import ElementNotSelectableException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException

from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.firefox import GeckoDriverManager

load_dotenv()

# TODO SPACE TYPO FROM CITY 08-25 and extra "," after contact 2nd page
PDF_DOWNLOADED_FILENAME: str = "HOA Contact List (PDF) .pdf"
PDF_NEW_FILENAME: str = "MANAGEMENT.pdf"
PDF_PATH: Path = Path.cwd() / "output" / "pdf"

CSV_PATH: Path = (
    Path.cwd().parent / "hoa_insights_surpriseaz" / "database" / "setup" / "seed_data"
)
CSV_FILENAME: str = "surpriseaz-hoa-management.csv"

logger: Logger = logging.getLogger(__name__)

URL: str = os.environ["HOA_MANAGEMENT_URL"]
XPATH = "/html/body/div[4]/div/div[2]/div[2]/div[3]/div/div/div[1]/div/div[2]/div[1]/div[2]/div/div/div/div/div[2]/div/div/div/div/div/div/div/div/div/div/div/div[2]/div/ul/li/a"

DOWNLOAD_TO: Path = Path.cwd() / "output" / "pdf"


def download() -> tuple[Path, Path, Path]:
    """
    Function creates a Selenium browser/driver to download HOA management file from city website.

    :return: downloaded file, new file, csv file
    """
    logger.info("\tSTARTED: MANAGEMENT PDF DOWNLOAD")

    try:
        options = webdriver.FirefoxOptions()
        options.add_argument("-headless")
        options.set_preference("browser.download.folderList", 2)
        options.set_preference("browser.download.manager.showWhenStarting", False)
        options.set_preference("browser.download.manager.focusWhenStarting", False)
        options.set_preference("browser.download.dir", os.path.abspath(DOWNLOAD_TO))
        options.set_preference("browser.helperApps.alwaysAsk.force", False)
        options.set_preference("browser.download.manager.alertOnEXEOpen", False)
        options.set_preference("browser.download.manager.closeWhenDone", True)
        options.set_preference("browser.download.manager.showAlertOnComplete", False)
        options.set_preference("browser.download.manager.useWindow", False)
        options.set_preference(
            "browser.helperApps.neverAsk.saveToDisk", "application/pdf"
        )
        options.set_preference("pdfjs.disabled", True)  # HEADLESS AND THIS NEEDED
        options.set_preference("browser.download.alwaysOpenPanel", False)

        firefox_browser = webdriver.Firefox(
            options=options, service=FirefoxService(GeckoDriverManager().install())
        )

        logger.info(f"\tFIREFOX browser service created w/options: {options.arguments}")

    except FileNotFoundError as file_err:
        logger.exception(file_err)
        exit()

    except WebDriverException as driver_err:
        logger.critical(f"{str(driver_err)}")
        exit()

    firefox_browser.get(URL)

    try:
        pdf_link = WebDriverWait(firefox_browser, 30).until(
            EC.presence_of_element_located((By.XPATH, XPATH))
        )

        pdf_link.click()
        firefox_browser.implicitly_wait(20)
        firefox_browser.close()

    except (ElementNotSelectableException, TimeoutException) as err:
        print(err)
        logger.error(err)
        firefox_browser.close()

    time.sleep(10)

    logger.info("\tCOMPLETED: MANAGEMENT PDF DOWNLOAD")

    firefox_browser.quit()

    return (
        PDF_PATH / PDF_DOWNLOADED_FILENAME,
        PDF_PATH / PDF_NEW_FILENAME,
        CSV_PATH / CSV_FILENAME,
    )


if __name__ == "__main__":
    print(download())
