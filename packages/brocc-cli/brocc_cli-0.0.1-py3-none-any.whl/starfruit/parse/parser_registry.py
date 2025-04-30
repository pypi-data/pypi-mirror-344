from typing import List

from starfruit.parse.base_parser import BaseParser
from starfruit.parse.html_parser import HtmlPageParser
from starfruit.parse.linkedin_post_parser import LinkedInPostParser
from starfruit.parse.twitter_feed_parser import TwitterFeedParser
from starfruit.parse.twitter_thread_parser import TwitterThreadParser

AnyParser = BaseParser

# --- Parser Registry ---
# Add new parser instances here.
# Order matters: More specific parsers (like Twitter, LinkedIn) should come BEFORE
# more generic parsers (like HtmlPageParser)
_parser_instances: List[AnyParser] = [
    TwitterThreadParser(),
    TwitterFeedParser(),
    LinkedInPostParser(),
    HtmlPageParser(),
]


def get_parser_for_url(url: str) -> AnyParser | None:
    """Finds the first parser instance that can handle the given URL."""
    for parser in _parser_instances:
        if parser.can_parse(url):
            return parser
    return None
