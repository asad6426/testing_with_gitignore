import base64
import warnings

import pytest
import pytest_html


def pytest_html_report_title(report):
    report.title = "Automation Test Dashboard"


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when != "call" or not report.failed:
        return

    page = item.funcargs.get("page")

    if page is None or page.is_closed():
        return

    try:
        screenshot = page.screenshot(
            full_page=True,
            timeout=5000,
        )

        encoded_image = base64.b64encode(
            screenshot
        ).decode("ascii")

        extras = getattr(report, "extras", [])

        extras.append(
            pytest_html.extras.png(
                encoded_image,
                name="Failure screenshot",
            )
        )

        report.extras = extras

    except Exception as error:
        warnings.warn(
            f"Could not capture screenshot: {error}",
            RuntimeWarning,
        )