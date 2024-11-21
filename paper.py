import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import pandas as pd
from datetime import datetime
import json
import os

class ProfessorPaperScraper:
    def __init__(self, url):
        self.url = url
        options = uc.ChromeOptions()
        
        # Headless mode settings
        options.add_argument('--headless')  # Headless mode
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')  # Helpful for headless mode
        options.add_argument('--window-size=1920,1080')  # Set browser window size
        
        # Use version 130
        self.driver = uc.Chrome(
            options=options,
            version_main=130  # Update to your Chrome version
        )
        self.wait = WebDriverWait(self.driver, 10)
    
    def search_professor(self, professor_name):
        """Search for a specific professor's papers"""
        try:
            print(f"Start search：{professor_name}")
            self.driver.get(self.url)
            
            # Enter professor name
            search_input = self.wait.until(
                EC.presence_of_element_located((By.ID, "ysearchinput0"))
            )
            search_input.clear()
            search_input.send_keys(professor_name)
            
            # Select advisor option
            checkbox = self.wait.until(
                EC.presence_of_element_located((By.ID, "ad_指導教授"))
            )
            if not checkbox.is_selected():
                checkbox.click()
            
            # Click search button
            search_button = self.wait.until(
                EC.presence_of_element_located((By.ID, "gs32search"))
            )
            search_button.click()
            
            # Wait for results to load and get paper information
            papers = self.get_paper_info()
            return papers
            
        except TimeoutException:
            print(f"loading timeout：{professor_name}")
            return []
        except Exception as e:
            print(f"searching {professor_name} error: {str(e)}")
            return []
    
    def get_paper_info(self):
        """Get paper information"""
        papers = []
        try:
            # Wait for paper title elements to appear
            paper_elements = self.wait.until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "etd_d"))
            )
            
            # Collect information for each paper
            for paper in paper_elements:
                paper_info = {
                    'title': paper.text,
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                papers.append(paper_info)
                
        except Exception as e:
            print(f"An error occurred while retrieving paper information: {str(e)}")
            
        return papers
    
    def save_to_csv(self, papers, professor_name):
        """Save paper information to CSV"""
        try:
            # Create output directory (if it doesn't exist)
            os.makedirs('output', exist_ok=True)
            
            filename = os.path.join('output', f"{professor_name}_papers_{datetime.now().strftime('%Y%m%d')}.csv")
            df = pd.DataFrame(papers)
            df.to_csv(filename, index=False, encoding='utf-8-sig')
            print(f"{professor_name}'s paper information has been saved to {filename}")
        except Exception as e:
            print(f"An error occurred while saving the file for {professor_name} : {str(e)}")
    
    def close(self):
        """Close browser"""
        self.driver.quit()

def load_config(config_path='config.json'):
    """Load configuration"""
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Configuration file not found {config_path}")
        return None
    except json.JSONDecodeError:
        print(f"Configuration file format error {config_path}")
        return None

def main():
    # Taiwan thesis website URL
    url = "https://etds.ncl.edu.tw/cgi-bin/gs32/gsweb.cgi/login?o=dwebmge"
    
    # Load configuration file
    config = load_config()
    if not config or 'professors' not in config:
        print("Configuration file error or no professor specified")
        return
    
    try:
        scraper = ProfessorPaperScraper(url)
        
        # Process each professor sequentially
        for professor_name in config['professors']:
            print(f"\nStart dealing with professor：{professor_name}")
            papers = scraper.search_professor(professor_name)
            
            if papers:
                scraper.save_to_csv(papers, professor_name)
            else:
                print(f"No papers found for {professor_name}")
        
        scraper.close()
        print("\nfinish")
        
    except Exception as e:
        print(f"execute error: {str(e)}")

if __name__ == "__main__":
    main()