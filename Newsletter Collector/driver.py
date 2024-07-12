import requests
import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import GPT_summary
import pandas as pd
import news_api as news_api
import time

def generate_ESG_articles():
    # Set up the Selenium WebDriver
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(service=service, options=options)

    # URL of the ASX 100 List on Market Index
    url = 'https://www.marketindex.com.au/asx100'

    # Load the page
    driver.get(url)

    # Use explicit wait to wait until the span is clickable
    wait = WebDriverWait(driver, 5)
    mkt_cap_span = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Mkt Cap']")))

    # Scroll to the element before clicking
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", mkt_cap_span)
    time.sleep(1)  # Give some time to scroll

    # Use JavaScript to click the element
    driver.execute_script("arguments[0].click();", mkt_cap_span)

    # Wait for the table to update (give it some time to ensure the page updates)
    time.sleep(1)

    mkt_cap_span = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Mkt Cap']")))

    # Scroll to the element before clicking
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", mkt_cap_span)
    time.sleep(1)  # Give some time to scroll

    # Use JavaScript to click the element
    driver.execute_script("arguments[0].click();", mkt_cap_span)
    # Wait for the table to update (give it some time to ensure the page updates)
    time.sleep(1)

    # Wait for the table to be present
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'mi-table')))

    # Find the correct table containing the list of ASX 100 companies
    tables = driver.find_elements(By.CLASS_NAME, 'mi-table')

    # List to store company names and tickers
    companies = []
    tickers = []

    # Check if any tables were found
    if not tables:
        print("No tables found on the page.")
    else:
        # Iterate over the tables to find the one with the correct headers
        for table in tables:
            headers = [th.text.strip() for th in table.find_elements(By.TAG_NAME, 'th')]
            if 'Code' in headers and 'Company' in headers:
                # Extract rows
                rows = table.find_elements(By.TAG_NAME, 'tr')
                # Iterate over the rows to extract company names and tickers
                for row in rows:
                    if row.get_attribute('data-quoteapi-id'):  # Check if the row has a ticker attribute
                        ticker = row.get_attribute('data-quoteapi-id').split('.')[0].upper()  # Extract and format ticker
                        cols = row.find_elements(By.TAG_NAME, 'td')
                        if len(cols) >= 3:  # Ensure the row has enough columns
                            try:
                                company = cols[2].text.strip()  # 'Company' name is in the 3rd column
                                if '\n' in company:
                                    company = company.split('\n')[0]  # Only keep the company name

                                tickers.append(ticker)
                                companies.append(company)
                            except Exception as e:
                                print(f"Error in row: {e}")

    # Clean up the Selenium WebDriver
    driver.quit()

    # Function to get ESG score for a company from Yahoo Finance
    def get_esg_score(ticker):
        url = f'https://finance.yahoo.com/quote/{ticker}.ax/sustainability'
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            try:
                # Find the h4 tag with class 'border svelte-y3c2sq'
                esg_score_tag = soup.find('h4', class_='border svelte-y3c2sq')
                if esg_score_tag:
                    esg_score = esg_score_tag.text.strip()
                    return esg_score
            except Exception as e:
                print(f"Error parsing ESG score for {ticker}: {e}")
        return 'Not found'

    # Dictionary to store ESG scores
    esg_scores = {}

    # Fetch ESG score for each ticker
    for ticker in tickers:
        esg_score = get_esg_score(ticker)
        if esg_score:
            esg_scores[ticker] = esg_score
        else:
            esg_scores[ticker] = 'Not found'
        time.sleep(1)  # Sleep to avoid overwhelming the server

    # Combine companies, tickers, and ESG scores into a DataFrame
    companies_df = pd.DataFrame({
        'Company': companies,
        'Ticker': tickers,
        'ESG Score': [esg_scores.get(ticker, 'Not found') for ticker in tickers]
    })

    # Convert ESG Score column to numeric, forcing errors to NaN
    companies_df['ESG Score'] = pd.to_numeric(companies_df['ESG Score'], errors='coerce')

    # Sort the DataFrame by ESG Score in ascending order (lowest scores first)
    sorted_companies_df = companies_df.sort_values(by='ESG Score', ascending=False)

    # Print the sorted DataFrame

    # Convert DataFrame to CSV
    # sorted_companies_df.to_csv('output.csv', index=False)
    

    list_of_articles = []
    for index, row in sorted_companies_df.iterrows():
        print(f"Index: {index}, Company: {row['Company']}, Ticker: {row['Ticker']}, ESG Score: {row['ESG Score']}")
        if isinstance(row['ESG Score'], (int, float)):
            article =  news_api.esg_company_articles(row['Company'],row['Ticker'])
            article["ESG"] = row['ESG Score']

            list_of_articles.append(article)
    

    data = []
    counter = 1
    
    for article in list_of_articles:
        URL = article["link"]
        summary = GPT_summary.generate_summary_ONE_article(URL)
        result  = {"id": counter,'title': article["title"],"author": article["author"],"ESG": article["ESG"],"body": summary,"link": URL }
        data.append(result)
        counter +=1
    
    

    return data


def generate_general_news():
    articles = news_api.get_tophealindes()

    data = []
    counter = 1
    
    for article in articles:
        URL = article["link"]
        summary = GPT_summary.generate_summary_ONE_article(URL)
        result  = {"id": counter,'title': article["title"],"author": article["author"],"body": summary,"link": URL }
        data.append(result)
        counter +=1
    
    

    return data

def Generate_all_articles():
    with open('data.json', 'w') as json_file:
        json.dump({"general news": generate_general_news(),"company news":generate_ESG_articles()}, json_file, indent=4)
    

    
Generate_all_articles()










