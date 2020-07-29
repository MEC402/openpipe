# pip install sparqlwrapper
# https://rdflib.github.io/sparqlwrapper/

import sys
from SPARQLWrapper import SPARQLWrapper, JSON

endpoint_url = "https://query.wikidata.org/sparql"

query = """#Periods of Japanese history and what they were named after
SELECT ?era ?eraLabel (YEAR(?start_time) AS ?start) (YEAR(?end_time) AS ?end) ?namedDescription ?country ?countryLabel WHERE {
  ?era wdt:P31 wd:Q11514315;
    wdt:P580 ?start_time.
  MINUS { ?era (wdt:P2348/wdt:P361) wd:Q130436. }
  OPTIONAL { ?era wdt:P582 ?end_time. }
  OPTIONAL { ?era wdt:P17 ?country. }
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }

}
ORDER BY (?start) DESC (?end)"""


def get_results(endpoint_url, query):
    user_agent = "WDQS-example Python/%s.%s" % (sys.version_info[0], sys.version_info[1])
    # TODO adjust user agent; see https://w.wiki/CX6
    sparql = SPARQLWrapper(endpoint_url, agent=user_agent)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()


results = get_results(endpoint_url, query)

for result in results["results"]["bindings"]:
    print(result)