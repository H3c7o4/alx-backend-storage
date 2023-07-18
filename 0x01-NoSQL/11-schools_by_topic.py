#!/usr/bin/env python3
"""
Module that contains the function schools_by_topic(mongo_collection, topic)
"""
import pymongo


def schools_by_topic(mongo_collection, topic):
    """

    Args:
       mongo_collection: pymongo collection object
       topic(string): topic searched

    Returns:
         the list of school having a specific topic
    """
    return list(mongo_collection.find({"topic": {"$in": [topic]}}))
