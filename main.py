from scraper import scrap_team_data
from display import afficher_classement
from scraper_matchs import scrap_match_data

def main():
    team_data_list = scrap_team_data()
    afficher_classement(team_data_list)

if __name__ == "__main__":
    main()
