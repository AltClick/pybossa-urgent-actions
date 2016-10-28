import json

from bson import json_util
from flask import request
from flask.ext.login import current_user

from pybossa.mongo import task_run_mongo
import math


class AreaCalculator():
    # CONSTANTS
    GROUND_RES_PER_ZOOM = {
        10: 152.8741,
        11: 76.4370,
        12: 38.2185,
        13: 19.1093,
        14: 9.5546,
        15: 4.7773,
        16: 2.3887,
        17: 1.1943,
        18: 0.5972
    }
    TILES_PER_TASK = 12
    TILE_PIXELS = 256
    ZOOM = 18

    # calculates the tile length in meters.
    def calculate_tile_edge_length_meters(self, zoom_level):
        return self.GROUND_RES_PER_ZOOM[zoom_level] * self.TILE_PIXELS

    def calculate_tile_area_meters_sq(self, zoom_level):
        return math.pow(self.calculate_tile_edge_length_meters(zoom_level), 2)

    def calculate_task_area_meters_sq(self, zoom_level):
        return self.calculate_tile_area_meters_sq(zoom_level) * self.TILES_PER_TASK

    def calculate_task_area_km_sq(self, zoom_level):
        return self.calculate_task_area_meters_sq(zoom_level) / 1000000

    def get_square_km_all_volunteers(self, project_short_name):
        all_volunteers_docs = 0
        current_user_docs = 0
        sq_km_decoded = {
            "all_volunteers": 0,
            "current_user": 0
        }
        if current_user.is_authenticated():
            results = self.get_task_count(project_short_name=project_short_name, user=current_user.name)
        else:
            ip_addr = json_util.dumps(request.remote_addr)
            results = self.get_task_count(project_short_name=project_short_name, ip=ip_addr)

        json_results = json.loads(json_util.dumps(results))

        for item in json_results:
            if item["_id"] == "current_user":
                current_user_docs = item["count"]
            if item["_id"] == "all_volunteers":
                all_volunteers_docs = item["count"]

        all_volunteers_docs += current_user_docs

        sq_km_decoded["current_user"] = self.calculate_task_area_km_sq(self.ZOOM) * current_user_docs
        sq_km_decoded["all_volunteers"] = self.calculate_task_area_km_sq(self.ZOOM) * all_volunteers_docs
        return json_util.dumps(sq_km_decoded)

    def get_task_count(self, project_short_name=None, user=None, ip=None):
        result = task_run_mongo.get_tasks_count(project_short_name=project_short_name, user=user, ip=ip)
        return result
