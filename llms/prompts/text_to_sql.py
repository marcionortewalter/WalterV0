examples = [
    {"input": "Find all introductions made to funds.", "query": "SELECT * FROM view_intros;"},
    {
        "input": "Find all introductions made to funds'.",
        "query": """SELECT 
    i.created_at,
    i.entry_id,
    f.name AS fund_name,
    c.name AS introduced_company_name
FROM 
    public.view_intros i
LEFT JOIN 
    public.companies f ON i.fund_company_id = f.id
LEFT JOIN 
    public.companies c ON i.intro_company_id = c.id;""",
    },
    {
        "input": "Tell me if what are the categories of Aptuno.",
        "query": """SELECT name, description, categories FROM companies
          WHERE name ILIKE '%Aptuno%' OR
          name ILIKE '%aptuno%' OR
          name ILIKE '%ptuno%' OR name NOT ILIKE '%market%'
          LIMIT 5; ---even though you only need one, the ILIKE may retrieve wrong results. This number can vary""",
    },
    {
        "input": "What are the ticket sizes for Canary?",
        "query": """SELECT frl.investment_range, frl.investor_type, frl.vc_quality_perception, frl.status, frl.observations, frl.meeting_frequency
FROM public.fund_relations_list frl --- give extra info to help the agent
JOIN public.companies c ON frl.company_id = c.id
WHERE c.name ILIKE '%canary%' OR c.name ILIKE '%canari%' OR c.name ILIKE '%canar%';""",
    },
    {
        "input": "List all funds from Outside Latam.",
        "query": """SELECT frl.*, c.name
FROM public.fund_relations_list frl
JOIN public.companies c ON frl.company_id = c.id
WHERE frl.geo_origin ILIKE '%outside%' OR frl.geo_origin ILIKE '%outside latam%' ;""",
    },
    {
        "input": "How many employees/members are there and who are they?",
        "query": 'SELECT name FROM "members"',
    },
    {
        "input": "Who is the founder of WeHandle?",
        "query": "SELECT * from people join companies on people.company_id = companies.id where companies.name ILIKE '%WeHandle%' and people.job_title ILIKE '%founder%';"
    }
]

prompt = """
    You are an agent designed to interact with a SQL database.
    Given an input question, create a syntactically correct {dialect} query to run, then look at the results of the query and return the answer.
    You can order the results by a relevant column to return the most interesting examples in the database and ALWAYS make it NULLS LAST. 
    Never query for all the columns from a specific table, only ask for the relevant columns given the question.
    You have access to tools for interacting with the database.
    Only use the given tools. Only use the information returned by the tools to construct your final answer.
    You MUST double check your query before executing it. If you get an error while executing a query, rewrite the query and try again.
    You MUST return all relevant data from the query in a structured format with enough information to answer the question.
    If the question is complex, you need to break it down into smaller questions and use the tools to answer each part.

    DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the database.

    ALWAYS SORT WITH NULL VALUES LAST. NULL = BAD.

    The user doesn't want to see IDs unless necessary. Always try to join with companies or people to get names

    Unless the user specifies, limit the number of rows returned to {top_k}.
    
    If the question does not seem related to the database, just return "I don't know" as the answer.

    The database contains the following schema:
    {schema}

    Here are some examples of user inputs and their corresponding SQL queries:
"""