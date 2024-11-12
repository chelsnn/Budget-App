import pytest
from playwright.async_api import async_playwright, expect

@pytest.mark.asyncio
async def test_login():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto("http://127.0.0.1:5000/")

        # Check if the element with class 'logo' and text 'StudentSpender' is visible
        await expect(page.locator("h1.logo", has_text="StudentSpender")).to_be_visible()

        # Fill in login fields
        await page.fill("input#username", "hi")  # Adjust selector if necessary
        await page.fill("input#password", "hi")  # Adjust selector if necessary

        # Click the login button with class 'primary-btn' and text 'Login'
        await page.locator(".primary-btn", has_text="Login").click()

        # Expect a welcome message with the text "Welcome Back" to be visible
        await expect(page.locator("h1.welc", has_text="Welcome Back")).to_be_visible()

        await browser.close()
