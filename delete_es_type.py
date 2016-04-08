#!/bin/python
import elasticsearch
import sys, getopt

def main(argv):
   number = 100
   search = {
                "query": {
                    "match_all": {}
                }
            }
   try:
      opts, args = getopt.getopt(argv,"hs:n:",["search=","number="])
   except getopt.GetoptError:
      print 'delete_from_elasticsearch.py -s <search_expression> -n <number_per_shard>'
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print 'delete_from_elasticsearch.py -s <search_expression> -n <number_per_shard>'
         sys.exit()
      elif opt in ("-s", "--search"):
         search = arg
      elif opt in ("-n", "--number"):
         number = arg
   print 'I will search for "', search
   print 'I will delete these in batches of "', number
   delete_docs(search, number)

def delete_docs(search, number):

  # Setup elasticsearch connection.
  es = elasticsearch.Elasticsearch()

  # Start the initial search.
  hits=es.search(
    body=search,
    index="article",
    fields="_id",
    size=number,
    scroll='5m',
    doc_type='wikipedia'
  )

  print hits

  # We have results initialize the bulk variable.
  bulk = ""

  # Remove the variables.
  for result in hits['hits']['hits']:
      print result
      bulk = bulk + '{ "delete" : { "_index" : "' + str(result['_index']) + '", "_type" : "wikipedia", "_id" : "' + str(result['_id']) + '" } }\n'
      #    print "Items left " + str(scroll['hits']['total']) + ' deleting ' + str(bulk.count('delete')) + ' items.'
      #    print bulk
      es.bulk( body=bulk )


if __name__ == "__main__":
   main(sys.argv[1:])
