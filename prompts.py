# provide context to AI system
system_message = """
    You are a budgeting and personal finance advisor. Help undergraduate students planning to study abroad create realistic 
    two-week spending plans based on their total budget and specified spending categories, ensuring they can sustain their 
    finances throughout the program.
"""

# generate a prompt based on input obtained from budget_form table
def generate_budget_prompt(budget, arrival_date, departure_date, city, country, categories):
    prompt = f"""
        I'm an undergraduate student starting a study abroad program in {city}, {country}. I’m concerned about managing 
        my budget of {budget} across these categories: {categories}. 

        Please provide a detailed spending plan broken down into two-week periods. Avoid any small talk or introductory remarks, 
        and do not include graphs, tables, or special formatting. The response should be structured in plain text and divided into 
        three paragraphs.

        My program runs from {arrival_date} to {departure_date}.
    """    
    return prompt