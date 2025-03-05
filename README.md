# ![TASCS LOGO](images/logo.png)


## HOA_INSIGHTS_SURPRISEAZ



Provides information on Surprise, AZ Home Owners Association (HOA) communities by accessing and aggragating various public data sources for insights and analysis.

### See It

[Community Rentals Map](https://hoa.tascs.net/areaMap.php)

[Relevant HOA Legislation](https://hoa.tascs.net/relevant_bills.php)

[Community Sales](https://hoa.tascs.net)


### Provides insights on:
- Community Management
  - Management Company
  - Management Contact Information
- Community Rentals
  - % Rentals
  - Rental Property Contact Information
  - Rental Property Owner Information
  - Rental Property Location
- Community Sales
  - Community Average Sale Price
  - Community Count of Sales

- Legislation information on relevant HOA bills

---

Assessor API Documentation: https://mcassessor.maricopa.gov/file/home/MC-Assessor-API-Documentation.pdf

Legiscan API Information: https://legiscan.com/legiscan

---
POSSIBLE OTHER DATA SOURCES

  - County Recorder's Office
  - City Crime Stats
  - Zillow

---

PDF financial report functionality will need the [pdfkit Python module](https://pypi.org/project/pdfkit/) and [wkhtmltopdf](https://wkhtmltopdf.org/)

---

#### utils folder contains

- Linux shell script for cron job scheduling
- Windows batch file for Scheduled Tasks scheduling
- A template of my 'my_secrets.py' secrets file

#### src/utils folder contains

- LINUX gecko driver (geckodriver) for monthly management pdf download via Firefox
- WINDOWS gecko driver (geckodriver) for monthly management pdf download via Firefox
- various parsers/formaters
- file deletes/renames

---

#### PRE INITIAL_LAUNCH TODO's

- [ ] TASC 1 - Execute command: "uv run db-init.py" from database/setup directory 
- [ ] TASC 2 - Verify database initialized via __database-setup.log
- [ ] TASC 3 - Change directory to src/hoa_insights_surpriseaz/ and execute command "uv run main.py"