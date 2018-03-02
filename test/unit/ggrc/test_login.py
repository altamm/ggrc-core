# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

import mock
import unittest

from ggrc import login


class TestLoginFunctions(unittest.TestCase):

  @mock.patch('ggrc.settings.EXTERNAL_APP_USER', None)
  def test_is_external_app_user_no_external_user(self):
    self.assertFalse(login.is_external_app_user())

  @mock.patch('ggrc.settings.EXTERNAL_APP_USER', 'External App <>')
  def test_is_external_app_user_no_external_user_email(self):
    self.assertFalse(login.is_external_app_user())

  @mock.patch('ggrc.settings.EXTERNAL_APP_USER',
              'External App <external_app@example.com>')
  @mock.patch('ggrc.login.get_current_user')
  def test_is_external_app_user_no_logged_in_user(self, current_user_mock):
    current_user_mock.return_value = None
    self.assertFalse(login.is_external_app_user())
    current_user_mock.assert_called_once_with()

  @mock.patch('ggrc.settings.EXTERNAL_APP_USER',
              'External App <external_app@example.com>')
  @mock.patch('ggrc.login.get_current_user')
  def test_is_external_app_user_anonymous_user(self, current_user_mock):
    user_mock = mock.MagicMock()
    user_mock.is_anonymous.return_value = True
    current_user_mock.return_value = user_mock
    self.assertFalse(login.is_external_app_user())
    current_user_mock.assert_called_once_with()
    user_mock.is_anonymous.assert_called_once_with()

  @mock.patch('ggrc.settings.EXTERNAL_APP_USER',
              'External App <external_app@example.com>')
  @mock.patch('ggrc.login.get_current_user')
  def test_is_external_app_user_not_external_user(self, current_user_mock):
    user_mock = mock.MagicMock()
    user_mock.email = 'user@example.com'
    user_mock.is_anonymous.return_value = False
    current_user_mock.return_value = user_mock
    self.assertFalse(login.is_external_app_user())
    current_user_mock.assert_called_once_with()
    user_mock.is_anonymous.assert_called_once_with()

  @mock.patch('ggrc.settings.EXTERNAL_APP_USER',
              'External App <external_app@example.com>')
  @mock.patch('ggrc.login.get_current_user')
  def test_is_external_app_user_external_user(self, current_user_mock):
    user_mock = mock.MagicMock()
    user_mock.email = 'external_app@example.com'
    user_mock.is_anonymous.return_value = False
    current_user_mock.return_value = user_mock
    self.assertTrue(login.is_external_app_user())
    current_user_mock.assert_called_once_with()
    user_mock.is_anonymous.assert_called_once_with()
