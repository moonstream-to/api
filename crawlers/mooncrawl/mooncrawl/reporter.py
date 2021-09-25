import os
import uuid

from humbug.consent import HumbugConsent
from humbug.report import HumbugReporter

from .settings import HUMBUG_REPORTER_CRAWLERS_TOKEN

session_id = str(uuid.uuid4())
client_id = "moonstream-crawlers"

spire_url = os.environ.get("MOONSTREAM_SPIRE_API_URL")

reporter = HumbugReporter(
    name="moonstream-crawlers",
    consent=HumbugConsent(True),
    client_id=client_id,
    session_id=session_id,
    bugout_token=HUMBUG_REPORTER_CRAWLERS_TOKEN,
    tags=[],
    url=spire_url,
)
