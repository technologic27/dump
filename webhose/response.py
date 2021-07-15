from pprint import pprint
import json
import requests
import logging
import time


web_hose_url = "http://webhose.io/filterWebContent?token=2dd4a789-5376-4536-999d-9262736fbcbf"

headers = {"Accept": 'text/plain'}


logging.basicConfig(filename="webhose_query_log",
                    format='[%(filename)s:%(lineno)s - %(module)s:%(funcName)10s() : %(levelname)s] %(message)s', level=logging.INFO)
log = logging.getLogger(__name__)


def search(params):
    try:
        start_time = time.time()
        response = requests.get(web_hose_url, headers=headers, params=params)
        result = response
        end_time = time.time()
        log.info("Query Completed. Time taken: %f seconds",
                 end_time - start_time)
        return result
    except Exception as e:
        log.error("%s Error fetching initial response from query", e)


def fetch_scroll_response(next_url):
    while True:
        try:
            web_hose_url = "http://webhose.io" + next_url
            response = requests.get(web_hose_url)
            result = response
            return result
        except Exception as e:
            log.error("%s Error fetching next page from query. Retrying...", e)
            time.sleep(5)


def search_and_write(params):
    try:
        response = search(params)
        print(response)
        next_url, response_data = parse_search_response(response)
        print(next_url)

        for one_record in response_data["posts"]:
            try:
                collection.insert_one(one_record)
            except Exception as e:
                log.error(e)

            while next_url is not None:
                response = fetch_scroll_response(next_url)
                next_url, response_data = parse_search_response(response)
                for one_record in response_data["posts"]:
                    try:
                        collection.insert_one(one_record)
                    except Exception as e:
                        log.error(e)

    except Exception as e:
        log.error(e)
    return


def parse_search_response(response):
    if response.text is not None and len(response.text) > 0:
        try:
            response_data = json.loads(response.text)

            if "next" in response_data.keys():
                next_url = response_data["next"]

        except Exception as e:
            log.error(e)
    return next_url, response_data
