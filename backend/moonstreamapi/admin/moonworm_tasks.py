import logging

from ..settings import BUGOUT_REQUEST_TIMEOUT_SECONDS, MOONSTREAM_ADMIN_ACCESS_TOKEN, 
from ..settings import bugout_client as bc

logger = logging.getLogger(__name__)



def get_list_of_tags(query: str, tag: str):
    """
    Return list of tags depends on query and tag
    """

    existing_metods = bc.search(
        token=MOONSTREAM_ADMIN_ACCESS_TOKEN,
        journal_id=journal_id,
        query=search_query,
        content=False,
        timeout=10.0,
        limit=limit,
        offset=offset,
    )