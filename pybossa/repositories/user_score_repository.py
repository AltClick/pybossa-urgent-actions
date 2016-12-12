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

from pybossa.repositories import Repository
from pybossa.model.user_score import UserScore
from sqlalchemy import text

class UserScoreRepository(Repository):

    # Methods for queries on UserScore objects
    def get(self, project_id, user_id):

        # Requesting the project score for an authenticated user
        if user_id is not None:
            sql = text('''
                    SELECT * FROM "user_score"
                    WHERE user_score.project_id = :project_id
                    AND user_score.user_id = :user_id
                ''')

            task_row_proxy = self.db.session.execute(sql, dict(project_id=project_id, user_id=user_id)).fetchone()
            return UserScore(task_row_proxy).score

        return -1

    def set(self, project_id, user_id):
        #TODO: Implement
        #IMPORTANT: Only set ONCE. Do not update row if it already exists.
        pass
