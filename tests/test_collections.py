# -*- coding: utf-8 -*-

import unittest
from requests import HTTPError

from test_utils import *


class CollectionsTests(unittest.TestCase):
    def setUp(self):
        try:
            PyCy3.PyCy3.delete_all_networks()
        except:
            pass

    def tearDown(self):
        pass

    #    @PyCy3.skip
    @PyCy3.print_entry_exit
    def test_get_collection_list(self):
        # Verify that case of no collections is handled
        self.assertListEqual(PyCy3.get_collection_list(), [])

        # Verify that loading a single session returns a single collection
        load_test_session()
        self.assertSetEqual(set(PyCy3.get_collection_list()), {'galFiltered.sif'})

        # Verify that having two collections (one with two networks) returns two collections
        load_test_session('data/Multiple Collections.cys')
        self.assertSetEqual(set(PyCy3.get_collection_list()), {'galFiltered.sif', 'BINDyeast.sif'})

    #    @PyCy3.skip
    @PyCy3.print_entry_exit
    def test_get_collection_suid(self):
        # Verify that an error is raised when no collections exist
        self.assertRaises(PyCy3.CyError, PyCy3.get_collection_suid, 'current')

        # Initialization
        load_test_session()
        galFiltered_collection_suid = PyCy3.get_collection_suid()

        # Verify that current network returns the appropriate SUID
        self.assertEqual(PyCy3.get_collection_suid(), galFiltered_collection_suid)
        self.assertEqual(PyCy3.get_collection_suid('current'), galFiltered_collection_suid)
        self.assertEqual(PyCy3.get_collection_suid(PyCy3.get_network_suid()), galFiltered_collection_suid)
        self.assertEqual(PyCy3.get_collection_suid('galFiltered.sif'), galFiltered_collection_suid)

        # Verify that bogus network returns nothing
        self.assertRaises(PyCy3.CyError, PyCy3.get_collection_suid, 'bogus')
        self.assertRaises(PyCy3.CyError, PyCy3.get_collection_suid, -1)

    #    @PyCy3.skip
    @PyCy3.print_entry_exit
    def test_get_collection_name(self):
        # Verify that an error is raised when no collections exist
        self.assertRaises(PyCy3.CyError, PyCy3.get_collection_name, None)

        # Initialization
        load_test_session()
        galFiltered_collection_suid = PyCy3.get_collection_suid()

        # Verify that current collection returns the appropriate name
        self.assertEqual(PyCy3.get_collection_name(), 'galFiltered.sif')
        self.assertEqual(PyCy3.get_collection_name(galFiltered_collection_suid), 'galFiltered.sif')

        # TODO: Can't test fetching other names because we don't have access to other collection SUIDs ... can we fix this?

        # Verify that bogus collection SUID returns nothing
        self.assertRaises(PyCy3.CyError, PyCy3.get_collection_name, -1)

    #    @PyCy3.skip
    @PyCy3.print_entry_exit
    def test_get_collection_networks(self):
        # Verify that an error is raised when no collections exist
        self.assertRaises(PyCy3.CyError, PyCy3.get_collection_networks, None)

        # Initialization
        load_test_session('data/Multiple Collections.cys')
        galFiltered_collection_suid = PyCy3.get_collection_suid()

        # Verify that current collection returns four subnetworks
        network_list = PyCy3.get_collection_networks()
        self.assertIsInstance(network_list, list)
        self.assertSetEqual({PyCy3.get_network_name(suid) for suid in network_list},
                            {'galFiltered.sif', 'galFiltered.sif(1)', 'galFiltered.sif(2)', 'yeastHighQuality.sif'})

        # Verify that named collection returns the same subnetworks
        self.assertSetEqual(set(network_list), set(PyCy3.get_collection_networks(galFiltered_collection_suid)))

        # Verify that bogus collection SUID returns nothing
        self.assertRaises(PyCy3.CyError, PyCy3.get_collection_networks, -1)


if __name__ == '__main__':
    unittest.main()