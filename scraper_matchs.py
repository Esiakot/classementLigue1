import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrap_match_data():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('window-size=1920x1080')
    options.add_argument('--blink-settings=imagesEnabled=false')
    options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
    options.add_argument('--disable-javascript')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get('https://www.flashscore.fr/football/france/ligue-1/resultats/')

    match_data_list = []
    team_ids = {}

    try:
        matches = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.event__match"))
        )

        for index, match in enumerate(matches):
            try:
                home_team = match.find_element(By.CSS_SELECTOR, "div.event__homeParticipant").text
                away_team = match.find_element(By.CSS_SELECTOR, "div.event__awayParticipant").text
                home_score = match.find_element(By.CSS_SELECTOR, "div.event__score.event__score--home").text
                away_score = match.find_element(By.CSS_SELECTOR, "div.event__score.event__score--away").text

                if home_team not in team_ids:
                    team_ids[home_team] = f'team_{len(team_ids) + 1}'
                if away_team not in team_ids:
                    team_ids[away_team] = f'team_{len(team_ids) + 1}'

                match_data = {
                    'id': f'match_{index + 1}',
                    'home_team': {
                        'name': home_team,
                        'id': team_ids[home_team]
                    },
                    'away_team': {
                        'name': away_team,
                        'id': team_ids[away_team]
                    },
                    'home_score': home_score,
                    'away_score': away_score
                }
                match_data_list.append(match_data)
            except Exception as e:
                print(f"Erreur lors de la récupération des données du match : {e}")
    except Exception as e:
        print(f"Erreur lors de l'attente des éléments de match : {e}")

    driver.quit()

    with open("ligue1_match_data.json", "w", encoding="utf-8") as file:
        json.dump(match_data_list, file, ensure_ascii=False, indent=4)

    return match_data_list, team_ids

match_data_list, team_ids = scrap_match_data()
