try:
    from .reporter import reporter
    from .version import MOONSTREAMAPI_VERSION

    # Reporting
    reporter.tags.append(f"version:{MOONSTREAMAPI_VERSION}")
    reporter.system_report(publish=True)
    reporter.setup_excepthook(publish=True)
except:
    # Pass it to be able import MOONSTREAMAPI_VERSION in setup.py with pip
    pass
