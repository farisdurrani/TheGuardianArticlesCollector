from bs4 import BeautifulSoup
from decouple import config
from random import random
from typing import List, Dict
import os
import pandas as pd
import requests

API_KEY = config("API_KEY")
START_DATES = ["2015-01-01",
               "2015-03-01",
               "2015-06-01",
               "2015-09-01",
               "2015-12-01",

               "2016-03-01",
               "2016-06-01",
               "2016-09-01",
               "2016-12-01",

               "2017-03-01",
               "2017-06-01",
               "2017-09-01",
               "2017-12-01",

               "2018-03-01",
               "2018-06-01",
               "2018-09-01",
               "2018-12-01",

               "2019-03-01",
               "2019-06-01",
               "2019-09-01",
               "2019-12-01",

               "2020-03-01",
               "2020-06-01",
               "2020-09-01",
               "2020-12-01",

               "2021-03-01",
               "2021-06-01",
               "2021-09-01",
               "2021-12-01",

               "2022-03-01",
               "2022-06-01",
               "2022-09-01",
               ]


def abort(contentsToWrite: List[Dict[str, any]], filename):
    writeToCSV(contentsToWrite, filename)
    raise Exception(f"ERROR: Aborted")


def writeToCSV(contentsToWrite: List[Dict[str, any]], filename: str):
    df = pd.DataFrame(contentsToWrite)
    randomNumber = int(random() * 1e4)
    filepath = f"outputs/{filename}-{randomNumber}.csv"
    df.to_csv(filepath, encoding='utf-8')
    contentsToWrite.clear()
    print(f"File successfully {filepath} written with "
          f"size {os.path.getsize(f'{filepath}') / 1e6: _} MB")


def queryAPI(currentPage, monthListIndex):
    params = {
        "format": "json",
        "from-date": START_DATES[monthListIndex],
        "to-date": START_DATES[monthListIndex + 1],
        "show-tags": "contributor",
        "show-fields": "headline,short-url,body",
        "api-key": API_KEY,
        "lang": "en",
        "page-size": "50",
        "order-by": "oldest",
        "page": str(currentPage),
    }
    return requests.get("https://content.guardianapis.com/search",
                        params=params).json()


def appendResults(results, contentsToWrite):
    for result in results:
        contentType = result.get("type", None)

        if contentType != "article":
            continue

        articleContent = {"timestamp": result.get("webPublicationDate", None),
                          "webUrl": result.get("webUrl", None),
                          "headline": result["fields"].get("headline", None),
                          "sectionId": result.get("sectionId", None),
                          "sectionName": result.get("sectionName", None),
                          "site": "The Guardian"}

        bodyHTML = result["fields"].get("body", None)
        if not bodyHTML:
            continue
        articleContent["bodyContent"] = \
            BeautifulSoup(bodyHTML, 'html.parser').get_text()
        if len(articleContent["bodyContent"]) < 10:
            # skip super short articles, e.g., may only contain videos or images
            continue

        authors = result["tags"]
        for author in authors:
            articleContent["authorUrl"] = author.get("id", None)
            articleContent["authorFirstName"] = author.get("firstName", None)
            articleContent["authorLastName"] = author.get("lastName", None)
            break
        contentsToWrite.append(articleContent)


def getThisPage(currentPage, contentsToWrite, monthListIndex):
    response = queryAPI(currentPage, monthListIndex)

    statusIsOk = (response
                  and response.get("response", None)
                  and response["response"].get("status", None) == "ok")
    if not statusIsOk:
        print("response:", response)
        raise ValueError("Status is not OK")

    appendResults(response["response"]["results"], contentsToWrite)

    totalPages = response["response"]["pages"]
    return totalPages


def getAllArticles():
    for monthListIndex in range(len(START_DATES) - 1):
        collect3Months(monthListIndex)


def collect3Months(monthListIndex):
    contentsToWrite = []
    currentPage = 1
    totalPages = currentPage

    while currentPage <= totalPages:
        if currentPage % 1000 == 0:
            writeToCSV(contentsToWrite, f"g-month{monthListIndex}-page{currentPage}")
        print(f"Acquiring month {monthListIndex} / {len(START_DATES)} "
              f"page {currentPage} / {totalPages}")
        try:
            totalPages = getThisPage(currentPage, contentsToWrite,
                                     monthListIndex)
        except Exception:
            abort(contentsToWrite, f"g-month{monthListIndex}-page{currentPage}finalE")
        currentPage += 1

    writeToCSV(contentsToWrite, f"g-month{monthListIndex}-page{currentPage}final")


def main():
    print('Starting')
    getAllArticles()


if __name__ == '__main__':
    main()
