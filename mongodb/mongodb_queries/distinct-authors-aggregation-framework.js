// MongoDB script
// Find the distinct set of values for a particular field in the Reddit comments JSON and
// the number of times each value has occurred.

db.runCommand(
  { aggregate: "comments",
    pipeline: [
      {$match : {}},
      {$group : {_id:'$author',count:{$sum:1}}},
      {$project : {author: '$_id', count: '$count'}},
      {$sort: {'author': 1, 'count': 1}},
      {$out: 'totals-aggregation'} ],
    allowDiskUse: true
  }
);
