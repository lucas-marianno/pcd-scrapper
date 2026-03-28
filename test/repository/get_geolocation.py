import requests

url = "https://gatewaywhitelabel.empregos.com.br/autocomplete/Location"

payload = {"term": "São Bernardo do Campo, SP", "geolocation": None}
headers = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "en-US,en;q=0.7",
    "authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJtb2RlbCI6IntcIklkXCI6XCI1Nzc1NjdcIixcIkZpcnN0TmFtZVwiOlwiTW9yZmV1IE9uZWlyb3NcIixcIkdlb0xvY2F0aW9uXCI6bnVsbCxcIkVtYWlsXCI6XCJ2YWRvaGE1MjAyQGV4YWh1dC5jb21cIixcIkNhcHRhdGlvblwiOlwiU2l0ZVwiLFwiSGFzaFwiOlwiN2NkOGYwOTkwNDZiNWJlMTUyZmRkMWVmNzRlMTY5ODlcIixcIlNlY29uZGFyeUlkXCI6XCI0OTc1NzlcIixcIlN0YXR1c1wiOjQxMixcIlR5cGVDb2RlXCI6bnVsbH0iLCJ3aF9wbGF0YWZvcm0iOiIiLCJqdGkiOiIwMjE2NmQwOC1lMjZmLTQ0M2ItYTYzNi00YTQ4ZjU1MWFmZjEiLCJpYXQiOjE3NzQ2NTUzNTAsIm5iZiI6MTc3NDY1NTM0OSwiZXhwIjoyMDkwMDE1MzQ5LCJpc3MiOiJlbXByZWdvcy1yZWNydXRhZG9yIiwiYXVkIjoiZW1wcmVnb3MtY29tLWJyIn0.38hlnbSfrpFEDZ0yAn6cmtXxM7t2V-KJ31t2gg8wvXc",
    "content-type": "application/json",
    "origin": "https://b2b.empregos.com.br",
    "priority": "u=1, i",
    "referer": "https://b2b.empregos.com.br/",
    "sec-ch-ua": '"Chromium";v="146", "Not-A.Brand";v="24", "Brave";v="146"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Linux"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "sec-gpc": "1",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36",
}

response = requests.post(url, json=payload, headers=headers)

print(response.json())
