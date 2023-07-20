#!/usr/bin/env python3
""" nginx logs to mongo instance parser """

from pymongo import MongoClient


def temp_F():
    """ temp function to check the checker"""
    client = MongoClient()
    main = client.logs.nginx
    method_C = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    status = main.count_documents({"method": "GET", "path": "/status"})
    print(f"{main.estimated_document_count()} logs")
    print("Methods:")
    for i in method_C:
        check = main.count_documents({"method": i})
        print(f"\tmethod {i}: {check}")
    print(f"{status} status check")
    count = 0
    aggr = [{"$group": {"_id": '$ip', "c": {"$sum": 1}}}, {"$sort": {"c": -1}}]
    db = client.logs
    ip = {x["_id"]: x["c"] for x in db.nginx.aggregate(aggr)}
    print("IPs:")
    for key, value in ip.items():
        if count > 9:
            break
        count += 1
        print(f"\t{key}: {value}")


if __name__ == "__main__":
    temp_F()
