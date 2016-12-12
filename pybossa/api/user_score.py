# -*- coding: utf8 -*-
# This file is part of PyBossa.
#
# Copyright (C) 2015 SciFabric LTD.
#
# PyBossa is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PyBossa is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with PyBossa.  If not, see <http://www.gnu.org/licenses/>.
"""
PyBossa api module for domain object APP via an API.

This package adds GET, POST, PUT and DELETE methods for:
    * projects,

"""
from flask import redirect, url_for, request, abort
from flask.ext.login import current_user
from api_base import APIBase
from pybossa.model.user_score import UserScore
from pybossa.model.project import Project
from pybossa.core import user_score_repo
from werkzeug.exceptions import MethodNotAllowed



class UserScoreAPI(APIBase):

    """
    Class for the domain object Project.

    It refreshes automatically the cache, and updates the project properly.

    """

    __class__ = UserScore

    def get(self, oid):
        raise MethodNotAllowed(valid_methods=['POST'])

    def post(self):
        #TODO: Implement
        return None

    def delete(self, oid):
        raise MethodNotAllowed(valid_methods=['POST'])

    def put(self, oid):
        raise MethodNotAllowed(valid_methods=['POST'])

