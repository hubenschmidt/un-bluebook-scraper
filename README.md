# UN Blue Book Scraper

Scrapes representative data for all 193 UN Member States from the [UN Blue Book](https://bluebook.e-delegate.un.org/).

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install playwright
playwright install chromium
```

## Usage

```bash
source venv/bin/activate
python scraper.py
```

Outputs `un_bluebook_representatives.csv` with ~2,700 representatives.

## Output Fields

| Field | Description |
|-------|-------------|
| _country | Country name |
| BB_FirstName | First name |
| BB_LastName | Last name |
| BB_Title | Title (H.E. Mr., Ms., etc.) |
| BB_Dipl_Rank | Diplomatic rank |
| BB_Function | Role (Permanent Representative, etc.) |
| BB_Appointment | Appointment date |
| BB_Cred_Presented | Credentials presented date |
| BB_Email | Email address |
| BB_PhnNumber | Phone number |
| BB_Status | Active/Inactive |
