import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# 수집할 직무 키워드 (JD keywords for crawling)
job_keywords = {
    "HRD": "HRD JD",
    "Data Science": "Data Science JD",
    "Software Engineering": "Software Engineering JD",
    "Product Management": "Product Management JD",
    "Marketing": "Marketing JD"
}

base_folder = "./bing_jds"
os.makedirs(base_folder, exist_ok=True)

# 브라우저 설정 (Browser settings)
options = webdriver.ChromeOptions()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("user-agent=Mozilla/5.0")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# 직무별 크롤링 (Crawling by job)
for label, query in job_keywords.items():
    print(f"\n[{label}] 수집 시작")
    folder_path = os.path.join(base_folder, label)
    os.makedirs(folder_path, exist_ok=True)
    visited = set()

    for page in range(3):  # 최대 3페이지 (up to 3 pages -> you can adjust)
        first_index = 1 + page * 10
        search_url = f"https://www.bing.com/search?q={query}+filetype%3Apdf&first={first_index}"
        driver.get(search_url)
        time.sleep(2)

        links = driver.find_elements(By.XPATH, "//a[@href]") 
        for link in links:
            href = link.get_attribute("href")
            if href and ".pdf" in href.lower() and href not in visited:
                visited.add(href)
                filename = href.split("/")[-1].split("?")[0]
                save_path = os.path.join(folder_path, filename)

                try:
                    headers = {"User-Agent": "Mozilla/5.0"}
                    r = requests.get(href, headers=headers, timeout=10)
                    if r.status_code == 200 and href.endswith(".pdf"):
                        with open(save_path, "wb") as f:
                            f.write(r.content)
                        print(f"[+] 저장 완료: {filename}") # Save completed
                except Exception as e:
                    print(f"[!] 다운로드 실패: {href} - {e}") # Download failed

driver.quit()

input("\n[ENTER] 누르면 종료됩니다.") # Press ENTER to exit
