import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrap_team_data():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get('https://www.flashscore.fr/football/france/ligue-1/classement/')

    team_data_list = []
    
    # Extraction des éléments contenant les données de chaque équipe
    teams = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class, "table__row")]'))
    )
    
    # Collecte des informations pour chaque équipe
    for team in teams:
        try:
            team_position = team.find_element(By.XPATH, './/div[contains(@class, "tableCellRank")]').text
            team_logo = team.find_element(By.XPATH, './/div[contains(@class, "tableCellParticipant")]/div/a/img').get_attribute('src')
            team_name = team.find_element(By.XPATH, './/div[contains(@class, "tableCellParticipant")]/div/a[@class="tableCellParticipant__name"]').text
            nb_played = team.find_element(By.XPATH, './/span[contains(@class, "table__cell--value")][1]').text
            nb_victory = team.find_element(By.XPATH, './/span[contains(@class, "table__cell--value")][2]').text
            nb_draw = team.find_element(By.XPATH, './/span[contains(@class, "table__cell--value")][3]').text
            nb_lose = team.find_element(By.XPATH, './/span[contains(@class, "table__cell--value")][4]').text
            score = team.find_element(By.XPATH, './/span[contains(@class, "table__cell--score")]').text
            points = team.find_element(By.XPATH, './/span[contains(@class, "table__cell--points")]').text

            team_data = {
                'position': team_position,
                'logo': team_logo,
                'name': team_name,
                'matches_played': nb_played,
                'victories': nb_victory,
                'draws': nb_draw,
                'losses': nb_lose,
                'score': score,
                'points': points
            }
            team_data_list.append(team_data)
        except Exception as e:
            print(f"Erreur lors de la récupération des données pour une équipe : {e}")

    driver.quit()
    
    # Enregistre les données dans un fichier JSON
    with open("ligue1_team_data.json", "w", encoding="utf-8") as file:
        json.dump(team_data_list, file, ensure_ascii=False, indent=4)
    
    return team_data_list
