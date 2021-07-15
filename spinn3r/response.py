from pprint import pprint
import json
import requests
import logging
import time
from record_processor import format_record
import configparser


config_file_path = os.path.expanduser("~/.credentials.ini")
config_section_name = "spinn3r"
config_parser = configparser.ConfigParser()
files_read = config_parser.read(config_file_path)

creds = {}
for property, value in config_parser.items(config_section_name):
    creds[property] = value

scroll_keep_alive_time = "5m"
index_collection = 'content_*,warm_content_*,cold_content_*'
url = 'http://company.elasticsearch.datastreamer.io/content*/_search?scroll=5m&pretty=true'
spinn3r_query_url = 'http://company.elasticsearch.datastreamer.io/{0}/_search?scroll={1}'.format(
    index_collection, scroll_keep_alive_time)
spinn3r_scroll_url = 'http://company.elasticsearch.datastreamer.io/_search/scroll?scroll={0}'.format(
    scroll_keep_alive_time)

headers = {"X-vendor": creds['X-vendor'],
           "X-vendor-auth": creds['X-vendor-auth']}

logging.basicConfig(filename="spinn3r_query_log",
                    format='[%(filename)s:%(lineno)s - %(module)s:%(funcName)10s() : %(levelname)s] %(message)s', level=logging.INFO)
log = logging.getLogger(__name__)


default_fetch_size = 1000


def search(query_dict):
    try:
        start_time = time.time()
        response = requests.post(
            spinn3r_query_url, headers=headers, json=query_dict)
        result = response
        end_time = time.time()
        log.info("Query Completed. Time taken: %f seconds",
                 end_time - start_time)
        return result
    except Exception as e:
        log.error("%s Error fetching initial response from query", e)


def fetch_scroll_response(scroll_id):
    while True:
        try:
            response = requests.post(
                spinn3r_scroll_url, headers=headers, data=scroll_id)
            result = response
            return result
        except Exception as e:
            log.error(
                "%s Error fetching scroll response from query. Retrying...", e)
            time.sleep(5)


def search_and_write(query_dict):
    query_dict["size"] = default_fetch_size

    try:
        response = search(query_dict)
        results, total_hits, scroll_id = parse_search_response(response)

        if results is not None and total_hits > 0:
            log.info("Total No. of hits: %i", total_hits)

            for i in results:
                try:
                    one_record = format_record(i)
                    collection.insert_one(one_record)
                except Exception as e:
                    log.error(e)
            page = 1
            records_written = 0
            number_results = total_hits

            while scroll_id is not None and number_results > 0:
                response = fetch_scroll_response(scroll_id)
                results, total_hits, scroll_id = parse_search_response(
                    response)
                number_results = 0
                if results is not None:
                    number_results = len(results)
                    for i in results:
                        try:
                            one_record = format_record(i)
                            collection.insert_one(one_record)
                        except Exception as e:
                            log.error(e)
                    records_written += number_results

                page += 1
        log.info("Total number of hits: %i", total_hits)
    except Exception as e:
        log.error(e)
    # to do - write to database
    return


def parse_search_response(response):
    if response.text is not None and len(response.text) > 0:
        try:
            response_data = json.loads(response.text)
            if "hits" in response_data.keys():
                total_hits = response_data["hits"]["total"]
                if "hits" in response_data["hits"]:
                    results = response_data["hits"]["hits"]

                    if "_scroll_id" in response_data.keys():
                        scroll_id = response_data["_scroll_id"]
        except Exception as e:
            log.error(e)
    return results, total_hits, scroll_id
