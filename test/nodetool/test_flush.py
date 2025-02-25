#
# Copyright 2023-present ScyllaDB
#
# SPDX-License-Identifier: AGPL-3.0-or-later
#

from rest_api_mock import expected_request
import utils


def test_flush(nodetool):
    nodetool("flush", "ks1", expected_requests=[
        expected_request("GET", "/storage_service/keyspaces", response=["ks1", "ks2"]),
        expected_request("POST", "/storage_service/keyspace_flush/ks1")
    ])


def test_flush_one_table(nodetool):
    nodetool("flush", "ks1", "tbl1", expected_requests=[
        expected_request("GET", "/storage_service/keyspaces", response=["ks1", "ks2"]),
        expected_request("POST", "/storage_service/keyspace_flush/ks1", params={"cf": "tbl1"})
    ])


def test_flush_two_tables(nodetool):
    nodetool("flush", "ks1", "tbl1", "tbl2", expected_requests=[
        expected_request("GET", "/storage_service/keyspaces", response=["ks1", "ks2"]),
        expected_request("POST", "/storage_service/keyspace_flush/ks1", params={"cf": "tbl1,tbl2"})
    ])


def test_flush_none_existent_keyspace(nodetool):
    utils.check_nodetool_fails_with(
            nodetool,
            ("flush", "non_existent_ks"),
            {"expected_requests": [expected_request("GET", "/storage_service/keyspaces", response=["ks1", "ks2"])]},
            ["nodetool: Keyspace [non_existent_ks] does not exist.",
             "error processing arguments: keyspace non_existent_ks does not exist"])
