from playwright.sync_api import Playwright, sync_playwright, expect
import pandas as pd
from time import sleep
import json
from bs4 import BeautifulSoup
import re


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context( 
                                  locale="pt-BR", 
                                  user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")
    page = context.new_page()
    url = "https://br.betano.com/live"
    page.goto(url)
    page.wait_for_load_state('load') # “load”|”domcontentloaded”|”networkidle”

    sleep(3)

    soup = BeautifulSoup(page.content(), 'lxml')

    # for script in soup.find_all("script"):
    #     results = re.search(r'^(window)\[\"initial_state\"\]=(.*)', script.text)
    #     if results:
    #         relevant = results.group(0).split('=', maxsplit=1)[1]
    #         data = json.loads(relevant)

    #         df = pd.json_normalize(data['structureComponents']['betsofday']['data']['betsOfDay'])
    #         df['market.selections'] = df['market.selections'].map(lambda x: pd.DataFrame(x)['price'].tolist())
    #         print(df[['teams','market.selections']])

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

    with open('betano.html', 'w', encoding='utf-8') as f:
        f.write(page.content())
        
    

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)

