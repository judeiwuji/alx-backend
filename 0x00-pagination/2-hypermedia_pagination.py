#!/usr/bin/env python3
"""Module: Hypermedia pagination"""
import csv
import math
from typing import List, Dict, Union


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """Returns data for a given page

        Args:
            page(int)
            page_size(int)
        """
        assert type(page) == int and page > 0
        assert type(page_size) == int and page_size > 0
        start_index, end_index = index_range(page, page_size)
        return self.dataset()[start_index:end_index]

    def get_hyper(self, page: int = 1, page_size: int = 10)\
            -> Dict[str, Union[int, None]]:
        """Returns a hypermedia data

        Args:
            page(int)
            page_size(int)
        """
        data = self.get_page(page, page_size)
        total_pages = math.ceil(len(self.dataset()) / page_size)
        has_prev = page - 1 > 0
        has_next = page + 1 <= total_pages

        return {
            'page_size': len(data),
            'page': page,
            'data': data,
            'next_page': page + 1 if has_next else None,
            'prev_page': page - 1 if has_prev else None,
            'total_pages': total_pages
        }


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
