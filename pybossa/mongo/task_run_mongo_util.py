from flask import current_app
from pybossa.mongo.base_mongo_util import BaseMongoUtil

class TaskRunMongoUtil(BaseMongoUtil):
    def __init__(self):
        super(TaskRunMongoUtil, self).__init__('taskruns')

    def consolidate_redundancy(self, project_short_name=None, ip=None):
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
                    "zoom": "$info.zoom",
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
                    "id": "$_id.tile_id",
                    "zoom": "$_id.zoom"
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
                    "y": "$tiles.y",
                    "zoom": "$_id.zoom"
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
                    "task_id": "$_id.task_id",
                    "zoom": "$_id.zoom"
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
                "zoom": "$_id.zoom",
                "tiles": "$tiles"
            }
        }

        if project_short_name:
            match["$match"]["project_short_name"] = project_short_name

        if ip:
            match["$match"]["user_ip"] = ip.replace('"', "")

        aggregation = [unwind_taskrun, match, group_1, sort_1, group_2, unwind_tiles, group_3, sort_2, group_4, project]
        return current_app.mongo.db[self.collection_name].aggregate(aggregation)

    def get_tasks_count(self, user=None, ip=None, project_short_name=None):
        match = {
            "$match": {}
        }

        if project_short_name:
            match["$match"]["project_short_name"] = project_short_name

        group = {
            "$group": {
                "_id": {
                    "zoom": "$info.zoom"
                },
                "count": {
                    "$sum": 1
                }
            }
        }

        project = {
            "$project": {
                "_id": 0,
                "zoom": "$_id.zoom",
                "counts": "$count"
            }
        }

        if user:
            match["$match"]["username"] = user

        if ip:
            match["$match"]["user_ip"] = ip.replace('"', "")

        aggregation = [match, group, project]
        return current_app.mongo.db[self.collection_name].aggregate(aggregation)

    def validate_human_presence(self, redundancy, project_short_name, task_id=None):
        if project_short_name and task_id:
            data = self.consolidate_redundancy(project_short_name, task_id)
        elif project_short_name:
            data = self.consolidate_redundancy(project_short_name)
        elif task_id:
            data = self.consolidate_redundancy(task_id)
        else:
            data = self.consolidate_redundancy()

        results = []
        for item in data:
            if 'tiles' in item:
                redundancy_tile = {}
                tiles = item['tiles']
                for tile in tiles:
                    redundancy_tile['zoom'] = item['zoom']
                    redundancy_tile['task_id'] = item['task_id']
                    if (tile['true'] >= redundancy and tile['true'] > tile['false']):
                        redundancy_tile['x'] = int(tile['x'])
                        redundancy_tile['y'] = int(tile['y'])
                        redundancy_tile['true'] = tile['true']
                        results.append(redundancy_tile)
                        redundancy_tile = {}
        return results
        