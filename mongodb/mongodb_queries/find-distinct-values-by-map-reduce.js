// MongoDB script

// Find the distinct set of values for a particular field in the Reddit comments JSON and
// the number of times each value has occurred by using the MongoDB map-reduce framework.

map = function() {
    if (!this.author) return;
    var author = this.author;
    emit(author, { count: 1 } );
};

reduce = function(key, values) {
    var result = { count: 0 } ;
    values.forEach( function(v) {
        result.count += v.count ;
    });
    return result;
};

db.totals.drop();
db.comments.mapReduce(map, reduce, {query: {}, out: 'totals'}) ;
