import json

from bson import json_util
from flask import request
from flask.ext.login import current_user

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

    # calculates the tile length in kilometers.
    def calculate_tile_edge_length_km(self, zoom_level):
        return self.calculate_tile_edge_length_meters(zoom_level) / 1000

    def calculate_tile_area_meters_sq(self, zoom_level):
        return math.pow(self.calculate_tile_edge_length_meters(zoom_level), 2)

    def calculate_tile_area_km_sq(self, zoom_level):
        return self.calculate_tile_area_meters_sq(zoom_level) / 1000

    def calculate_task_area_meters_sq(self, zoom_level):
        return self.calculate_tile_area_meters_sq(zoom_level) * 12

    def calculate_task_area_km_sq(self, zoom_level):
        return (self.calculate_tile_area_km_sq(zoom_level) / 1000) * 12

    def get_square_km_all_volunteers(self):
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
                sq_km_decoded["all_volunteers"] = self.calculate_task_area_km_sq(zoom) * counts
                if current_user.is_authenticated():
                    sq_km_decoded["current_user"] = self.get_current_user_square_km_decoded(True)
                else:
                    sq_km_decoded["current_user"] = self.get_current_user_square_km_decoded(False)

        return json_util.dumps(sq_km_decoded)

    @staticmethod
    def get_authenticated_user_results():
        return task_run_mongo.get_tasks_count(user=current_user.name)

    @staticmethod
    def get_anonymous_user_results():
        ip_addr = json_util.dumps(request.remote_addr)
        return task_run_mongo.get_tasks_count(ip=ip_addr)

    def get_current_user_square_km_decoded(self, is_authenticated):
        if is_authenticated:
            results_user = self.get_authenticated_user_results()
        else:
            results_user = self.get_anonymous_user_results()
        json_results_user = json.loads(json_util.dumps(results_user))
        if len(json_results_user) > 0:
            zoom_user = json_results_user[0]['zoom']
            counts_user = json_results_user[0]['counts']
            return self.calculate_task_area_km_sq(zoom_user) * counts_user
        else:
            return 0
