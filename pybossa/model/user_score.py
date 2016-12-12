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

from sqlalchemy import Integer, Text
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.orm import relationship, backref
from flask.ext.login import UserMixin
from pybossa.core import db
from pybossa.model import DomainObject, make_timestamp
from pybossa.model.project import Project
from pybossa.model.user import User


class UserScore(db.Model, DomainObject, UserMixin):
    '''The project trial scores for registered user of the PyBossa system'''

    __tablename__ = 'user_score'

    #: Unique identifier
    id = Column(Integer, primary_key=True)

    #: User.ID that this score is associated with.
    user_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'), nullable=False)

    #: Project.ID that this score is associated with.
    project_id = Column(Integer, ForeignKey('project.id', ondelete='CASCADE'), nullable=False)

    #: UTC timestamp of the user when it's created.
    created = Column(Text, default=make_timestamp, nullable=False)

    #: Score value
    score = Column(Integer, nullable=False)

    ## Relationships
    #users = relationship(User, backref='user')
    #projects = relationship(Project, backref='owner')

