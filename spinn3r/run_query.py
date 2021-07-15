# filter terms include: twitter_handle, source_type, source_subtype
# range queries include: date_time
# add search terms, match term, not match term

from query import set_date_range, _form_date_time_range_query, _form_filter_queries, _form_bool_query, get_query
from response import search_and_write

content_field = "main"
date_field = "date_found"
source_type_field = "source_publisher_type"
source_subtype_field = "source_publisher_subtype"
twitter_handle_field = "author_handle"
match_operator = "match_phrase"


must_conditions = [("main", "DDoS")]
must_not_conditions = []
filter_term_conditions = [("lang", "en")]

domains = ["threatpost.com", "securityaffairs.co", "bleepingcomputer.com",
           "thehackernews.com", "securityweek.com", "hackread.com"]

# filter_term_conditions ("source_publisher_subtype", "twitter")

# 1. filter terms
# 1a. source_type
# 1b. date_time
# 1c. lang

start_year = 2017
start_month = 1
start_day = 1
end_year = 2017
end_month = 6
end_day = 1

start_date_string, end_date_string = set_date_range(
    start_year, start_month, start_day, end_year, end_month, end_day)

final_query = get_query(
    must_conditions, must_not_conditions, 0, 0, filter_term_conditions)

search_and_write(final_query)
