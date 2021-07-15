fields_to_ignore_level_one = ("_id", "_index", "_type", "_score")

fields_to_ignore_level_two = ('bucket', 'sequence', 'sequence_range', 'detection_method', 'duplicates_count', 'description',
                              'extract_checksum', 'extract_length', 'hashcode', 'identifier', 'index_method', 'image_height',
                              'image_width', 'links', 'main_checksum', 'main_length', 'metadata_score', 'permalink_redirect',
                              'permalink_redirect_domain', 'permalink_redirect_site', 'sequence', 'sequence_range', 'shared_type',
                              'source_assigned_tags', 'source_publisher_type', 'source_favicon_height', 'source_favicon_width',
                              'source_image_height', 'source_image_width', 'source_parsed_posts', 'source_parsed_posts_max',
                              'source_setting_author_policy', 'source_setting_minimum_content_metadata_score', 'source_user_interactions',
                              'source_content_checksum', 'source_content_length', 'source_description', 'source_hashcode',
                              'source_http_status', 'source_last_posted', 'source_last_published', 'source_last_updated',
                              'source_link', 'source_next_update', 'source_resource', 'source_setting_index_strategy',
                              'source_setting_update_strategy', 'source_update_interval', 'version')


def format_record(one_record):
    if "_source" in one_record.keys():
        for field_to_igonore in fields_to_ignore_level_two:
            one_record["_source"].pop(field_to_igonore, None)
    for field_to_ignore in fields_to_ignore_level_one:
        one_record.pop(field_to_ignore, None)
    return one_record
