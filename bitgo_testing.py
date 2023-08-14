from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import json

def main():
    # Set up Chrome WebDriver
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    chrome_options.binary_location = r"C:\Users\home\Downloads\chrome-win64\chrome-win64\chrome.exe"
    service = Service("./chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    try:
        # Open the website
        url = "https://blockstream.info/block/000000000000000000076c036ff5119e5a5a74df77abf64203473364509f7732"
        driver.get(url)
                
        # Find the div element with class name "transactions"
        transaction_div = driver.find_element(By.CLASS_NAME, "transactions")
        
        # Extract the text from the h3 element
        h3_element = transaction_div.find_element(By.TAG_NAME, "h3")
        extracted_text = h3_element.text
        print("Extracted Text:")
        print(extracted_text)
        
        # Extract transaction data
        new_out = extract_transaction_data(driver)
        
        # Save results to a JSON file
        with open('result.json', 'w') as fp:
            json.dump(new_out, fp)
            
    finally:
        # Close the WebDriver
        driver.quit()

def extract_transaction_data(driver):
    ins_outs = driver.find_elements(By.CLASS_NAME, "ins-and-outs")
    
    out = []
    for each in ins_outs:
        tmp = {"ins": [], "outs": []}
        ins = each.find_element(By.CLASS_NAME, "vins")
        for each_in in ins.find_elements(By.CLASS_NAME, "vin"):
            tmp["ins"].append(each_in.text)
        outs = each.find_element(By.CLASS_NAME, "vouts")
        for each_out in outs.find_elements(By.CLASS_NAME, "vout"):
            tmp["outs"].append(each_out.text)
        out.append(tmp)
    
    new_out = [each for each in out if len(each["ins"]) == 1 and len(each["outs"]) == 2]
    return new_out

if __name__ == "__main__":
    main()
