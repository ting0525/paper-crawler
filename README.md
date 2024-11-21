# Thesis Paper Crawler

## 📖 Project Overview

A Python web scraper designed to retrieve thesis information for specific professors from the Taiwan National Library Thesis System. The tool supports batch searching for multiple professors and saves the results as CSV files.

## ✨ Features

- Headless browser support
- Batch processing for multiple professors
- Automatic saving of search results as CSV
- Utilizes Selenium and undetected-chromedriver

## 🛠 Requirements

- Python 3.7+
- Chrome Browser
- Python packages:
  - selenium
  - undetected-chromedriver
  - pandas

## 📦 Installation

1. Clone the repository
```bash
git clone https://github.com/ting0525/paper-crawler.git
cd paper-crawler
```

2. Create a virtual environment (recommended)
```bash
python -m venv venv
# For Windows
venv\Scripts\activate
# For macOS/Linux
source venv/bin/activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

## 🔧 Configuration

1. Create a `config.json` file
```json
{
    "professors": [
        "Professor Name 1",
        "Professor Name 2"
    ]
}
```

2. Ensure Chrome version matches the `version_main` parameter

## 🚀 Usage

```bash
python main.py
```

Search results will be saved in the `output/` folder

## 📄 `requirements.txt`

```
selenium
undetected-chromedriver
pandas
```

## 🔧 `config.json` Template

```json
{
    "professors": [
        "Professor Name 1",
        "Professor Name 2"
    ]
}
```

## 💻 `main.py` Code Documentation

### ProfessorPaperScraper Class

The `ProfessorPaperScraper` is the core class responsible for web scraping thesis information.

#### Methods

- `__init__(self, url)`: Initializes the scraper with Chrome WebDriver
- `search_professor(self, professor_name)`: Searches for a specific professor's papers
- `get_paper_info(self)`: Extracts paper information from search results
- `save_to_csv(self, papers, professor_name)`: Saves paper information to a CSV file
- `close(self)`: Closes the browser

### Configuration Loading

- `load_config(config_path='config.json')`: Loads professor names from a JSON configuration file

### Main Execution Flow

1. Load configuration
2. Initialize scraper
3. Search for each professor's papers
4. Save results to CSV
5. Close browser

