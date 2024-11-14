import pytest
from playwright.async_api import async_playwright, expect
from datetime import datetime
@pytest.mark.asyncio
async def test_signup(): # sign up with new account
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto("http://127.0.0.1:5000/")

        # check if the element with class 'logo' and text 'StudentSpender' is visible
        await expect(page.locator("h1.logo", has_text="StudentSpender")).to_be_visible()

        # sign up for account using dummy data
        await page.locator("a", has_text="Sign up").click()
        await page.fill("input[name='fullname']", "test test")  
        await page.fill("input[name='email']", "test@email.com")  
        await page.fill("input[name='username']", "hi")  
        await page.fill("input[name='password']", "hi")  
        await page.fill("input[name='address']", "USA")
        await page.locator(".primary-btn", has_text="Sign Up").click()

        # log in with newly created account
        await page.fill("input#username", "hi")  
        await page.fill("input#password", "hi")  
        await page.locator(".primary-btn", has_text="Login").click()

        # check if 'Welcome Back' text on homepage is visible
        await expect(page.locator("h1.welc", has_text="Welcome Back")).to_be_visible()

        await browser.close()

@pytest.mark.asyncio
async def test_login(): # normal sign in, then check for welcome message
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto("http://127.0.0.1:5000/")

        # check if the element with class 'logo' and text 'StudentSpender' is visible
        await expect(page.locator("h1.logo", has_text="StudentSpender")).to_be_visible()

        # log in to existing account
        await page.fill("input#username", "hi")  
        await page.fill("input#password", "hi")  
        await page.locator(".primary-btn", has_text="Login").click()

        # check if 'Welcome Back' text on homepage is visible
        await expect(page.locator("h1.welc", has_text="Welcome Back")).to_be_visible()

        await browser.close()

@pytest.mark.asyncio
async def test_logout(): # normal sign in, then log out
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto("http://127.0.0.1:5000/")

        # check if the element with class 'logo' and text 'StudentSpender' is visible
        await expect(page.locator("h1.logo", has_text="StudentSpender")).to_be_visible()

        # log in to existing account
        await page.fill("input#username", "hi")  
        await page.fill("input#password", "hi")  
        await page.locator(".primary-btn", has_text="Login").click()

        # check if 'Welcome Back' text on homepage is visible
        await expect(page.locator("h1.welc", has_text="Welcome Back")).to_be_visible()

        # log out from active user session
        await page.locator("a", has_text="Log Out").click()

        # check if login popup container is visible
        await expect(page.locator("div.popup-container")).to_be_visible()

        await browser.close()

@pytest.mark.asyncio
async def test_logout(): # normal sign in, then check for homepage text elements
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto("http://127.0.0.1:5000/")

        # check if the element with class 'logo' and text 'StudentSpender' is visible
        await expect(page.locator("h1.logo", has_text="StudentSpender")).to_be_visible()

        # log in to existing account
        await page.fill("input#username", "hi") 
        await page.fill("input#password", "hi") 
        await page.locator(".primary-btn", has_text="Login").click()

        # check if all expected homepage text elements are visible
        await expect(page.locator("h1.welc", has_text="Welcome Back")).to_be_visible()
        await expect(page.locator("h2.exchange", has_text="Exchange Rate Calculator")).to_be_visible()
        await expect(page.locator("h2.modhead", has_text="Total Budget")).to_be_visible()
        await expect(page.locator("h2.text", has_text="Weekly Budget Left")).to_be_visible()
        await expect(page.locator("h2.modhead", has_text="Recent Spending")).to_be_visible()   

        await browser.close()


@pytest.mark.asyncio
async def test_expenses(): # add expense to an existing account
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto("http://127.0.0.1:5000/")

        # check if the element with class 'logo' and text 'StudentSpender' is visible
        await expect(page.locator("h1.logo", has_text="StudentSpender")).to_be_visible()

        # navigate to signup form and back to login form 
        await page.locator("a", has_text="Sign up").click()
        await page.locator("a", has_text="Login").click()

        # log in to existing account
        await page.fill("input#username", "hi")  
        await page.fill("input#password", "hi")  
        await page.locator(".primary-btn", has_text="Login").click()

        # check if 'Welcome Back' text on homepage is visible
        await expect(page.locator("h1.welc", has_text="Welcome Back")).to_be_visible()

        # navigate to expense page, add a sample expense
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

        # navigate back to expense page, delete previously created expense
        await expect(page.locator("h1.expenses-title", has_text="Expenses")).to_be_visible()
        await expect(page.locator("p.expense-title", has_text="Testing")).to_be_visible()
        await page.locator("button", has_text="Delete").click()
        count = await page.locator("h1.expenses-title", has_text="12-25-2024").count()

        # check that expense was added and deleted as intended
        assert count == 0, "Expected no elements with the text 'Expenses' to be visible"
                
        await browser.close()

