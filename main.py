from scraper import scrap_team_data
from display import afficher_classement

def main():
    team_data_list = scrap_team_data()
    afficher_classement(team_data_list)

if __name__ == "__main__":
    main()
