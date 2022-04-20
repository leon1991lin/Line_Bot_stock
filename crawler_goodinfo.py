import requests
from bs4 import BeautifulSoup
import pandas as pd

stockCode = 2303

url = f"https://statementdog.com/analysis/{stockCode}/du-pont-analysis"

headers = {
             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
          }

res = requests.get(url, headers=headers)
res.encoding = 'utf-8'
soup = BeautifulSoup(res.text, 'html.parser')

table = soup.select("table tr")

dict = {}
for item in table:
    content = item.text.split("\n")[1:-1]
    dict[content[0]] = content[1:]

df = pd.DataFrame(dict)
df[['稅後淨利率','總資產週轉','ROE']] = df[['稅後淨利率','總資產週轉','ROE']].astype(float)

df["財務槓桿"] = df.apply(lambda x:((x['ROE']/x['總資產週轉'])/x['稅後淨利率']),axis=1)
print(df)

df.to_csv("dupont_analysis_data.csv")

