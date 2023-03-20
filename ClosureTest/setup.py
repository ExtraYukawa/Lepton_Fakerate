import requests
from bs4 import BeautifulSoup
import os

os.system("cp ../python/CMS* .")
os.system("mkdir -p data")
os.chdir("data")

repo_url = "https://github.com/ExtraYukawa/Script_ForMVA/tree/main/data"
page = requests.get(repo_url)
soup = BeautifulSoup(page.content, "html.parser")
links = soup.findAll("a",{"class": "js-navigation-open Link--primary"})
for link in links:
  subpage = requests.get("https://github.com/" + link["href"])
  subsoup = BeautifulSoup(subpage.content, "html.parser")
  for a in subsoup.findAll("a", {"id": "raw-url"}):
    os.system("wget https://github.com/" + a["href"])
