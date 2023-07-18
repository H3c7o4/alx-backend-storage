#!/usr/bin/env python3
"""
Module that contains the function insert_school
"""
import pymongo


def insert_school(mongo_collection, **kwargs):
    """

    Args:
       mongo_collection: pymongo collection object
       **kwargs: object to insert in the collection

    Returns: the new _id
    """
    data = mongo_collection.insert_one(kwargs)
    return data.inserted_id
