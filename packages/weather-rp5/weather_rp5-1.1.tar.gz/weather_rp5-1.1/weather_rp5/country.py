import requests
from bs4 import BeautifulSoup

def get_all_station_urls_for_country(country_name: str) -> list[str]:
    url = f"https://rp5.ru/Weather_in_{country_name}"
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    a_tags = soup.find_all("a", class_="href20")
    return [f"https://rp5.ru/{a_tag['href']}" for a_tag in a_tags]

print(get_all_station_urls_for_country("Afghanistan"))