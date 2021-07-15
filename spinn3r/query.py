content_field = "main"
date_field = "date_found"
source_type_field = "source_publisher_type"
source_subtype_field = "source_publisher_subtype"
twitter_handle_field = "author_handle"
match_operator = "match_phrase"

default_fetch_size = 1000


def get_query(must_conditions, must_not_conditions, start_date_string, end_date_string, filter_term_conditions):
    """
    {
        "query": {
                "bool": {
                    "must": to_replace,
                    "filter" : [
                        {  "term": {"lang": "en"} },

                    ]
                }
            }
        }
    }
    """
    boolean_query = _form_bool_query(
        must_conditions, must_not_conditions, start_date_string, end_date_string, filter_term_conditions)
    query = {}
    query["query"] = boolean_query
    query["size"] = default_fetch_size

    return query


def _form_bool_query(must_conditions, must_not_conditions, start_date_string, end_date_string, filter_term_conditions):
    """
    Returns:
    {   "bool": {
            "must"  : [
                {"match": {"title": "Search"}},
                {"match": {"content": "Elasticsearch"}}
            ],
            "filter": [
                {"term": {"status": "published"}},
                {"range": {"publish_date": {"gte": "2015-01-01"}}}
            ]
        }
    }
    """

    boolean_query = {}
    if len(must_conditions) > 0:
        must_query = _form_match_queries(must_conditions)
        boolean_query["must"] = must_query

    if len(must_not_conditions) > 0:
        must_not_query = _form_match_queries(must_not_conditions)
        boolean_query["must_not"] = must_not_query

    if len(filter_term_conditions) > 0:
        filter_query = _form_filter_queries(
            start_date_string, end_date_string, filter_term_conditions)
        boolean_query["filter"] = filter_query

    query = {"bool": boolean_query}

    return query


def set_date_range(start_year, start_month, start_day, end_year, end_month, end_day):
    start_date_string = __form_elastic_basic_date_time_no_millis_format(
        start_year, start_month, start_day, 0, 0, 0)
    end_date_string = __form_elastic_basic_date_time_no_millis_format(
        end_year, end_month, end_day, 23, 59, 59)
    return start_date_string, end_date_string


def __form_elastic_basic_date_time_no_millis_format(year, month, day, hour, minute, second):
    result = "{}-{}-{}T{}:{}:{}Z".format(
        str(year).zfill(4),
        str(month).zfill(2),
        str(day).zfill(2),
        str(hour).zfill(2),
        str(minute).zfill(2),
        str(second).zfill(2))
    return result


def _form_date_time_range_query(start_date_string, end_date_string):
    _range = {}
    if start_date_string != 0:
        _range["gte"] = start_date_string
    if end_date_string != 0:
        _range["lte"] = end_date_string

    range_condition = {date_field: _range}

    query = {"range": range_condition}

    return query


def _form_match_queries(match_conditions):
    """
    Returns:
        [{"match": {"title":  "Search"}},{"match": {"content": "Elasticsearch" }}]
    """
    match_list = []
    if len(match_conditions) > 0:
        for field, condition in match_conditions:
            condition = {field: condition}
            query = {match_operator: condition}
            match_list.append(query)
    return match_list


def _form_filter_queries(start_date_string, end_date_string, filter_term_conditions):
    """
    Returns:
        [   {"term":  {"status": "published" }},
            {"range": {"publish_date": { "gte": "2015-01-01" }}} ]
    """
    terms_list = []
    if start_date_string != 0 and end_date_string != 0:
        date_time_query = _form_date_time_range_query(
            start_date_string, end_date_string)
        terms_list.append(date_time_query)

    if len(filter_term_conditions) > 0:
        for term_condition in filter_term_conditions:
            condition = {term_condition[0]: term_condition[1]}
            term_query = {"term": condition}
            terms_list.append(term_query)
    return terms_list
