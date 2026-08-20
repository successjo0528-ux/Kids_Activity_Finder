from .base import BaseScraper
from .seongnam_lib import SeongnamLibraryScraper
from .seongnam_city import SeongnamCityScraper
from .gwacheon_sci import GwacheonScienceScraper
from .museum import MuseumScraper
from .conventions import ConventionScraper
from .contests import ContestScraper
from .sports_events import SportsEventsScraper
from .kids_platforms import KidsPlatformsScraper
from .regional_museums_sports import RegionalMuseumsSportsScraper
from .concerts import ConcertsScraper

ALL_SCRAPERS = [
    SeongnamLibraryScraper,
    SeongnamCityScraper,
    GwacheonScienceScraper,
    MuseumScraper,
    ConventionScraper,
    ContestScraper,
    SportsEventsScraper,
    KidsPlatformsScraper,
    RegionalMuseumsSportsScraper,
    ConcertsScraper,
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
    "RegionalMuseumsSportsScraper",
    "ConcertsScraper",
]
