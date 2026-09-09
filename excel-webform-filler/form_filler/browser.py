from __future__ import annotations

import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from form_filler.config import BrowserConfig
from form_filler.excel_leads import LeadRow


def start_driver(browser: BrowserConfig) -> WebDriver:
    options = Options()
    if browser.maximized:
        options.add_argument("--start-maximized")
    return webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options,
    )


def _scroll_into_view(driver: WebDriver, element) -> None:
    driver.execute_script(
        "arguments[0].scrollIntoView({block: 'nearest', inline: 'nearest'});",
        element,
    )
    time.sleep(0.3)


def submit_quote_form(driver: WebDriver, url: str, lead: LeadRow, wait_seconds: int, pause_after_submit: float) -> None:
    wait = WebDriverWait(driver, wait_seconds)
    driver.get(url)

    select_el = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "select[name='version']")))
    _scroll_into_view(driver, select_el)
    Select(select_el).select_by_visible_text(lead.version)

    name_el = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[placeholder='Full name']")))
    _scroll_into_view(driver, name_el)
    name_el.clear()
    name_el.send_keys(lead.name)

    phone_el = driver.find_element(By.CSS_SELECTOR, "input[placeholder='Phone']")
    _scroll_into_view(driver, phone_el)
    phone_el.clear()
    phone_el.send_keys(lead.phone)

    email_el = driver.find_element(By.CSS_SELECTOR, "input[placeholder='Email']")
    _scroll_into_view(driver, email_el)
    email_el.clear()
    email_el.send_keys(lead.email)

    notes_el = driver.find_element(By.CSS_SELECTOR, "textarea[placeholder='Questions or notes']")
    _scroll_into_view(driver, notes_el)
    notes_el.clear()
    notes_el.send_keys(lead.notes)

    radios = driver.find_elements(By.CSS_SELECTOR, "input[name='contact_pref'][value='whatsapp']")
    if radios:
        radio = radios[0]
        _scroll_into_view(driver, radio)
        if not radio.is_selected():
            radio.click()
    else:
        print("  warning: preferred-contact option was not found; continuing")

    checkbox = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='checkbox'][name='privacy']")))
    _scroll_into_view(driver, checkbox)
    if not checkbox.is_selected():
        driver.execute_script("arguments[0].click();", checkbox)

    button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[type='submit']")))
    _scroll_into_view(driver, button)
    driver.execute_script("arguments[0].click();", button)
    time.sleep(pause_after_submit)
