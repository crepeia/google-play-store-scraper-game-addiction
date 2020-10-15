from utils import store_apps_from_category

CATEGORIES = {
    "GAME_ACTION": "GAME_ACTION",
    "GAME_ADVENTURE": "GAME_ADVENTURE",
    "GAME_ARCADE": "GAME_ARCADE",
    "GAME_BOARD": "GAME_BOARD",
    "GAME_CARD": "GAME_CARD",
    "GAME_CASINO": "GAME_CASINO",
    "GAME_CASUAL": "GAME_CASUAL",
    "GAME_EDUCATIONAL": "GAME_EDUCATIONAL",
    "GAME_FAMILY": "GAME_FAMILY",
    "GAME_MUSIC": "GAME_MUSIC",
    "GAME_PUZZLE": "GAME_PUZZLE",
    "GAME_RACING": "GAME_RACING",
    "GAME_ROLE_PLAYING": "GAME_ROLE_PLAYING",
    "GAME_SIMULATION": "GAME_SIMULATION",
    "GAME_SPORTS": "GAME_SPORTS",
    "GAME_STRATEGY": "GAME_STRATEGY",
    "GAME_TRIVIA": "GAME_TRIVIA",
    "GAME_WORD": "GAME_WORD",
}

if __name__ in '__main__':
    try:
        for category in CATEGORIES:
            store_apps_from_category(category)
            print("Category {0} was stored.".format(category))
        print("Categories stored")
    except:
        print("")
