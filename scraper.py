#!/usr/bin/env python3
"""UN Blue Book Scraper - Extracts representative data for all 193 Member States."""

import csv
import json
import time
from playwright.sync_api import sync_playwright

BASE_URL = "https://bluebook.e-delegate.un.org/"


def scrape_un_bluebook():
    """Scrape representative data for all 193 Member States via console capture."""
    all_representatives = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_context().new_page()

        console_logs = []

        def handle_console(msg):
            for arg in msg.args:
                try:
                    val = arg.json_value()
                    console_logs.append(val)
                except:
                    pass

        page.on("console", handle_console)

        # Load page
        print("Loading UN Blue Book...")
        page.goto(BASE_URL)
        page.wait_for_selector("app-root", timeout=30000)
        time.sleep(3)

        # Step 1: Select "Member States maintaining permanent missions" category
        print("Selecting Member States category...")
        page.locator('[role="combobox"]').first.click()
        time.sleep(1)
        for opt in page.locator('[role="option"]').all():
            if "Member States maintaining" in opt.inner_text():
                opt.click()
                break
        time.sleep(2)

        # Step 2: Get list of all countries
        page.locator('[role="combobox"]').last.click()
        time.sleep(1)
        options = page.locator('[role="option"]').all()
        countries = [opt.inner_text().strip() for opt in options]
        print(f"Found {len(countries)} countries")
        page.keyboard.press("Escape")
        time.sleep(0.5)

        # Step 3: Iterate through each country
        for i, country in enumerate(countries):
            print(f"[{i+1}/{len(countries)}] {country}", end="", flush=True)

            console_logs.clear()

            # Select country
            page.locator('[role="combobox"]').last.click()
            time.sleep(0.3)
            page.locator(f'[role="option"]:has-text("{country}")').first.click()
            time.sleep(1.5)

            # Extract representative data from console logs
            reps_found = 0
            for log in console_logs:
                if not isinstance(log, list):
                    continue
                if not log or not isinstance(log[0], dict):
                    continue
                if not any(k.startswith('BB_') for k in log[0].keys()):
                    continue
                for rep in log:
                    rep['_country'] = country
                    all_representatives.append(rep)
                reps_found = len(log)
                break

            print(f" -> {reps_found} representatives")

        browser.close()

    return all_representatives


def write_csv(data, filename="un_bluebook_representatives.csv"):
    """Write representative data to CSV."""
    if not data:
        print("No data to write")
        return

    # Get all unique keys
    all_keys = set()
    for record in data:
        all_keys.update(record.keys())

    # Sort keys: _country first, then BB_ fields, then others
    bb_keys = sorted([k for k in all_keys if k.startswith("BB_")])
    other_keys = sorted([k for k in all_keys if not k.startswith("BB_") and k != '_country'])
    fieldnames = ['_country'] + bb_keys + other_keys

    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(data)

    print(f"\nWrote {len(data)} records to {filename}")


if __name__ == "__main__":
    print("UN Blue Book Scraper")
    print("=" * 50)

    representatives = scrape_un_bluebook()
    write_csv(representatives)
