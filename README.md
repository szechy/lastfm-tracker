This is a collection of scripts to perform analytics of my Last.fm listening data, using the [PyLast](https://github.com/pylast/pylast) library for interfacing with the Last.fm API using Python.

Python libraries/dependencies:

[PyLast](https://github.com/pylast/pylast)

time

datetime

[pymongo](http://api.mongodb.org/python/current/index.html)

Installation instructions for Mongo:

* Install [MongoDB](https://www.mongodb.org/) 
* Start the `mongod` daemon
* Create a collection:

```
$	mongo
$	db.createCollection("tracks", {autoIndexId: true})

```

* Run ``