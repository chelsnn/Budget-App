import pytest
from playwright.async_api import async_playwright, expect
from datetime import datetime
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
        await page.fill("input[name='username']", "hi")  # Username field
        await page.fill("input[name='password']", "hi")  # Password field
        await page.fill("input[name='address']", "USA")  # Home Country field
        await page.locator(".primary-btn", has_text="Sign Up").click()
        await page.fill("input#username", "hi")  # Adjust selector if necessary
        await page.fill("input#password", "hi")  # Adjust selector if necessary
        await page.locator(".primary-btn", has_text="Login").click()
        await expect(page.locator("h1.welc", has_text="Welcome Back")).to_be_visible()

        await browser.close()



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
async def test_expenses(): #add expense and that login from sign up works
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto("http://127.0.0.1:5000/")


        # Check if the element with class 'logo' and text 'StudentSpender' is visible
        await expect(page.locator("h1.logo", has_text="StudentSpender")).to_be_visible()
        await page.locator("a", has_text="Sign up").click()
        await page.locator("a", has_text="Login").click()
        await page.fill("input#username", "hi")  # Adjust selector if necessary
        await page.fill("input#password", "hi")  # Adjust selector if necessary
        await page.locator(".primary-btn", has_text="Login").click()
        await expect(page.locator("h1.welc", has_text="Welcome Back")).to_be_visible()
        await page.locator("a", has_text="Expenses").click()
        await expect(page.locator("h1.expenses-title", has_text="Expenses")).to_be_visible()
        await page.locator("button.add-button", has_text="Add Expense").click() 
        await expect(page.locator("h1", has_text="Add Expense")).to_be_visible()
        await page.fill("input[name='amount']", "33")
        await page.fill("input[name='expenseName']", "Testing")
        await page.locator('input[type="radio"][value="travel"]').check()
        await page.locator('input[type="date"]').fill('2024-12-25')
        await page.fill("input[name='notes']", "test test test")
        await page.locator("button", has_text="Add").click()
        await expect(page.locator("h1.expenses-title", has_text="Expenses")).to_be_visible()
        await expect(page.locator("p.expense-title", has_text="Testing")).to_be_visible()
        await page.locator("button", has_text="Delete").click()
        count = await page.locator("h1.expenses-title", has_text="2024-12-25").count()
        assert count == 0, "Expected no elements with the text 'Expenses' to be visible"
                
        await browser.close()

@pytest.mark.asyncio
async def test_todayExpenses(): #checks that Today shows rather than date 
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto("http://127.0.0.1:5000/")


        # Check if the element with class 'logo' and text 'StudentSpender' is visible
        await expect(page.locator("h1.logo", has_text="StudentSpender")).to_be_visible()
        await page.locator("a", has_text="Sign up").click()
        await page.locator("a", has_text="Login").click()
        await page.fill("input#username", "hi")  # Adjust selector if necessary
        await page.fill("input#password", "hi")  # Adjust selector if necessary
        await page.locator(".primary-btn", has_text="Login").click()
        await expect(page.locator("h1.welc", has_text="Welcome Back")).to_be_visible()
        await page.locator("a", has_text="Expenses").click()
        await expect(page.locator("h1.expenses-title", has_text="Expenses")).to_be_visible()
        await page.locator("button.add-button", has_text="Add Expense").click() 
        await expect(page.locator("h1", has_text="Add Expense")).to_be_visible()
        await page.fill("input[name='amount']", "33")
        await page.fill("input[name='expenseName']", "Testing")
        await page.locator('input[type="radio"][value="travel"]').check()
        today = datetime.today().strftime('%Y-%m-%d') 
        await page.locator('input[type="date"]').fill(today)
        await page.fill("input[name='notes']", "test test test")
        await page.locator("button", has_text="Add").click()
        await expect(page.locator("h1.expenses-title", has_text="Expenses")).to_be_visible()
        await expect(page.locator("p.expense-title", has_text="Testing")).to_be_visible()
        count = await page.locator("h1.expenses-title", has_text=today).count()
        assert count == 0, "Expected no elements with the text 'Expenses' to be visible"
        await expect(page.locator("h1", has_text="Today")).to_be_visible()
        await page.locator("button", has_text="Delete").click()   
        await browser.close()

