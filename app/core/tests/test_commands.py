"""
Test custom Django management commands
"""

from unittest.mock import patch

from psycopg2 import OperationalError as psycopg2Error

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase


@patch("core.management.commands.wait_for_db.Command.check")
class CommandTests(SimpleTestCase):
    """
    Test commands.
    """
    def test_wait_for_db_ready(self, patched_check: patch):
        """Test waiting for database if database ready"""
        patched_check.return_value = True
        # checks to see if the command
        # that we are testing can actually be called
        call_command('wait_for_db')

        patched_check.assert_called_with(databases=['default'])

    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, patched_check: patch):
        """
        Test waiting for database when getting OperationalError.
        -
        The first two times we call the mocked method,
        we raise the psycopg2Error
        -
        The next 3 times, we raise OperationalError
        -
        On the sixth time, we pass in True
        """
        patched_check.side_effect = [psycopg2Error] * 2 + \
            [OperationalError] * 3 + [True]

        call_command('wait_for_db')

        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=['default'])
