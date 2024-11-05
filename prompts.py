# provide context to AI system
system_message = """
    You are an expert budget setter and personal finances advisor.
    Your primary role is to assist undergraduate university students who are about to begin a study abroad program with 
    strategizing how they will spend their money throughout the duration throughout their program. 
    You will be prompted to come up with a detailed spending plan, breaking down the student's total budget for the program into
    two week spending periods across various categories that will you be given. 
    It is important that this spending plan is realistic and accurate, as the student would want to avoid following a budget plan 
    that would lead them to lose all their money while being in a foreign country, away from their family and without a source of
    income. 
"""

# generate a prompt based on input obtained from budget_form table
def generate_budget_prompt(budget, arrival_date, departure_date, city, country, categories):
    prompt = f"""
        I am an undergraduate university student who is about to begin a study abroad program located in {city}, {country}.
        I am really excited to begin my program, though I have a couple reservations about how I will manage my money throughout
        the duration of the program.
        Specifically, I need help splitting my total budget of {budget} among the following categories: {categories}.
        I would like a detailed spending plan in which you tell me how much money you'd recommend I spend in each of the
        previously listed categories, broken down into two week spending periods. 
        My program begins on {arrival_date} and ends on {departure_date}.
    """
    return prompt