# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: miha@reciprocitylabs.com
# Maintained By: miha@reciprocitylabs.com

"""Module for testing constant regex expressions."""

import re
from lib.constants import regex


def test_url_to_widget_info_regex():
  """Test regex for parsing the object id, object name and widget name from
  url."""
  urls = [
      ("https://grc-test.appspot.com/dashboard",
          "dashboard", "", ""),
      ("https://grc-test.appspot.com/dashboard#clause_widget",
          "dashboard", "", "clause_widget"),
      ("https://grc-test.appspot.com/clauses/90#/clause/90",
          "clauses", 90, "info_widget"),
      ("https://grc-test.appspot.com/clauses/90#",
          "clauses", 90, "info_widget"),
      ("https://grc-test.appspot.com/clauses/90",
          "clauses", 90, "info_widget"),
      ("https://grc-test.appspot.com/clauses/90#control_widget",
          "clauses", 90, "control_widget"),
      ("https://grc-test.appspot.com/clauses/90#info_widget",
          "clauses", 90, "info_widget"),
      ("https://grc-test.appspot.com/workflows/107",
          "workflows", 107, "info_widget"),
      ("https://grc-test.appspot.com/workflows/107#task_group_widget/"
          "task_group/122", "workflows", 107, "task_group_widget"),
      ("https://grc-test.appspot.com/workflows/107#info_widget/workflow/107",
          "workflows", 107, "info_widget"),
      ("https://grc-test.appspot.com/workflows/107#/workflow/107",
          "workflows", 107, "info_widget"),
  ]

  for url, expected_object_name, expected_id, expected_widget_name in urls:
    object_name, object_id, widget_name = re.search(
        regex.URL_WIDGET_INFO, url).groups()

    if object_id:
      object_id = int(object_id)
      widget_name = widget_name or "info_widget"

    assert object_id == expected_id
    assert widget_name == expected_widget_name
    assert object_name == expected_object_name
