#!/usr/bin/env python3

from lib import CONN, CURSOR
from lib.dog import Dog

sql = """
    DROP TABLE IF EXISTS dogs
"""

CURSOR.execute(sql)

Dog.create_table()
joey = Dog("joey", "cocker spaniel")
joey.save()
fanny = Dog("fanny", "cockapoo")
fanny.save()

import pytest; pytest.set_trace()
