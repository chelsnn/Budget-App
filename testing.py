import pytest
from playwright.async_api import async_playwright, expect

@pytest.mark.asyncio
async def test_login(): #normal sign in
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
async def test_home(): #homepage elements exist
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
async def test_signup(): #signup with new account
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



@pytest.mark.asyncio
async def test_expenses(): #add expense and that login from sign up works
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto("http://127.0.0.1:5000/")


        # Check if the element with class 'logo' and text 'StudentSpender' is visible
        await expect(page.locator("h1.logo", has_text="StudentSpender")).to_be_visible()
        await page.locator("a", has_text="Sign up").click()
        await page.locator("a", has_text="Login").click()
        await page.fill("input#username", "testuser")  # Adjust selector if necessary
        await page.fill("input#password", "hi")  # Adjust selector if necessary
        await page.locator(".primary-btn", has_text="Login").click()
        await expect(page.locator("h1.welc", has_text="Welcome Back")).to_be_visible()
        await page.locator("a", has_text="Expenses").click()
        await expect(page.locator("h1.expenses-title", has_text="Expenses")).to_be_visible()
        await page.locator("button.add-button", has_text="Add Expense").click() 
        await expect(page.locator("h1", has_text="Add Expense")).to_be_visible()
        await page.fill("input[name='amount']", "33")
        await page.fill("input[name='expenseName']", "Testing")
        # await page.locator("input[type='radio'][value='Food']").check()
        # await page.fill("input[name='date']", "11/12/2024")
        # await page.fill("input[name='notes']", "Testing notes")
        # await page.locator("button", has_text="Add").click()
        # await expect(page.locator("h1.expenses-title", has_text="Expenses")).to_be_visible()
        
        
        await browser.close()

