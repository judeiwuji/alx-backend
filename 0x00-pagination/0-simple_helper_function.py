#!/usr/bin/env python3
"""Module: Simple helper function"""


def index_range(page, page_size):
    """return a tuple of size two containing a start
    index and an end index

    Args:
        page(int)
        page_size(int)
    """
    start_index = (page - 1) * page_size
    end_index = (page) * page_size
    return start_index, end_index
