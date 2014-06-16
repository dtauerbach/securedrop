import unittest

import crypto_util
import db_util
import test_setup

from db import db_session, Source
from mock import patch, ANY, MagicMock

class TestDbUtil(unittest.TestCase):

    def createTestSource(self, sid, display_name):
        self.test_source = Source(sid, display_name)
        #self.test_source.pending = False
        db_session.add(self.test_source)
        db_session.commit()

    def setUp(self):
        test_setup.create_directories()
        test_setup.init_db()
        self.mock_display_name = 'handbanana'
        self.sid = 'EQZGCJBRGISGOTC2NZVWG6LILJBHEV3CINNEWSCLLFTUWZJPKJFECLS2NZ4G4U3QOZCFKTTPNZMVIWDCJBBHMUDBGFHXCQ3R'
        crypto_util.superhero_display_id = MagicMock(
            return_value=self.mock_display_name)

    def tearDown(self):
        test_setup.clean_root()

    def test_create_source_display_name(self):
        self.assertEqual(
            db_util.create_source_display_name(), self.mock_display_name)

    def test_create_source_display_with_name_collision_no_escape(self):
        self.createTestSource(self.sid, self.mock_display_name)
        self.assertRaises(crypto_util.SourceException, db_util.create_source_display_name, 4)
        