@pytest.mark.asyncio
async def test_todayExpenses(): # the word 'Today' should be displayed instead of today's date 
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto("http://127.0.0.1:5000/")

        # check if the element with class 'logo' and text 'StudentSpender' is visible
        await expect(page.locator("h1.logo", has_text="StudentSpender")).to_be_visible()

        # log in to existing account
        await page.locator("a", has_text="Sign up").click()
        await page.locator("a", has_text="Login").click()
        await page.fill("input#username", "hi")  
        await page.fill("input#password", "hi")  
        await page.locator(".primary-btn", has_text="Login").click()

        # navigate to expenses page from homepage, add a sample expense
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

        # navigate back to Expenses page, check that 'Today' is displayed
        await expect(page.locator("h1.expenses-title", has_text="Expenses")).to_be_visible()
        await expect(page.locator("p.expense-title", has_text="Testing")).to_be_visible()
        today = datetime.today().strftime('%m-%d-%Y')
        count = await page.locator("h1.expenses-title", has_text=today).count()
        assert count == 0, "Expected no elements with the text 'Expenses' to be visible"
        await expect(page.locator("h1", has_text="Today")).to_be_visible()
        await page.locator("button", has_text="Delete").click()   
        await browser.close()

@pytest.mark.asyncio
async def test_expensesCategories(): # all expenses categories can be selected and displayed 
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto("http://127.0.0.1:5000/")

        # log in to existing account, navigate to expenses page
        await expect(page.locator("h1.logo", has_text="StudentSpender")).to_be_visible()
        await page.locator("a", has_text="Sign up").click()
        await page.locator("a", has_text="Login").click()
        await page.fill("input#username", "hi") 
        await page.fill("input#password", "hi")
        await page.locator(".primary-btn", has_text="Login").click()
        await expect(page.locator("h1.welc", has_text="Welcome Back")).to_be_visible()
        await page.locator("a", has_text="Expenses").click()
        await expect(page.locator("h1.expenses-title", has_text="Expenses")).to_be_visible()

        # test food category
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
        today = datetime.today().strftime('%m-%d-%Y')
        count = await page.locator("h1.expenses-title", has_text=today).count()
        assert count == 0, "Expected no elements with the text 'Expenses' to be visible"
        await expect(page.locator("h1", has_text="Today")).to_be_visible()
        await expect(page.locator("img#food")).to_be_visible()
        await page.locator("button", has_text="Delete").click() 

        # test accomodation category
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
        today = datetime.today().strftime('%m-%d-%Y')
        count = await page.locator("h1.expenses-title", has_text=today).count()
        assert count == 0, "Expected no elements with the text 'Expenses' to be visible"
        await expect(page.locator("h1", has_text="Today")).to_be_visible()
        await expect(page.locator("img#accomodation")).to_be_visible()
        await page.locator("button", has_text="Delete").click() 

        # test travel category
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
        today = datetime.today().strftime('%m-%d-%Y')
        count = await page.locator("h1.expenses-title", has_text=today).count()
        assert count == 0, "Expected no elements with the text 'Expenses' to be visible"
        await expect(page.locator("h1", has_text="Today")).to_be_visible()
        await expect(page.locator("img#travel")).to_be_visible()
        await page.locator("button", has_text="Delete").click() 

        # test entertainment category
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
        today = datetime.today().strftime('%m-%d-%Y')
        count = await page.locator("h1.expenses-title", has_text=today).count()
        assert count == 0, "Expected no elements with the text 'Expenses' to be visible"
        await expect(page.locator("h1", has_text="Today")).to_be_visible()
        await expect(page.locator("img#entertainment")).to_be_visible()
        await page.locator("button", has_text="Delete").click() 

        # test shopping category
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
        today = datetime.today().strftime('%m-%d-%Y')
        count = await page.locator("h1.expenses-title", has_text=today).count()
        assert count == 0, "Expected no elements with the text 'Expenses' to be visible"
        await expect(page.locator("h1", has_text="Today")).to_be_visible()
        await expect(page.locator("img#shopping")).to_be_visible()
        await page.locator("button", has_text="Delete").click() 

        # test miscellaneous category
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
        today = datetime.today().strftime('%m-%d-%Y')
        count = await page.locator("h1.expenses-title", has_text=today).count()
        assert count == 0, "Expected no elements with the text 'Expenses' to be visible"
        await expect(page.locator("h1", has_text="Today")).to_be_visible()
        await expect(page.locator("img#miscellaneous")).to_be_visible()
        await page.locator("button", has_text="Delete").click() 

        await browser.close()

