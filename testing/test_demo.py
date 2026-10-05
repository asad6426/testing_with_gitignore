import pytest
from playwright.sync_api import Page, expect


@pytest.fixture
def demo_page(page: Page):
    page.set_content(
        """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Automation Demo</title>
        </head>
        <body>
            <h1>Student Portal</h1>

            <label for="name">Student name</label>

            <input id="name" type="text">

            <button onclick="
                document.querySelector('#message').textContent =
                'Welcome, ' + document.querySelector('#name').value;
            ">
                Submit
            </button>

            <p id="message"></p>
        </body>
        </html>
        """
    )

    return page


def test_page_title(demo_page: Page):
    expect(demo_page).to_have_title("Automation Demo")


def test_student_submit(demo_page: Page):
    demo_page.get_by_label("Student name").fill("Asad")

    demo_page.get_by_role(
        "button",
        name="Submit"
    ).click()

    expect(
        demo_page.locator("#message")
    ).to_have_text("Welcome, Asad")


def test_heading_demo_failure(demo_page: Page):
    # Deliberately wrong: inspect the failure in the report.
    expect(
        demo_page.get_by_role("heading")
    ).to_have_text(
        "Student Portal",
        timeout=1000
    )