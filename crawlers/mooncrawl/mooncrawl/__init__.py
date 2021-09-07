from .reporter import reporter
from .version import MOONCRAWL_VERSION

# Reporting
reporter.tags.append(f"version:{MOONCRAWL_VERSION}")
reporter.system_report(publish=True)
reporter.setup_excepthook(publish=True)
