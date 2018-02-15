# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Request handlers for external applications API."""

import logging
import json

from flask import current_app
from flask import request

from ggrc import db
from ggrc import models
from ggrc.utils import GrcEncoder


logger = logging.getLogger()


def _get_object(src_object_type, object_id):
  """Returns object by object type name and id.

  Args:
    src_object_type: A string unique name of object type database model.
    object_id: An integer object unique identifier in scope of object type.

  Returns:
    An instance of database model of given object type or None if no object
    found.
  """
  model = models.inflector.get_model(src_object_type)
  return db.session.query(model).filter(model.id == object_id).first()


def _build_json_response(params_dict, status_code):
  """Builds json response for given parameters dict and HTTP status code.

  Args:
    params_dict: A dict with response parameters.
    status_code: An integer HTTP status code.

  Return:
    An instance of flask response.
  """
  return current_app.make_response((
      json.dumps(params_dict, cls=GrcEncoder),
      status_code,
      [('Content-Type', 'application/json')],
  ))


def _build_object_not_found_response(object_type, object_id):
  """Builds object not found response.

  Args:
    object_type: A string unique name of object type database model.
    object_id: An integer object unique identifier in scope of object type.

  Returns:
    An instance of flask response for object not found error.
  """
  return _build_json_response(
      {'message': '%s-%d does not exist.' % (object_type, object_id)}, 404)


def _build_invalid_object_type_response(object_type):
  """Builds invalid object type response.

  Args:
    object_type: A string unique name of object type database model.

  Returns:
    An instance of flask response for invalid object type error.
  """
  return _build_json_response(
      {'message': 'Map %s is not allowed for external app.' % object_type}, 400)


# TODO (altamm): Move to config.
_MAP_ALLOWED_OBJECT_TYPES = ('Product', 'System', 'Process')
def _mapping_request(func):
  """Decorator for parsing and initial processing of mapping request."""

  def wrapper():
    """Parses mapping request and retrieves objects to be mapped/unmapped.

    Wrapped function must have only src_object and dst_object arguments.
    """
    # Parse request.
    request_dict = json.loads(request.data)
    src_object_id = request_dict.get('src_object_id')
    src_object_type = request_dict.get('src_object_type')

    dst_object_id = request_dict.get('dst_object_id')
    dst_object_type = request_dict.get('dst_object_type')

    # Validate object types.
    if src_object_type not in _MAP_ALLOWED_OBJECT_TYPES:
      return _build_invalid_object_type_response(src_object_type)

    if dst_object_type not in _MAP_ALLOWED_OBJECT_TYPES:
      return _build_invalid_object_type_response(dst_object_type)

    # Get objects from database.
    src_object = _get_object(src_object_type, src_object_id)
    if not src_object:
      return _build_object_not_found_response(src_object_type, src_object_id)

    dst_object = _get_object(dst_object_type, dst_object_id)
    if not dst_object:
      return _build_object_not_found_response(dst_object_type, dst_object_id)

    return func(src_object, dst_object)

  return wrapper


@_mapping_request
def map_objects(src_object, dst_object):
  """Request handler to create mapping between two objects from external app.

  If mapping already exists - empty operation.

  Args:
    src_object: An instance of source object database model to map.
    dst_object: An instance of destination object database model to map.

  Returns:
    An instance of flask response with unmap operation result.
  """
  relationship = models.Relationship.find_related(src_object, dst_object)
  if relationship:
    logger.info(
        'External Map: Relationship between %s-%d and %s-%d already '
        'exist. Skipping.' % (
            src_object.type, src_object.id, dst_object.type, dst_object.id))
    return _build_json_response({}, 200)

  db.session.add(models.Relationship(
      source_id=src_object.id,
      source_type=src_object.type,
      destination_id=dst_object.id,
      destination_type=dst_object.type,
      is_external=True,
      source=src_object,
      destination=dst_object))
  db.session.commit()

  logger.info(
      'External Map: External relationship between %s-%d and %s-%d was '
      'created.' % (
          src_object.type, src_object.id, dst_object.type, dst_object.id))

  return _build_json_response({}, 200)


@_mapping_request
def unmap_objects(src_object, dst_object):
  """Request handler to delete mapping between two objects from external app.

  If mapping doesn't exist or existing mapping was created manually - empty
  operation. Unmap from external source can be done only on relationships
  marked as external.

  Args:
    src_object: An instance of source object database model to unmap.
    dst_object: An instance of destination object database model to unmap.

  Returns:
    An instance of flask response with unmap operation result.
  """
  relationship = models.Relationship.find_related(src_object, dst_object)

  if not relationship:
    logger.info(
        'External Unmap: Relationship between %s-%d and %s-%d already '
        'does not exist. Skipping.' % (
            src_object.type, src_object.id, dst_object.type, dst_object.id))
    return _build_json_response({}, 200)

  if not relationship.is_external:
    logger.info(
        'External Unmap: Relationship between %s-%d and %s-%d was created '
        'manually and can not be deleted by external app. Skipping.' % (
            src_object.type, src_object.id, dst_object.type, dst_object.id))
    return _build_json_response({}, 200)

  db.session.delete(relationship)
  db.session.commit()

  logger.info(
      'External Unamp: External relationship between %s-%d and %s-%d was'
      'deleted.' % (
          src_object.type, src_object.id, dst_object.type, dst_object.id))

  return _build_json_response({}, 200)
