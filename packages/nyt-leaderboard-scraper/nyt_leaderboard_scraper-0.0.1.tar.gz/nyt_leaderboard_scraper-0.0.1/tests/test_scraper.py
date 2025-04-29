"""Test to see if the scraper actually grabs data."""

import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from src.nyt_leaderboard_scraper import scraper
from credential import nyt_s_cookie


class ScraperTests(unittest.TestCase):

    def test_print_leaderboard(self):
        print(f"{ScraperTests.test_print_leaderboard.__name__.upper()}:")

        session = scraper.create_requests_session(nyt_s_cookie)
        score_collection = scraper.scrape_leaderboard(session)
        session.close()

        print(score_collection)
        self.assertIsNotNone(score_collection)
        print()

    def test_property_access(self):
        print(f"{ScraperTests.test_property_access.__name__.upper()}:")

        session = scraper.create_requests_session(nyt_s_cookie)
        score_collection = scraper.scrape_leaderboard(session)
        session.close()

        for score in score_collection:
            print(score.username + str(score.crossword_date) + str(score.time_in_seconds))
            self.assertIsNotNone(score.username)
            self.assertIsNotNone(score.crossword_date)
        print()


if __name__ == "__main__":
    unittest.main()
