import csv
import requests

from config import NEO4J_IMPORT_DIRECTORY


def ExtractHtmlFromUrl(url: str):
    response = requests.get(url)
    return response.text


def SaveMatrixToCsv(matrix, file_name):
    with open(NEO4J_IMPORT_DIRECTORY + file_name, "w+", encoding="utf-8") as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',')
        csv_writer.writerows(matrix)
