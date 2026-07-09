"""Tests for player owned-leader selection (Stellaris 4.x leader counting).

In Stellaris 4.x the ``leaders`` section contains both the empire's hired leaders
AND unrecruited recruitment-pool candidates, all tagged with ``country=<player>``.
Scanning by country therefore over-counts (e.g. 18 vs the 9 the Leaders screen
shows). The authoritative hired-leader set is the country's ``owned_leaders`` list.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from stellaris_save_extractor.base import SaveExtractorBase


class _Dummy(SaveExtractorBase):
    """Minimal base double: stubs the two dependencies of _get_player_owned_leader_ids."""

    def __init__(self, country_entry):
        self._country_entry = country_entry

    def get_player_empire_id(self):
        return 1

    def _get_player_country_entry(self, player_id=0):
        return self._country_entry


def test_returns_owned_leaders_as_string_set():
    ext = _Dummy({"owned_leaders": ["158", "439", "16777810"]})
    assert ext._get_player_owned_leader_ids() == {"158", "439", "16777810"}


def test_coerces_ids_to_strings():
    ext = _Dummy({"owned_leaders": [158, 439]})
    assert ext._get_player_owned_leader_ids() == {"158", "439"}


def test_returns_none_when_no_owned_leaders_field():
    # Pre-4.x saves / missing field -> None so the caller falls back to the scan.
    ext = _Dummy({})
    assert ext._get_player_owned_leader_ids() is None


def test_returns_none_when_country_entry_missing():
    ext = _Dummy(None)
    assert ext._get_player_owned_leader_ids() is None
