import requests
import logging
import sys
import diamonds_fatch as df


def test_link():
    r = requests.get(df.DpLink)
    assert r.status_code == 200
