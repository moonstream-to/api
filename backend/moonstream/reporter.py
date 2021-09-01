import uuid

from humbug.consent import HumbugConsent
from humbug.report import HumbugReporter

from .settings import BUGOUT_HUMBUG_TOKEN

session_id = str(uuid.uuid4())
client_id = "moonstream-backend"

reporter = HumbugReporter(
    name="moonstream",
    consent=HumbugConsent(True),
    client_id=client_id,
    session_id=session_id,
    bugout_token=BUGOUT_HUMBUG_TOKEN,
    tags=[],
)
