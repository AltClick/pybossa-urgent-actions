import pprint

from flask import current_app
import datetime


class BaseMongoUtil(object):
    def __init__(self, collection_name):
        self.collection_name = collection_name

    def insert_one(self, doc):
        doc['timestamp'] = datetime.datetime.now()
        current_app.mongo.db[self.collection_name].insert_one(doc)

    def get_tile_results(self, project_id=None, task_id=None):
        unwind_taskrun = {
            "$unwind": "$info.taskrun"
        }

        unwind_tiles = {
            "$unwind": "$tiles"
        }
        match = {
            "$match": {}
        }
        group_1 = {
            "$group": {
                "_id": {
                    "task_id": "$task_id",
                    "tile_id": "$info.taskrun.id",
                    "x": "$info.taskrun.x",
                    "y": "$info.taskrun.y",
                    "true": {
                        "$cond": [
                            {
                                "$eq": [
                                    "$info.taskrun.hp",
                                    True
                                ]
                            },
                            1,
                            0
                        ]
                    },
                    "false": {
                        "$cond": [
                            {
                                "$eq": [
                                    "$info.taskrun.hp",
                                    False
                                ]
                            },
                            1,
                            0
                        ]
                    }
                },
                "count": {
                    "$sum": 1
                }
            }
        }

        group_2 = {
            "$group": {
                "_id": {
                    "task_id": "$_id.task_id",
                    "id": "$_id.tile_id"
                },
                "tiles": {
                    "$push": {
                        "id": "$_id.tile_id",
                        "true": {
                            "$multiply": ["$count", "$_id.true"]
                        },
                        "false": {
                            "$multiply": ["$count", "$_id.false"]
                        },
                        "x": "$_id.x",
                        "y": "$_id.y"
                    }
                }
            }
        }

        group_3 = {
            "$group": {
                "_id": {
                    "task_id": "$_id.task_id",
                    "tile_id": "$tiles.id",
                    "x": "$tiles.x",
                    "y": "$tiles.y"
                },
                "true": {
                    "$sum": "$tiles.true"
                },
                "false": {
                    "$sum": "$tiles.false"
                }
            }
        }

        group_4 = {
            "$group": {
                "_id": {
                    "task_id": "$_id.task_id"
                },
                "tiles": {
                    "$push": {
                        "id": "$_id.tile_id",
                        "true": "$true",
                        "false": "$false",
                        "x": "$_id.x",
                        "y": "$_id.y"
                    }
                }
            }
        }

        sort_1 = {
            "$sort": {
                "_id.tile_id": 1
            }
        }

        sort_2 = {
            "$sort": {
                "_id.task_id": 1,
                "_id.tile_id": 1
            }
        }

        project = {
            "$project": {
                "_id": 0,
                "task_id": "$_id.task_id",
                "tiles": "$tiles"
            }
        }

        if project_id:
            match["$match"]["project_id"] = project_id

        if task_id:
            match["$match"]["task_id"] = task_id

        aggregation = [unwind_taskrun, match, group_1, sort_1, group_2, unwind_tiles, group_3, sort_2, group_4, project]
        return current_app.mongo.db[self.collection_name].aggregate(aggregation)