@pytest.mark.asyncio
async def test_expensesCategories(): #checks that all expenses categories can be selected and shown properly 
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto("http://127.0.0.1:5000/")


        # Check if the element with class 'logo' and text 'StudentSpender' is visible
        await expect(page.locator("h1.logo", has_text="StudentSpender")).to_be_visible()
        await page.locator("a", has_text="Sign up").click()
        await page.locator("a", has_text="Login").click()
        await page.fill("input#username", "hi")  # Adjust selector if necessary
        await page.fill("input#password", "hi")  # Adjust selector if necessary
        await page.locator(".primary-btn", has_text="Login").click()
        await expect(page.locator("h1.welc", has_text="Welcome Back")).to_be_visible()
        await page.locator("a", has_text="Expenses").click()
        await expect(page.locator("h1.expenses-title", has_text="Expenses")).to_be_visible()


        await page.locator("button.add-button", has_text="Add Expense").click() 
        await expect(page.locator("h1", has_text="Add Expense")).to_be_visible()
        await page.fill("input[name='amount']", "5")
        await page.fill("input[name='expenseName']", "category test")
        await page.locator('input[type="radio"][value="food"]').check()
        today = datetime.today().strftime('%Y-%m-%d') 
        await page.locator('input[type="date"]').fill(today)
        await page.fill("input[name='notes']", "test test test")
        await page.locator("button", has_text="Add").click()
        await expect(page.locator("h1.expenses-title", has_text="Expenses")).to_be_visible()
        await expect(page.locator("p.expense-title", has_text="category test")).to_be_visible()
        count = await page.locator("h1.expenses-title", has_text=today).count()
        assert count == 0, "Expected no elements with the text 'Expenses' to be visible"
        await expect(page.locator("h1", has_text="Today")).to_be_visible()
        await expect(page.locator("img#food")).to_be_visible()
        await page.locator("button", has_text="Delete").click() 

        await page.locator("button.add-button", has_text="Add Expense").click() 
        await expect(page.locator("h1", has_text="Add Expense")).to_be_visible()
        await page.fill("input[name='amount']", "5")
        await page.fill("input[name='expenseName']", "category test")
        await page.locator('input[type="radio"][value="accomodation"]').check()
        today = datetime.today().strftime('%Y-%m-%d') 
        await page.locator('input[type="date"]').fill(today)
        await page.fill("input[name='notes']", "test test test")
        await page.locator("button", has_text="Add").click()
        await expect(page.locator("h1.expenses-title", has_text="Expenses")).to_be_visible()
        await expect(page.locator("p.expense-title", has_text="category test")).to_be_visible()
        count = await page.locator("h1.expenses-title", has_text=today).count()
        assert count == 0, "Expected no elements with the text 'Expenses' to be visible"
        await expect(page.locator("h1", has_text="Today")).to_be_visible()
        await expect(page.locator("img#accomodation")).to_be_visible()
        await page.locator("button", has_text="Delete").click() 

        await page.locator("button.add-button", has_text="Add Expense").click() 
        await expect(page.locator("h1", has_text="Add Expense")).to_be_visible()
        await page.fill("input[name='amount']", "5")
        await page.fill("input[name='expenseName']", "category test")
        await page.locator('input[type="radio"][value="travel"]').check()
        today = datetime.today().strftime('%Y-%m-%d') 
        await page.locator('input[type="date"]').fill(today)
        await page.fill("input[name='notes']", "test test test")
        await page.locator("button", has_text="Add").click()
        await expect(page.locator("h1.expenses-title", has_text="Expenses")).to_be_visible()
        await expect(page.locator("p.expense-title", has_text="category test")).to_be_visible()
        count = await page.locator("h1.expenses-title", has_text=today).count()
        assert count == 0, "Expected no elements with the text 'Expenses' to be visible"
        await expect(page.locator("h1", has_text="Today")).to_be_visible()
        await expect(page.locator("img#travel")).to_be_visible()
        await page.locator("button", has_text="Delete").click() 

        await page.locator("button.add-button", has_text="Add Expense").click() 
        await expect(page.locator("h1", has_text="Add Expense")).to_be_visible()
        await page.fill("input[name='amount']", "5")
        await page.fill("input[name='expenseName']", "category test")
        await page.locator('input[type="radio"][value="entertainment"]').check()
        today = datetime.today().strftime('%Y-%m-%d') 
        await page.locator('input[type="date"]').fill(today)
        await page.fill("input[name='notes']", "test test test")
        await page.locator("button", has_text="Add").click()
        await expect(page.locator("h1.expenses-title", has_text="Expenses")).to_be_visible()
        await expect(page.locator("p.expense-title", has_text="category test")).to_be_visible()
        count = await page.locator("h1.expenses-title", has_text=today).count()
        assert count == 0, "Expected no elements with the text 'Expenses' to be visible"
        await expect(page.locator("h1", has_text="Today")).to_be_visible()
        await expect(page.locator("img#entertainment")).to_be_visible()
        await page.locator("button", has_text="Delete").click() 


        await page.locator("button.add-button", has_text="Add Expense").click() 
        await expect(page.locator("h1", has_text="Add Expense")).to_be_visible()
        await page.fill("input[name='amount']", "5")
        await page.fill("input[name='expenseName']", "category test")
        await page.locator('input[type="radio"][value="shopping"]').check()
        today = datetime.today().strftime('%Y-%m-%d') 
        await page.locator('input[type="date"]').fill(today)
        await page.fill("input[name='notes']", "test test test")
        await page.locator("button", has_text="Add").click()
        await expect(page.locator("h1.expenses-title", has_text="Expenses")).to_be_visible()
        await expect(page.locator("p.expense-title", has_text="category test")).to_be_visible()
        count = await page.locator("h1.expenses-title", has_text=today).count()
        assert count == 0, "Expected no elements with the text 'Expenses' to be visible"
        await expect(page.locator("h1", has_text="Today")).to_be_visible()
        await expect(page.locator("img#shopping")).to_be_visible()
        await page.locator("button", has_text="Delete").click() 


        await page.locator("button.add-button", has_text="Add Expense").click() 
        await expect(page.locator("h1", has_text="Add Expense")).to_be_visible()
        await page.fill("input[name='amount']", "5")
        await page.fill("input[name='expenseName']", "category test")
        await page.locator('input[type="radio"][value="miscellaneous"]').check()
        today = datetime.today().strftime('%Y-%m-%d') 
        await page.locator('input[type="date"]').fill(today)
        await page.fill("input[name='notes']", "test test test")
        await page.locator("button", has_text="Add").click()
        await expect(page.locator("h1.expenses-title", has_text="Expenses")).to_be_visible()
        await expect(page.locator("p.expense-title", has_text="category test")).to_be_visible()
        count = await page.locator("h1.expenses-title", has_text=today).count()
        assert count == 0, "Expected no elements with the text 'Expenses' to be visible"
        await expect(page.locator("h1", has_text="Today")).to_be_visible()
        await expect(page.locator("img#miscellaneous")).to_be_visible()
        await page.locator("button", has_text="Delete").click() 

        await browser.close()
