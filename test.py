from bs4 import BeautifulSoup
import re
import json
import pandas as pd


with open('betano.html', 'r') as f:
    soup = BeautifulSoup(f.read(), 'lxml')

# for script in soup.find_all("script"):
#     results = re.search(r'^(window)\[\"initial_state\"\]=(.*)', script.text)
#     if results:
#         relevant = results.group(0).split('=', maxsplit=1)[1]
#         data = json.loads(relevant)

#         df = pd.json_normalize(data['structureComponents']['betsofday']['data']['betsOfDay'])
#         df['market.selections'] = df['market.selections'].map(lambda x: pd.DataFrame(x)['price'].tolist())
#         print(df[['teams','market.selections']])


# for team in soup.find_all('div', attrs={'class':['tw-truncate','tw-text-s', 'tw-font-medium', 'tw-leading-s', 'tw-text-n-13-steel']}):
#     print(team)

    padrao = re.compile(r"""
    (?P<tempo>\d+:\d{2})
    (?P<times>\w.+)
    (?P<gols>\d{2})1
    (?P<cota1>\d+\.\d{2})X
    (?P<empate>\d+\.\d{2})2
    (?P<cota2>\d+\.\d{2})
    """, re.VERBOSE)
df = pd.DataFrame(columns=['time', 'teams', 'goals', 'cote1', 'draw', 'cote2'])
tags = 'class="tw-flex tw-justify-center tw-items-center tw-flex-col tw-w-full tw-pt-s s:tw-pt-0"'.split(' ')
for team in soup.find_all('div', attrs={'class': tags}):
    # print(team.get_text())
    # Procurar todas as correspondências no texto
    matches = padrao.finditer(team.get_text())

    # Extrair os dados e organizá-los em uma lista de dicionários
    dados = []
    if matches:
        for match in matches:
            dados.append(match.groupdict())
        for dado in dados:
            df.loc[len(df)] = [x for x in pd.Series(dado)]
print(df)
