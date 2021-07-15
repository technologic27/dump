// MongoDB script

// Find the distinct set of values for a particular field in the Reddit comments JSON and
// the number of times each value has occurred.

function find_distinct_values( database_name, collection_name, field_name ) {
    var my_db = db.getSiblingDB(database_name); // same effect as "use database_name"

    output_collection_name = 'totals-aggregation-' + field_name ;
    my_db[ output_collection_name ].drop() ;

    var result = my_db.runCommand(
      { aggregate: collection_name,
        pipeline: [
          {$match : {}},
          {$group : {   _id:'$'+field_name,
                        count:{$sum:1}
                        }},
          {$project : {count: '$count'}},
          {$sort: {field_name: 1, 'count': 1}},
          {$out: output_collection_name} ],
        allowDiskUse: true
      }
    );

    return result ;
}

var database_name = 'redit_10000' ;
var collection_name = 'comments' ;
var field_names = [ 'id', 'parent_id', 'link_id', 'subreddit_id',
                    'subreddit',
                    'author', 'author_flair_text', 'author_flair_css_class',
                    'score', 'controversiality',
                    'gilded', 'edited', 'distinguished', 'stickied' ] ;

for (i = 0; i < field_names.length; i++) {
    print( "Getting distinct values for the field: " + field_names[i]) ;
    var result = find_distinct_values( database_name, collection_name, field_names[i] ) ;
    print( "  Result: " ) ;
    printjson( result ) ;

    var my_db = db.getSiblingDB(database_name); // same effect as "use database_name"
    var output_collection_name = 'totals-aggregation-' + field_names[i] ;
    var number_of_records = my_db.getCollection(output_collection_name).count() ;
    print( "  No. of records: " + number_of_records) ;

    print("_________________________________________") ;
}
