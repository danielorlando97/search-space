from search_space.spaces.domains import NaturalDomain, LogBachedDomain
from unittest import TestCase


class FinderTest(TestCase):
    def test_successes_find(self):
        domain = LogBachedDomain(
            NaturalDomain(1, 10),
            NaturalDomain(20, 30),
            NaturalDomain(100, 200)
        )

        for i in range(20, 30):
            index = domain._find_bache(i)
            assert index == 1

    def test_failed_find(self):
        domain = LogBachedDomain(
            NaturalDomain(1, 10),
            NaturalDomain(20, 30),
            NaturalDomain(100, 200)
        )

        for i in range(11, 20):
            index = domain._find_bache(i)
            assert index == 0

        for i in range(-5, 1):
            index = domain._find_bache(i)
            assert index == 0

        for i in range(201, 205):
            index = domain._find_bache(i)
            assert index == 2
