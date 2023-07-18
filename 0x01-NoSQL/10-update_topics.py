#!/usr/bin/env python3
"""
Module that contains the function update_topics()
"""
import pymongo


def update_topics(mongo_collection, name, topics):
    """

    Args:
       mongo_collection: a pymongo collection
       name(string): school name to update
       topics(list of strings): list of topics approached in the school

    Returns:
         Nothing
    """
    return mongo_collection.update_many({
            "name": name
        },
        {
            "$set": {
                "topics": topics
            }
        })
