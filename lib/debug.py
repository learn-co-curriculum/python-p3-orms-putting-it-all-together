#!/usr/bin/env python3

from dog import Dog, CONN, CURSOR

sql = """
    DROP TABLE IF EXISTS dogs
"""

CURSOR.execute(sql)

Dog.create_table()
joey = Dog("joey", "cocker spaniel")
joey.save()
fanny = Dog("fanny", "cockapoo")
fanny.save()

import ipdb; ipdb.set_trace()
