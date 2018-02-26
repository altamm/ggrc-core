# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""
add is external column to relationships table

Create Date: 2018-02-13 10:38:10.322322
"""
# disable Invalid constant name pylint warning for mandatory Alembic variables.
# pylint: disable=invalid-name

import datetime
from email.utils import parseaddr

import sqlalchemy as sa
from sqlalchemy.sql import text

from alembic import op

from ggrc import settings


_INSERT_EXTERNAL_APP_USER_SQL = u'''
  INSERT INTO people(`email`, `name`, `created_at`, `updated_at`)
    VALUES (:email, :name, :created_at, :updated_at)'''

_DELETE_EXTERNAL_APP_USER_SQL = u'''
  DELETE FROM people WHERE email = :email'''


# revision identifiers, used by Alembic.
revision = 'd1671a8dac7'
down_revision = '123734a16f69'


def upgrade():
  """Upgrade database schema and/or data, creating a new revision."""
  op.add_column(
      'relationships',
      sa.Column('is_external', sa.Boolean(), nullable=False, default=False))

  conn = op.get_bind()
  now = datetime.datetime.utcnow()
  name, email = parseaddr(settings.EXTERNAL_APP_USER)
  conn.execute(
      text(_INSERT_EXTERNAL_APP_USER_SQL),
      email=email, name=name, created_at=now, updated_at=now)


def downgrade():
  """Downgrade database schema and/or data back to the previous revision."""
  op.drop_column('relationships', 'is_external')

  _, email = parseaddr(settings.EXTERNAL_APP_USER)
  conn = op.get_bind()
  conn.execute(text(_DELETE_EXTERNAL_APP_USER_SQL), email=email)

