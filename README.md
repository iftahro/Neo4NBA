# Neo4NBA
Neo4NBA is a neo4j graph db of the NBA league over the past decade (2010-20). 
The graph contains data about:

-	Teams and divisions
-	All players played
- Yearly rosters
-	Coaches
-	Regular season stats
-	Draft picks (also rookies and undrafted)
-	Personal awards (MVP, MIP etc.)
-	Playoff series
-	Players nicknames

## Requirements
### General
Python 3.7.0 (https://www.python.org/downloads/)

Local neo4j server 3.5.14 (https://neo4j.com/download-center/#community)

### Packages
neo4j 1.7.0

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install neo4j.

```bash
pip install neo4j
```

## Setup
### config.py
In the config file you will need to enter your neo4j server credentials and bolt address
```python
NEO4J_USERNAME = "username"
NEO4J_PASSWORD = "passwrod"
NEO4J_BOLT_ADDRESS = "bolt_address"
```

The graph is based on static csv files that are located in the 'graph_files' folder.
In order to copy them into your local server you will need to enter your server import directory path
the and set the *should_copy* flag *True*

```python
NEO4J_IMPORT_DIRECTORY = "import_dir_path"
SHOULD_COPY_FILES_TO_SERVER = True
```
Thats it! Your'e good to go.

## To Be Added

- NBA2K game ratings
-	Regular season games

## Resources
https://www.basketball-reference.com/
https://www.kaggle.com/pmp5kh/nba-draft-19802017
https://hoopshype.com/2019/02/24/all-the-nicknames-in-nba-history/
https://data.world/datasets/nba
