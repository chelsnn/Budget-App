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

@pytest.mark.asyncio
async def test_home():
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
        await expect(page.locator("h2.exchange", has_text="Exchange Rate Calculator")).to_be_visible()
        await expect(page.locator("h2.modhead", has_text="Total Budget")).to_be_visible()
        await expect(page.locator("h2.text", has_text="Weekly Budget Left")).to_be_visible()
        await expect(page.locator("h2.modhead", has_text="Recent Spending")).to_be_visible()   

        await browser.close()

@pytest.mark.asyncio
async def test_signup():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto("http://127.0.0.1:5000/")

        # Check if the element with class 'logo' and text 'StudentSpender' is visible
        await expect(page.locator("h1.logo", has_text="StudentSpender")).to_be_visible()

        await page.locator("a", has_text="Sign up").click()
        await page.fill("input[name='fullname']", "test test")  # Full Name field
        await page.fill("input[name='email']", "clarissachen5@gmail.com")  # Email field
        await page.fill("input[name='username']", "testuser")  # Username field
        await page.fill("input[name='password']", "hi")  # Password field
        await page.fill("input[name='address']", "USA")  # Home Country field
        await page.locator(".primary-btn", has_text="Sign Up").click()
        await page.fill("input#username", "testuser")  # Adjust selector if necessary
        await page.fill("input#password", "hi")  # Adjust selector if necessary
        await page.locator(".primary-btn", has_text="Login").click()
        await expect(page.locator("h1.welc", has_text="Welcome Back")).to_be_visible()

        await browser.close()


