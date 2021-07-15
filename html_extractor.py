#!../runtime/bin/python3

from typing import Dict
from typing import List
from typing import Tuple

from pymongo import MongoClient
import bs4
import newspaper
import readability
import justext
from langdetect import detect
import os
import datetime
from datetime import date
import time
import re
import json

import logging
logging.basicConfig(format='%(asctime)s [%(filename)s:%(lineno)s - %(module)s:%(funcName)10s() : %(levelname)s] %(message)s', level=logging.WARN)


class Exception_Util(object):
    __exception = None
    __object_type = None

    def __init__(self, exception):
        self.__exception = exception
        self.__object_type = type(exception)

    def to_string(self):
        exception_string = ''

        try:
            exception_string = str(self.__object_type) + ':' + str(self.__exception)
        except Exception as e:
            exception_string = 'unknown'

        return exception_string

class ExtractionApproach(object):
    beautiful_soup = 'beautiful soup'
    readability = 'readability'
    newspaper = 'newspaper'
    justext = 'justext'

class HtmlExtractor(object):
    __justext_stop_list = justext.get_stoplist("English")

    extraction_priorities_1 = [ExtractionApproach.newspaper,
                               ExtractionApproach.justext]

    extraction_priorities_2 = [#ExtractionApproach.readability,
                               ExtractionApproach.beautiful_soup]

    @staticmethod
    def extract_html_info(html: str) -> Tuple:
        """

        :param html:
        :return: A tuple with the following fields:
        i) text content
        ii) meta_data
        iii) extraction approach
        """

        meta_data = None

        text_content = ''
        max_len = len(text_content)
        extraction_approach = None
        if HtmlExtractor.extraction_priorities_1 is not None and len(HtmlExtractor.extraction_priorities_1) > 0:
            extraction_approach = HtmlExtractor.extraction_priorities_1[0]

        for approach in HtmlExtractor.extraction_priorities_1:
            text = None
            if approach == ExtractionApproach.newspaper:
                text, meta_data = HtmlExtractor.__extract_text_and_meta_data_with_newspaper(html, get_meta_data=True)
            else:
                text = HtmlExtractor.__extract_from_string(html, extraction_approach=approach)

            if text is not None:
                text.replace('\s+', ' ').strip()
                length = len(text)

                #logging.info("Approach: %s, size of extracted text: %i bytes", approach, length)
                if length > max_len:
                    text_content = text
                    max_len = length
                    extraction_approach = approach

        if max_len == 0:
            for approach in HtmlExtractor.extraction_priorities_2:
                text = None
                if approach == ExtractionApproach.newspaper:
                    text, meta_data = HtmlExtractor.__extract_text_and_meta_data_with_newspaper(html,
                                                                                                get_meta_data=True)
                else:
                    text = HtmlExtractor.__extract_from_string(html, extraction_approach=approach)

                if text is not None:
                    text.replace('\s+', ' ').strip()
                    length = len(text)

                    #logging.info("Approach: %s, size of extracted text: %i bytes", approach, length)

                    if length > max_len:
                        text_content = text
                        max_len = length
                        extraction_approach = approach

        return (text_content, meta_data, extraction_approach)

    @staticmethod
    def __extract_from_string(html: str, extraction_approach = ExtractionApproach.readability) -> str:
        text = ''
        length = len(html)
        if length > 0:
            #logging.info("Approach: %s, HTML size: %i bytes", extraction_approach, length)

            if extraction_approach == ExtractionApproach.beautiful_soup:
                text = HtmlExtractor.__extract_from_string_with_beautiful_soup(html)
            elif extraction_approach == ExtractionApproach.readability:
                text = HtmlExtractor.__extract_from_string_with_readability(html)
            elif extraction_approach == ExtractionApproach.newspaper:
                text = HtmlExtractor.__extract_from_string_with_newspaper(html)
            elif extraction_approach == ExtractionApproach.justext:
                text = HtmlExtractor.__extract_from_string_with_justext(html)

        return text

    @staticmethod
    def __extract_from_string_with_readability(content: str) -> str:
        text = ''
        if len(content) > 0:
            try:
                html = readability.Document(content).summary()
                text = HtmlExtractor.__extract_from_string_with_beautiful_soup(html)
            except Exception as e:
                exception_string = Exception_Util(e).to_string()
                logging.exception('Exception: %s', exception_string)

        return text

    @staticmethod
    def __extract_from_string_with_beautiful_soup(content: str) -> str:
        text = ''
        if len(content) > 0:
            try:
                soup = bs4.BeautifulSoup(content, "lxml")

                # kill all script and style elements
                for script in soup(["script", "css", "style", "meta", "link", "span"]):
                    script.extract()  # rip it out

                # get text
                text = soup.get_text()
            except Exception as e:
                exception_string = Exception_Util(e).to_string()
                logging.exception('Exception: %s', exception_string)

        return text

    @staticmethod
    def __extract_text_and_meta_data_with_newspaper(html: str, get_meta_data : bool =False) -> Tuple:
        """

        :param html:
        :param get_meta_data:
        :return: A tuple with the following fields:
        i) textual content extracted from the HTML article
        ii) meta data from the HTML article
        """
        meta_data = {}
        text = ''

        length = len(html)

        if len(html) > 0:
            #logging.info("Approach: newspaper, HTML size: %i bytes", length)

            try:
                article = newspaper.Article('')
                article.set_html(html)
                #logging.info('Start parsing .....:\n%s', html)
                article.parse()
                #logging.info('Parsing completed.')

                text = article.text
                if get_meta_data is True:
                    meta_data = HtmlExtractor.__get_html_meta_data(article)
            except Exception as e:
                exception_string = Exception_Util(e).to_string()
                logging.exception('Exception: %s', exception_string)

        return (text,meta_data)

    @staticmethod
    def __extract_from_string_with_newspaper(content: str) -> str:
        results = HtmlExtractor.__extract_text_and_meta_data_with_newspaper(content,get_meta_data=False)

        return results[0]

    @staticmethod
    def __get_value(object):
        result = None

        if object is not None:
            try:
                if isinstance(object, set) is True:
                    object = list(object)

                if isinstance(object, datetime.datetime) is True:
                    result = str(object.strftime('%Y-%m-%d %a %H:%M:%S %z'))
                else:
                    if len(object) == 0:
                        result = None
                    else:
                        result = object
            except Exception as e:
                exception_string = Exception_Util(e).to_string()
                logging.exception('Exception: %s, Type: %s', exception_string, type(object))

        return result

    @staticmethod
    def __get_html_meta_data(newspaper_article) -> Dict:
        """

        :type newspaper_article: Must be an Article object that is generated by the Newspaper module.
        :param newspaper_article:
        :return:
        """
        meta_data = {}
        year = None
        month = None
        day = None

        if newspaper_article is not None:
            try:
                html_meta_data = {'title': HtmlExtractor.__get_value(newspaper_article.title),
                                  'authors': HtmlExtractor.__get_value(newspaper_article.authors),
                                  'tags': HtmlExtractor.__get_value(newspaper_article.tags),
                                  'publish_date': HtmlExtractor.__get_value(newspaper_article.publish_date),
                                  'meta_lang': HtmlExtractor.__get_value(newspaper_article.meta_lang),
                                  'canonical_link': HtmlExtractor.__get_value(newspaper_article.canonical_link),
                                  'meta_data': HtmlExtractor.__get_value(newspaper_article.meta_data)}

                for key in html_meta_data:
                    value = html_meta_data[key]
                    if value is not None:
                        meta_data[key] = value

            except Exception as e:
                exception_string = Exception_Util(e).to_string()
                logging.exception('Exception: %s', exception_string)

        return meta_data

    @staticmethod
    def __extract_from_string_with_justext(content: str) -> str:
        text = ''
        if len(content) > 0:
            try:
                paragraphs = justext.justext(content, HtmlExtractor.__justext_stop_list)
            except Exception as e:
                exception_string = Exception_Util(e).to_string()
                logging.exception('Exception: %s', exception_string)
                return text

            for paragraph in paragraphs:
                if not paragraph.is_boilerplate:
                    try:
                        if len(text) > 0:
                            text = text + '\n'
                        # language = detect(paragraph.text)
                        # if language == ExtractTextJob.english_code:
                        text = text + paragraph.text
                    except Exception as e:
                        exception_string = Exception_Util(e).to_string()
                        logging.warning('Exception: %s', exception_string)

        return text
