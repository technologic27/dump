
from utils.configuration import Configuration

from typing import List
from typing import Dict
from typing import Tuple

import os
import json
from pymongo import MongoClient
from pymongo import ReplaceOne
from pymongo import WriteConcern
from pymongo.collection import Collection
from pymongo.results import InsertManyResult
from pymongo.results import BulkWriteResult
from pymongo.results import UpdateResult

import logging
logging.basicConfig(format='%(asctime)s [%(filename)s:%(lineno)s - %(module)s:%(funcName)10s() : %(levelname)s] %(message)s',
                    level=logging.DEBUG)


class MongoDB_Client(object):
    log = None

    mongodb_client = None

    configuration = None
    configuration_file_name = '../resources/config.ini'
    configuration_section_name = 'mongo'

    collection_map = {}

    def __init__(self, configuration_file_name=None, configuration_section_name=None):
        self.log = logging.getLogger(self.__class__.__name__)

        if configuration_file_name is not None:
            self.configuration_file_name = configuration_file_name

        if configuration_section_name is not None:
            self.configuration_section_name = configuration_section_name

        self.__init_configuration(self.configuration_file_name)
        self.__init_mongodb_client()

    def __init_configuration(self, file_name):
        if os.path.exists(file_name):
            self.configuration = Configuration(file_name)

    def __get_configuration(self, parameter_name):
        result = None

        if self.configuration is not None and parameter_name is not None:
            result = self.configuration.get_option(
                self.configuration_section_name, parameter_name)

        return result

    def __init_mongodb_client(self):
        username = self.__get_configuration('username')
        password = self.__get_configuration('password')
        host = self.__get_configuration('host')
        port = self.__get_configuration('port')

        try:
            self.mongodb_client = MongoClient(
                "mongodb://{}:{}@{}:{}".format(username, password, host, port))
        except Exception as e:
            self.log.error(e)
            self.mongodb_client = None

    def close(self):
        if self.mongodb_client is not None:
            try:
                self.mongodb_client.close()
            except Exception as e:
                self.log.error(e)

    def get_mongodb_collection(self,
                               mongodb_database_name: str,
                               mongodb_collection_name: str,
                               w: int=0,
                               wtimeout: int=60000) -> Collection:
        collection = None

        if self.mongodb_client is not None:
            collection_key = (mongodb_database_name, mongodb_collection_name)
            if collection_key in self.collection_map:
                collection = self.collection_map[collection_key]

            if collection is None:
                try:
                    database = self.mongodb_client.get_database(
                        mongodb_database_name)
                except Exception as e:
                    self.log.error(e)
                    database = None

                if database is not None:
                    collection = database[mongodb_collection_name]

            if collection is not None:
                if w >= 1:
                    collection = collection.with_options(
                        write_concern=WriteConcern(w=w, wtimeout=wtimeout)
                    )

        return collection

    def create_index(self, mongodb_database_name: str, mongodb_collection_name: str,
                     index_name: str, index_field_name: str,
                     w: int = 0,
                     wtimeout: int = 60000):
        mongodb_collection = self.get_mongodb_collection(
            mongodb_database_name, mongodb_collection_name, w=w, wtimeout=wtimeout)
        if mongodb_collection is not None:
            try:
                mongodb_collection.create_index(index_field_name, name=index_name,
                                                background=True, sparse=True)
            except Exception as e:
                self.log.error(e)

    def insert_one(self,
                   mongodb_database_name: str,
                   mongodb_collection_name: str,
                   doc: Dict,
                   w: int = 0,
                   wtimeout: int = 60000):
        id = None

        if doc is not None:
            mongodb_collection = self.get_mongodb_collection(
                mongodb_database_name, mongodb_collection_name, w=w, wtimeout=wtimeout)
            if mongodb_collection is not None:
                doc.pop('_id', None)

                try:
                    result = mongodb_collection.insert_one(doc)
                    id = result.inserted_id
                except Exception as e:
                    self.log.error(e)

        return id

    def insert(self,
               mongodb_database_name: str,
               mongodb_collection_name: str,
               doc_list: List,
               update_existing_records: bool=True,
               w: int = 0,
               wtimeout: int = 60000) -> (InsertManyResult, BulkWriteResult):
        insert_results = None
        bulk_write_results = None

        if len(doc_list) > 0:
            mongodb_collection = self.get_mongodb_collection(mongodb_database_name,
                                                             mongodb_collection_name,
                                                             w=w,
                                                             wtimeout=wtimeout)
            if mongodb_collection is not None:
                docs_to_update, docs_to_insert = self.__filter_documents(
                    doc_list,
                    mongodb_collection,
                    update_existing_records=update_existing_records)

                if len(docs_to_insert) > 0:
                    try:
                        insert_results = mongodb_collection.insert_many(
                            docs_to_insert, ordered=False)
                    except Exception as e1:
                        self.log.error(e1)
                        try:
                            output_doc_list = []
                            for doc in docs_to_insert:
                                output_doc = None
                                if doc is not None:
                                    output_doc = {}
                                    if '_id' in doc and doc['_id'] is not None:
                                        output_doc['_id'] = str(doc['_id'])
                                    else:
                                        for key in doc:
                                            value = doc[key]
                                            if value is not None:
                                                value = str(value)
                                            output_doc[key] = value

                                output_doc_list.append(output_doc)

                            self.log.error(json.dumps(
                                output_doc_list, indent=True, sort_keys=True))
                        except Exception as e2:
                            self.log.error(e2)

                if len(docs_to_update) > 0:
                    to_be_updated = []

                    for doc in docs_to_update:
                        doc_id = doc["_id"]
                        try:
                            to_be_updated.append(
                                ReplaceOne({"_id": doc_id}, doc))
                        except Exception as e:
                            self.log.error(e)

                    try:
                        bulk_write_results = mongodb_collection.bulk_write(
                            to_be_updated)
                    except Exception as e:
                        self.log.error(e)

        return insert_results, bulk_write_results

    def udpate(self,
               mongodb_database_name: str,
               mongodb_collection_name: str,
               doc_list: List,
               w: int = 0,
               wtimeout: int = 60000):
        if len(doc_list) > 0:
            mongodb_collection = self.get_mongodb_collection(
                mongodb_database_name, mongodb_collection_name, w=w, wtimeout=wtimeout)
            if mongodb_collection is not None:
                docs_to_update, docs_to_insert = self.__filter_documents(
                    doc_list, mongodb_collection)

                # self.log.info("Collection: %s - No. of documents to update: %i, No. of documents to insert: %i",
                # mongodb_collection_name, len(docs_to_update),
                # len(docs_to_insert))

                if len(docs_to_insert) > 0:
                    try:
                        insert_result = mongodb_collection.insert_many(
                            docs_to_insert)
                    except Exception as e:
                        self.log.error(e)

                if len(docs_to_update) > 0:
                    to_be_updated = []

                    for doc in docs_to_update:
                        doc_id = doc["_id"]
                        to_be_updated.append(ReplaceOne({"_id": doc_id}, doc))

                    try:
                        update_result = mongodb_collection.bulk_write(
                            to_be_updated)
                    except Exception as e:
                        self.log.error(e)

    def update_one(self,
                   mongodb_database_name: str,
                   mongodb_collection_name: str,
                   filter: Dict,
                   update_condition: Dict,
                   w: int = 0,
                   wtimeout: int = 60000) -> UpdateResult:
        update_result = None

        if filter is not None and update_condition is not None:
            mongodb_collection = self.get_mongodb_collection(mongodb_database_name,
                                                             mongodb_collection_name,
                                                             w=w,
                                                             wtimeout=wtimeout)
            if mongodb_collection is not None:
                try:
                    update_result = mongodb_collection.update_one(
                        filter, update_condition)
                except Exception as e:
                    self.log.error(e)

        return update_result

    def find_one(self,
                 mongodb_database_name: str,
                 mongodb_collection_name: str,
                 filter: Dict,
                 projection: Dict=None) -> Dict:
        result = None

        mongodb_collection = self.get_mongodb_collection(
            mongodb_database_name, mongodb_collection_name)
        if mongodb_collection is not None:
            try:
                result = mongodb_collection.find_one(
                    filter, projection=projection)
            except Exception as e:
                self.log.error(e)

        return result

    def __filter_documents(self,
                           doc_list: List,
                           mongodb_collection: object,
                           update_existing_records=True) -> Tuple:
        if len(doc_list) > 0:
            docs_to_update = []
            docs_to_insert = []

            if mongodb_collection is not None:
                for doc in doc_list:
                    if doc is not None:
                        if '_id' in doc:
                            doc_id = doc["_id"]
                            if update_existing_records is True:
                                docs_to_update.append(doc)
                            else:
                                try:
                                    exist = mongodb_collection.find_one(
                                        {"_id": doc_id}, {'_id': 1})
                                    if exist is None:
                                        docs_to_insert.append(doc)
                                except Exception as e:
                                    self.log.error(e)
                        else:
                            docs_to_insert.append(doc)

            return docs_to_update, docs_to_insert
        else:
            return [], []