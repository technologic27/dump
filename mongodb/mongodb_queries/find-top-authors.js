db.runCommand(
  { aggregate: "totals-aggregation-author",
    pipeline: [
      {$match : {}},
      {$sort: {'count': -1, 'author': 1}},
    allowDiskUse: true
  }
);