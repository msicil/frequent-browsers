# Frequent Browsers

A simple GraphQL-Django-Python program to track frequent browsers to websites

## GraphQL Endpoint Setup

The main way to access and manipulate this program is through the GraphQL endpoint, or alternatively through the built in IDE GraphiQL.  Here are the quick steps to do that:

* Start up the pipenv shell and install dependencies (may need to use exit command to exit any existing shells):
```
$ pipenv shell
$ pipenv install
```
* Start up the python server in the root folder:
```
$ python manage.py runserver
```

* Go to localhost:8000/graphql

### Queries/Mutations

Here is a list of all graphql queries and mutations to interact with the backend:

Queries:
* people(id, firstName, lastName, allVisits(M2M Field to Sites))
* sites(id, url, visitors(M2M Field to People))
* frequentBrowsers(people(One2One Field to People),numSitesVisited)

Mutations:
* refreshFrequent() => This clears the frequentBrowers table and then reloads it with the 10 users with the most site visits
* createSite(id, url)
* createPeople(id, firstName, lastName)
* createVisit(personId, siteId, timeVisited(default = currentTime))