@pytest.mark.asyncio
async def test_budget_form_valid_input(): # test budget form with valid user input
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto("http://127.0.0.1:5000/")

        # log into already existing account, access home page
        await page.fill("input#username", "hi")  
        await page.fill("input#password", "hi")  
        await page.click("button[type='submit']")
        await page.wait_for_url("http://127.0.0.1:5000/homepage")
        await page.click("a:has-text('Budget')")  

        # navigate to budget_form webpage, fill out form with dummy data
        await page.wait_for_url("http://127.0.0.1:5000/budget_form")
        await page.fill("input[name='budget']", "3000")
        await page.fill("input[name='arrival_date']", "2024-08-31")
        await page.fill("input[name='departure_date']", "2024-12-13")
        await page.fill("input[name='city']", "London")
        await page.fill("input[name='country']", "United Kingdom")
        await page.click("button[type='submit']")  

        # navigate to budget_category webpage, select dummy checkboxes
        await page.wait_for_url("http://127.0.0.1:5000/budget_category")  
        await page.click("input[name='categories'][value='food']")
        await page.click("input[name='categories'][value='entertainment']")
        await page.click("input[name='categories'][value='shopping']")
        await page.click("button[type='submit']") 

        # navigate to budget_view webpage, check for AI generated output
        await page.wait_for_url("http://127.0.0.1:5000/budget_view") 
        ai_output_element = page.locator(".api-output")  
        await ai_output_element.wait_for(state="visible")

        await browser.close()

@pytest.mark.asyncio
async def test_budget_form_no_input(): # test budget form with no input
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto("http://127.0.0.1:5000/")

        # log into an existing account, navigate to budget_form
        await page.fill("input#username", "hi")
        await page.fill("input#password", "hi")
        await page.click("button[type='submit']")
        await page.wait_for_url("http://127.0.0.1:5000/homepage")
        await page.click("a:has-text('Budget')")
        await page.wait_for_url("http://127.0.0.1:5000/budget_form")

        # attempt to submit empty budget form 
        await page.click("button[type='submit']")

        # verify error message is shown and form submission is blocked
        error_element = page.locator(".error-message")
        await error_element.wait_for(state="visible")

        await browser.close()

@pytest.mark.asyncio
async def test_budget_form_invalid_input(): # test budget form with invalid input, display all possible error messages 
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto("http://127.0.0.1:5000/")

        # log into an existing account, navigate to budget_form
        await page.fill("input#username", "hi")
        await page.fill("input#password", "hi")
        await page.click("button[type='submit']")
        await page.wait_for_url("http://127.0.0.1:5000/homepage")
        await page.click("a:has-text('Budget')")
        await page.wait_for_url("http://127.0.0.1:5000/budget_form")

        # round 1: attempt to submit empty budget form 
        await page.click("button[type='submit']")
        error_element = page.locator(".error-message")
        await error_element.wait_for(state="visible")
        error_text = await error_element.text_content()
        assert error_text == " Budget must be a numeric value.", f"Expected error message to be 'Budget must be a numeric value.' but got '{error_text}'"

        # round 2: attempt to submit budget form with empty date
        await page.fill("input[name='budget']", "3000")
        await page.fill("input[name='departure_date']", "2024-12-13")
        await page.fill("input[name='city']", "Geneva")
        await page.fill("input[name='country']", "Switzerland")
        await page.click("button[type='submit']")
        error_element = page.locator(".error-message")
        await error_element.wait_for(state="visible")
        error_text = await error_element.text_content()
        assert error_text == " Both arrival and departure dates are required.", f"Expected error message to be 'Both arrival and departure dates are required.' but got '{error_text}'"

        # round 3: attempt to submit budget form with empty location
        await page.fill("input[name='budget']", "3000")
        await page.fill("input[name='arrival_date']", "2024-09-13")
        await page.fill("input[name='departure_date']", "2024-12-13")
        await page.fill("input[name='city']", "Berlin")
        await page.fill("input[name='country']", "")
        await page.click("button[type='submit']")
        error_element = page.locator(".error-message")
        await error_element.wait_for(state="visible")
        error_text = await error_element.text_content()
        assert error_text == " City and country are required.", f"Expected error message to be 'City and country are required.' but got '{error_text}'"

        await browser.close()
