import requests
from bs4 import BeautifulSoup

def decode_secret_message(url):
   
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to retrieve document. Status code: {response.status_code}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    rows = soup.find_all('tr')
    
    data_points = []
    max_x = 0
    max_y = 0
    
    for row in rows[1:]:
        cols = row.find_all(['td', 'th'])
        if len(cols) >= 3:
            try:
                x = int(cols[0].text.strip())
                char = cols[1].text.strip()
                y = int(cols[2].text.strip())
                
                data_points.append((x, y, char))
                max_x = max(max_x, x)
                max_y = max(max_y, y)
            except ValueError:
                continue

    if not data_points:
        print("No valid character data found in the document.")
        return

    grid = [[" " for _ in range(max_x + 1)] for _ in range(max_y + 1)]

    for x, y, char in data_points:
        grid[max_y - y][x] = char

    for row in grid:
        print("".join(row))

doc_url = "https://docs.google.com/document/d/e/2PACX-1vTMOmshQe8YvaRXi6gEPKKlsC6UpFJSMAk4mQjLm_u1gmHdVVTaeh7nBNFBRlui0sTZ-snGwZM4DBCT/pub"
# doc_url = "https://docs.google.com/document/d/e/2PACX-1vSvM5gDlNvt7npYHhp_XfsJvuntUhq184By5xO_pA4b_gCWeXb6dM6ZxwN8rE6S4ghUsCj2VKR21oEP/pub"
decode_secret_message(doc_url)