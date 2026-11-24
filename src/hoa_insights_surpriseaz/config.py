from pathlib import Path
import os
from dotenv import load_dotenv
from hoa_insights_surpriseaz.utils import date_parser

load_dotenv()

PROJECT_ROOT: Path = Path(f"{os.environ['PROJECT_ROOT']}")

APP_LOG_NAME = f"{date_parser.logger_date()}.log"
APP_LOG_FILE: Path = PROJECT_ROOT.parent.parent / APP_LOG_NAME

PROD_LOCAL_DB_URI = f"{os.environ['PROD_LOCAL_DB_USER']}:{os.environ['PROD_LOCAL_DB_USER_PASSWORD']}@{os.environ['PROD_LOCAL_DB_HOST']}/{os.environ['PROD_LOCAL_DB_NAME']}"
PROD_REMOTE_DB_URI = f"{os.environ['PROD_REMOTE_DB_USER']}:{os.environ['PROD_REMOTE_DB_USER_PASSWORD']}@{os.environ['PROD_REMOTE_DB_HOST']}/{os.environ['PROD_REMOTE_DB_NAME']}"
PROD_LOCAL_DB_NAME: str = f"{os.environ['PROD_LOCAL_DB_NAME']}"
PROD_LOCAL_DB_USER: str = f"{os.environ['PROD_LOCAL_DB_USER']}"
PROD_LOCAL_DB_HOST = f"{os.environ['PROD_LOCAL_DB_HOST']}"
UPDATE_COMMUNITIES: str = "update_communities"

OWNERS_TABLE: str = "owners"
PARCELS_TABLE: str = "parcels"

CSV_FINANCIAL: Path = PROJECT_ROOT / "output" / "csv" / "financial"
CSV_FINANCIAL.mkdir(parents=True, exist_ok=True)
CSV_UPDATED_PARCELS: Path = PROJECT_ROOT / "output" / "csv" / "parcel_changes"
CSV_UPDATED_PARCELS.mkdir(parents=True, exist_ok=True)

HTML_REPORT_CHANGES: Path = PROJECT_ROOT / "output" / "web_reports" / "parcel_changes"
HTML_REPORT_CHANGES.mkdir(parents=True, exist_ok=True)
HTML_REPORT_FINANCIAL: Path = PROJECT_ROOT / "output" / "web_reports" / "financial"
HTML_REPORT_FINANCIAL.mkdir(parents=True, exist_ok=True)

PDF_REPORT_CHANGES: Path = PROJECT_ROOT / "output" / "pdf" / "parcel_changes"
PDF_REPORT_CHANGES.mkdir(parents=True, exist_ok=True)
PDF_REPORT_FINANCIAL: Path = PROJECT_ROOT / "output" / "pdf" / "financial"
PDF_REPORT_FINANCIAL.mkdir(parents=True, exist_ok=True)
