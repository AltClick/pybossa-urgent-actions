import json

from bson import json_util
from flask import request
from flask.ext.login import current_user

from pybossa.extensions import task_repo
from pybossa.mongo import task_run_mongo
import math


class AreaCalculator():
    # CONSTANTS
    GROUND_RES_PER_ZOOM = {
        "10": 152.8741,
        "11": 76.4370,
        "12": 38.2185,
        "13": 19.1093,
        "14": 9.5546,
        "15": 4.7773,
        "16": 2.3887,
        "17": 1.1943,
        "18": 0.5972
    }
    TILES_PER_TASK = 12
    TILE_PIXELS = 256

    # calculates the tile length in meters.
    def calculate_tile_edge_length_meters(self, zoom_level):
        return self.GROUND_RES_PER_ZOOM[zoom_level] * self.TILE_PIXELS

    def calculate_tile_area_meters_sq(self, zoom_level):
        return math.pow(self.calculate_tile_edge_length_meters(zoom_level), 2)

    def calculate_task_area_meters_sq(self, zoom_level):
        return self.calculate_tile_area_meters_sq(zoom_level) * self.TILES_PER_TASK

    def calculate_task_area_km_sq(self, zoom_level):
        return self.calculate_task_area_meters_sq(zoom_level) / 1000000

    def get_square_km_all_volunteers(self, project_short_name, redundancy):
        results = task_run_mongo.get_tasks_count()
        json_results = json.loads(json_util.dumps(results))
        sq_km_decoded = {
            "all_volunteers": 0,
            "current_user": 0
        }
        if len(json_results) > 1:
            pass
        else:
            if len(json_results) != 0:
                zoom = json_results[0]['zoom']
                counts = json_results[0]['counts']
                sq_km_decoded["all_volunteers"] = self.calculate_task_area_km_sq(zoom) * (counts / redundancy)
                if current_user.is_authenticated():
                    sq_km_decoded["current_user"] = self.get_current_user_square_km_decoded(True, project_short_name, redundancy)
                else:
                    sq_km_decoded["current_user"] = self.get_current_user_square_km_decoded(False, project_short_name, redundancy)

        return json_util.dumps(sq_km_decoded)

    @staticmethod
    def get_authenticated_user_results(project_short_name):
        return task_run_mongo.get_tasks_count(user=current_user.name, project_short_name=project_short_name)

    @staticmethod
    def get_anonymous_user_results(project_short_name):
        ip_addr = json_util.dumps(request.remote_addr)
        return task_run_mongo.get_tasks_count(ip=ip_addr, project_short_name=project_short_name)

    def get_current_user_square_km_decoded(self, is_authenticated, project_short_name, redundancy):
        if is_authenticated:
            results_user = self.get_authenticated_user_results(project_short_name)
        else:
            results_user = self.get_anonymous_user_results(project_short_name)
        json_results_user = json.loads(json_util.dumps(results_user))
        if len(json_results_user) > 0:
            zoom_user = json_results_user[0]['zoom']
            counts_user = json_results_user[0]['counts']
            return self.calculate_task_area_km_sq(zoom_user) * (counts_user / redundancy)
        else:
            return 0
