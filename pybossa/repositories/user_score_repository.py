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
from pybossa.exc import WrongObjectError, DBIntegrityError
from sqlalchemy.exc import IntegrityError
from flask.ext.login import current_user
from werkzeug.exceptions import MethodNotAllowed, Unauthorized

class UserScoreRepository(Repository):

    # Methods for queries on UserScore objects
    def get(self, project_id, user_id):

        # Requesting the project score for an authenticated user
        if user_id is not None:
            sql = text('''
                    SELECT score FROM "user_score"
                    WHERE user_score.project_id = :project_id
                    AND user_score.user_id = :user_id
                ''')

            row_proxy = self.db.session.execute(sql, dict(project_id=project_id, user_id=user_id)).fetchone()

            # If no record exists, return -1
            if row_proxy is None:
                return -1

            else:
                return int(row_proxy[0])

        return -1

    def save(self, UserScore):
        project_id = getattr(UserScore, 'project_id')
        if current_user.is_authenticated():
            if not self._check_for_score(project_id):
                self._validate_can_be('saved', UserScore)
                try:
                    self.db.session.add(UserScore)
                    self.db.session.commit()
                except IntegrityError as e:
                    self.db.session.rollback()
                    raise DBIntegrityError(e)
            else:
                return False
        else:
            return Unauthorized()

    def _validate_can_be(self, action, user):
        if not isinstance(user, UserScore):
            name = user.__class__.__name__
            msg = '%s cannot be %s by %s' % (name, action, self.__class__.__name__)
            raise WrongObjectError(msg)

    def _check_for_score(self, project_id):
        sql = text('''
                           SELECT * FROM "user_score"
                           WHERE user_score.user_id = :user_id
                           AND user_score.project_id = :project_id
                       ''')
        sql_result = self.db.session.execute(sql, dict(user_id=current_user.id, project_id=project_id))
        user_score_result= sql_result.fetchall()
        if len(user_score_result):
            return True
        else:
            return False
