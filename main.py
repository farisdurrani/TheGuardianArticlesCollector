from bs4 import BeautifulSoup
from decouple import config
from typing import List, Dict
import os
import pandas as pd
import requests

API_KEY = config("TEST_API_KEY")
START_DATE = "2015-01-01"


def abort(contentsToWrite: List[Dict[str, any]], currentPage):
    writeToCSV(contentsToWrite, f"g-page{currentPage}finalE")
    raise Exception(f"ERROR: Aborted at page {currentPage}")


def writeToCSV(contentsToWrite: List[Dict[str, any]], filename: str):
    df = pd.DataFrame(contentsToWrite)
    df.to_csv(f"{filename}.csv", encoding='utf-8')
    contentsToWrite.clear()
    print(f"File successfully {filename} written with "
          f"size {os.path.getsize(f'{filename}.csv') / 1e6: _} MB")


def queryAPI(currentPage):
    params = {
        "format": "json",
        "from-date": START_DATE,
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
            print(contentType)
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


def getThisPage(currentPage, contentsToWrite):
    response = queryAPI(currentPage)

    statusIsOk = (response
                  and response.get("response", None)
                  and response["response"].get("status", None) == "ok")
    if not statusIsOk:
        abort(contentsToWrite, currentPage)

    appendResults(response["response"]["results"], contentsToWrite)

    totalPages = response["response"]["pages"]
    return totalPages


def getAllArticles():
    contentsToWrite = []
    currentPage = 10
    totalPages = currentPage

    while currentPage <= totalPages:
        if currentPage % 20 == 0:
            writeToCSV(contentsToWrite, f"g-page{currentPage}")
            return
        print(f"Acquiring page {currentPage} / {totalPages}")
        try:
            totalPages = getThisPage(currentPage, contentsToWrite)
        except Exception:
            abort(contentsToWrite, currentPage)
        currentPage += 1

    writeToCSV(contentsToWrite, f"g-page{currentPage}final")


def main():
    print('Starting')
    getAllArticles()


if __name__ == '__main__':
    main()
