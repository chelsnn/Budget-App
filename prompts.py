# provide context to AI system
system_message = """
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
    You are a budgeting and personal finance advisor. Help undergraduate students planning to study abroad create realistic 
    two-week spending plans based on their total budget and specified spending categories, ensuring they can sustain their 
    finances throughout the program.
=======
=======
>>>>>>> 3e990c3 (Implemented OpenAI API, set up to produce output for budget_view based on user input)
    You are an expert budget setter and personal finances advisor.
    Your primary role is to assist undergraduate university students who are about to begin a study abroad program with 
    strategizing how they will spend their money throughout the duration throughout their program. 
    You will be prompted to come up with a detailed spending plan, breaking down the student's total budget for the program into
    two week spending periods across various categories that will you be given. 
    It is important that this spending plan is realistic and accurate, as the student would want to avoid following a budget plan 
    that would lead them to lose all their money while being in a foreign country, away from their family and without a source of
    income. 
<<<<<<< HEAD
>>>>>>> 7be1817 (Implemented OpenAI API, set up to produce output for budget_view based on user input)
=======
    You are a budgeting and personal finance advisor. Help undergraduate students planning to study abroad create realistic 
    two-week spending plans based on their total budget and specified spending categories, ensuring they can sustain their 
    finances throughout the program.
>>>>>>> eb87074 (Save changes before merging with main)
=======
>>>>>>> 3e990c3 (Implemented OpenAI API, set up to produce output for budget_view based on user input)
=======
    You are a budgeting and personal finance advisor. Help undergraduate students planning to study abroad create realistic 
    two-week spending plans based on their total budget and specified spending categories, ensuring they can sustain their 
    finances throughout the program.
>>>>>>> 15d9174 (Save changes before merging with main)
"""

# generate a prompt based on input obtained from budget_form table
def generate_budget_prompt(budget, arrival_date, departure_date, city, country, categories):
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> eb87074 (Save changes before merging with main)
    prompt = f"""
        I'm an undergraduate student starting a study abroad program in {city}, {country}. I’m concerned about managing 
        my budget of {budget} across these categories: {categories}. 

        Please provide a detailed spending plan broken down into two-week periods. Avoid any small talk or introductory remarks, 
        and do not include graphs, tables, or special formatting. The response should be structured in plain text and divided into 
        three paragraphs.

        My program runs from {arrival_date} to {departure_date}.
<<<<<<< HEAD
<<<<<<< HEAD
    """
    
=======
=======
>>>>>>> 3e990c3 (Implemented OpenAI API, set up to produce output for budget_view based on user input)
    prompt = """
=======
    prompt = f"""
>>>>>>> 64bef94 (Commit changes to complete rebasing)
        I am an undergraduate university student who is about to begin a study abroad program located in {city}, {country}.
        I am really excited to begin my program, though I have a couple reservations about how I will manage my money throughout
        the duration of the program.
        Specifically, I need help splitting my total budget of {budget} among the following categories: {categories}.
        I would like a detailed spending plan in which you tell me how much money you'd recommend I spend in each of the
        previously listed categories, broken down into two week spending periods. 
        My program begins on {arrival_date} and ends on {departure_date}.
    """
<<<<<<< HEAD
>>>>>>> 7be1817 (Implemented OpenAI API, set up to produce output for budget_view based on user input)
=======
    """
    
>>>>>>> eb87074 (Save changes before merging with main)
=======
>>>>>>> 3e990c3 (Implemented OpenAI API, set up to produce output for budget_view based on user input)
=======
    """
    
>>>>>>> 15d9174 (Save changes before merging with main)
    return prompt