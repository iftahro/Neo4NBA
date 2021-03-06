import logging
import os

# Graph files
GRAPH_FILES_DIRECTORY_PATH = os.path.dirname(__file__).replace("source", "graph_files")

# Logging
LOGGING_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_LEVEL = logging.DEBUG

# NBA
PERSONAL_AWARDS = {"Most Valuable Player": "MVP",
                   "Rookie of the Year": "ROY",
                   "Most Improved Player": "MIP",
                   "Defensive Player of the Year": "DPOY",
                   "Sixth Man of the Year": "SMOY",
                   "Finals Most Valuable Player": "FMVP",
                   "All Star Game Most Valuable Player": "AMVP"}

INVALID_TEAMS_LABELS = {
    "'BKN'": ['NJN', 'BRK'],
    "'NOP'": ['NOH'],
    "'PHX'": ['PHO'],
    "'CHA'": ['CHO']
}

EXCEPTIONAL_YEAR_GAMES = {
    2012: 990,
    2013: 1228,
}

SUPPORTED_YEARS = [year for year in range(2010, 2021)]
CURRENT_YEAR = 2020
