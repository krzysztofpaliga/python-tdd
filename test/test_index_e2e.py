import unittest
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

class E2ETests(unittest.TestCase):
    
    def setUp(self):
        service = Service(executable_path='/opt/mozilla/geckodriver')
        self.driver = webdriver.Firefox(service=service)
        try:
            self.driver.get('http://localhost:5000')
        except Exception as err: 
            print(err)
        
        
    def tearDown(self):
        self.driver.quit()
        
    def test_browser_title_contains_app_name(self):
        WebDriverWait(self.driver, 10).until(EC.title_contains('Named Entity'))

        self.assertIn('Named Entity', self.driver.title)
        
    def test_page_heading_is_named_entity_finder(self):
        heading = self._find("heading")
        self.assertEqual('Named Entity Finder', heading.text)
        
    def test_page_has_input_for_text(self):
    
        input_element = self._find("input-text")
        self.assertIsNotNone(input_element)
    
    def test_page_has_button_for_submitting_text(self):
        submit_button = self._find("find-button")
        self.assertIsNotNone(submit_button)
      
    def test_page_has_ner_table(self):
        input_element = self._find('input-text')
        submit_button = self._find('find-button')
        input_element.send_keys('France and Germany share a border in Europe')
        submit_button.click()
        table = self._find('ner-table')
        self.assertIsNotNone(table)

    def _find(self, val):
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, f'[data-test-id="{val}"]'))
        )
        try:
            input_element = self.driver.find_element(By.CSS_SELECTOR, f'[data-test-id="{val}"]')
            return input_element
        except NoSuchElementException:
            raise Exception(f"Element with data-test-id '{val}' not found.")
        
    