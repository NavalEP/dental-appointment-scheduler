import asyncio
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError, Error as PlaywrightError
import logging
from datetime import datetime, timedelta
import os
import re

class SchedulingService:
    def __init__(self):
        self.url = 'https://onlinebooking.mydentistlink.com/f0398585-a097-4b03-9313-83f79da43804/dafb6490-5320-4145-bf16-8176a195e379'
        self.playwright = None
        self.browser = None
        self.page = None
        self.cache = {}
        self.setup_logging()

    def setup_logging(self):
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)

    async def initialize_browser(self, headless=False):
        self.logger.debug("Initializing browser")
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=headless)
        self.page = await self.browser.new_page()
        self.logger.info("Browser initialized")

    async def close_browser(self):
        self.logger.debug("Closing browser")
        if self.page:
            await self.page.close()
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
        self.logger.info("Browser closed")

    async def navigate_to_scheduling_page(self):
        self.logger.debug(f"Navigating to {self.url}")
        try:
            response = await self.page.goto(self.url, wait_until="networkidle", timeout=60000)
            if response.status != 200:
                self.logger.error(f"Navigation failed with status code: {response.status}")
                await self.take_screenshot("navigation_error")
                raise Exception(f"Navigation failed with status code: {response.status}")
            self.logger.info(f"Successfully navigated to scheduling page: {self.url}")
        except TimeoutError:
            self.logger.error("Navigation timed out")
            await self.take_screenshot("navigation_timeout")
            raise
        except Exception as e:
            self.logger.error(f"Error navigating to the scheduling page: {e}")
            await self.take_screenshot("navigation_error")
            raise

    async def select_patient_type(self, patient_type):
        self.logger.debug(f"Selecting patient type: {patient_type}")
        try:
            patient_map = {
                "New Patient": "text='New Patient'",
                "Returning Patient": "text='Returning Patient'"
            }
            selector = patient_map.get(patient_type)

            if not selector:
                raise ValueError(f"Invalid patient type provided: {patient_type}")

            await self.page.wait_for_selector(selector, state="visible", timeout=20000)
            await self.page.click(selector)
            self.logger.info(f"Selected patient type: {patient_type}")
            
            continue_button = "text='Continue'"
            await self.page.wait_for_selector(continue_button, state="visible", timeout=10000)
            await self.page.click(continue_button)
            self.logger.info("Clicked on Continue button after selecting patient type")
            await self.page.wait_for_load_state("networkidle", timeout=20000)
        except TimeoutError:
            self.logger.error(f"Timeout while selecting patient type {patient_type}")
            await self.take_screenshot(f"patient_type_timeout_{patient_type}")
            raise
        except Exception as e:
            self.logger.error(f"Error selecting patient type {patient_type}: {e}")
            await self.take_screenshot(f"patient_type_error_{patient_type}")
            raise

    async def select_appointment_type_direct_click(self, appointment_type):
        self.logger.debug(f"Selecting appointment type: {appointment_type}")
        try:
            appointment_map = {
                "New appointment": "New Patient Exam - 60 min",
                "Emergency appointment": "Emergency Exam - 30 min",
                "Invisalign consultation": "In-office Invisalign Consultation - 60 min"
            }
            appointment_text = appointment_map.get(appointment_type)
            if not appointment_text:
                raise ValueError(f"Invalid appointment type provided: {appointment_type}")

            await self.page.wait_for_selector("text='Select a Reason'", state="visible", timeout=10000)
            await self.page.click("text='Select a Reason'")
            
            option_selector = f"text='{appointment_text}'"
            await self.page.wait_for_selector(option_selector, state="visible", timeout=10000)
            await self.page.click(option_selector)
            
            self.logger.info(f"Selected appointment type: {appointment_type}")
            await self.page.wait_for_load_state("networkidle", timeout=10000)
        except TimeoutError:
            self.logger.error(f"Timeout while selecting appointment type {appointment_type}")
            await self.take_screenshot(f"appointment_type_timeout_{appointment_type}")
            raise
        except Exception as e:
            self.logger.error(f"Error selecting appointment type {appointment_type}: {e}")
            await self.take_screenshot(f"appointment_type_error_{appointment_type}")
            raise

    async def set_date_preference(self, specific_date):
        self.logger.debug(f"Getting available slots for date: {specific_date}")
        try:
            target_date = datetime.strptime(specific_date, "%Y-%m-%d")
            
            await self.page.wait_for_selector(f"span.ib-booking-dateNum:has-text('{target_date.day}')", state="visible", timeout=10000)
            slots = await self.page.locator("div.ib-booking-active + div.ib-booking-times").locator("span.ib-booking-active").all()
            
            available_slots = []
            for slot in slots:
                time = await slot.inner_text()
                datetime_attr = await slot.get_attribute('time') 
                available_slots.append({
                    'date': specific_date,
                    'time': time,
                    'datetime': datetime_attr 
                })
            
            self.logger.info(f"Available slots for {specific_date}: {available_slots}")
            return available_slots
        except TimeoutError:
            self.logger.error("Timeout while getting available slots")
            await self.take_screenshot("slots_timeout")
            return []
        except Exception as e:
            self.logger.error(f"Error retrieving available slots: {e}")
            await self.take_screenshot("slots_error")
            return []

    async def get_available_slots(self):
        self.logger.debug("Getting available slots")
        try:
            await self.page.wait_for_selector(".ib-booking-column", state="visible", timeout=10000)

            date_columns = await self.page.query_selector_all(".ib-booking-column")
            available_slots = []

            for column in date_columns:
                day_element = await column.query_selector(".ib-booking-day")
                date_num_element = await column.query_selector(".ib-booking-dateNum")
                day = await day_element.inner_text() if day_element else None
                date_num = await date_num_element.inner_text() if date_num_element else None
                
                # Construct full date for output
                full_date = f"2024-09-{date_num.zfill(2)}"  # Ensure day is two digits

                time_elements = await column.query_selector_all(".ib-booking-time span[time]")

                for time_element in time_elements:
                    time_text = await time_element.inner_text() 
                    time_attr = await time_element.get_attribute("time")

                    if time_text and time_attr:
                        available_slots.append({
                            'date': full_date,
                            'time': time_text,
                            'datetime': time_attr
                        })
                    else:
                        available_slots.append({
                            'date': full_date,
                            'time': '\xa0',  # or whatever placeholder you prefer
                            'datetime': None
                        })
                    self.logger.debug(f"Available slot found: {full_date}, {time_text} ({time_attr})")

            self.logger.info(f"Available slots: {available_slots}")
            return available_slots

        except PlaywrightTimeoutError:
            self.logger.error("Timeout while getting available slots")
            await self.take_screenshot("slots_timeout")
            return []

        except Exception as e:
            self.logger.error(f"Error retrieving available slots: {e}")
            await self.take_screenshot("slots_error")
            return []



    async def take_screenshot(self, name):
        os.makedirs("screenshots", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screenshots/{name}_{timestamp}.png"
        try:
            await self.page.screenshot(path=filename)
            self.logger.info(f"Screenshot saved: {filename}")
        except PlaywrightError:
            self.logger.warning("Unable to take screenshot: Page might be closed")

    async def check_appointment_slots(self, patient_type, appointment_type, date_preference=None):
        cache_key = f"{patient_type}_{appointment_type}_{date_preference}"
        if cache_key in self.cache:
            self.logger.info(f"Using cached data for {appointment_type} on {date_preference}")
            return self.cache[cache_key]

        max_retries = 3
        for attempt in range(max_retries):
            try:
                await self.initialize_browser(headless=False)  # Set to True for production
                await self.navigate_to_scheduling_page()
                await self.select_patient_type(patient_type)
                await self.select_appointment_type_direct_click(appointment_type)
                if date_preference:
                   available_slots = await self.set_date_preference(date_preference)
                   return available_slots
                slots = await self.get_available_slots()

                self.cache[cache_key] = slots
                return slots
            except Exception as e:
                self.logger.error(f"Error checking appointment slots (attempt {attempt + 1}/{max_retries}): {e}")
                if attempt == max_retries - 1:
                    return []
                await asyncio.sleep(2 ** attempt)  
            finally:
                await self.close_browser()

async def main():
    service = SchedulingService()

    patient_type = "New Patient"
    appointment_type = "New appointment"
    date_preference = "2024-09-25"  

    try:
        available_slots = await service.check_appointment_slots(patient_type, appointment_type, date_preference)
        print("Available slots:")
        print("[")
        for slot in available_slots:
            if slot['datetime'] is not None:
                print(f"  {{'date': '{slot['date']}', 'time': '{slot['time']}', 'datetime': '{slot['datetime']}'}} ,")
        print("]")
    except Exception as e:
        print(f"An error occurred: {e}")
if __name__ == "__main__":
    asyncio.run(main())
