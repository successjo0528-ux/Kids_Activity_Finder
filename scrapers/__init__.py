from .base import BaseScraper
from .seongnam_lib import SeongnamLibraryScraper
from .seongnam_city import SeongnamCityScraper
from .gwacheon_sci import GwacheonScienceScraper
from .museum import MuseumScraper
from .conventions import ConventionScraper
from .contests import ContestScraper
from .sports_events import SportsEventsScraper
from .kids_platforms import KidsPlatformsScraper

ALL_SCRAPERS = [
    SeongnamLibraryScraper,
    SeongnamCityScraper,
    GwacheonScienceScraper,
    MuseumScraper,
    ConventionScraper,
    ContestScraper,
    SportsEventsScraper,
    KidsPlatformsScraper,
]

__all__ = [
    "BaseScraper",
    "ALL_SCRAPERS",
    "SeongnamLibraryScraper",
    "SeongnamCityScraper",
    "GwacheonScienceScraper",
    "MuseumScraper",
    "ConventionScraper",
    "ContestScraper",
    "SportsEventsScraper",
    "KidsPlatformsScraper",
]
