def exact_selector(query: map, attr: str) -> str:
    '''Takes a query, which may contain: 
    date, BMI, height, weight, etnicity or community 
    and returns a single string containing all of these 
    various SQL SELECT commands concatenated'''
    select = ""

    if(query.exact.date):
        select += f" WHERE date = {query.exact.date}"
    
    if(query.exact.bmi):
        select += f" WHERE bmi = {query.exact.bmi}"

    if(query.exact.height):
        select += f" WHERE height = {query.exact.height}"

    if(query.exact.weight):
        select += f" WHERE weight = {query.exact.weight}"

    if(query.exact.age):
        select += f" WHERE age = {query.exact.age}"

    if(query.etnicity):
        select += f" WHERE etnicity = {query.etnicity}"

    if(query.community):
        select += f" WHERE community = {query.community}"

    if(query.cnes):
        select += f" WHERE cnes = {query.cnes}"

    if(query.education):
        select += f" WHERE education = {query.education}"

    if(query.genre and query.genre != '*'):
        select += f" WHERE genre = {query.genre}"

    return select

def range_selector(query: map, attr: str) -> str:
    '''Takes a query, which may contain:
    date, BMI, height, weight or age 
    and returns a single string containing all of these 
    various SQL SELECT commands concatenated'''
    select = ""

    if(query.initial.attr and query.final.attr):
        select += f" WHERE date >= {query.initial_date} AND date <= {query.final_date}"

    if(query.initial.attr):
        select += f" WHERE date >= {query.initial}{type}"

    if(query.final.attr):
        select += f" WHERE date <= {query.final_date}"

    return select

def regional_selector(query: map) -> str:
    '''Takes a query and returns a string containing 
    a SELECT statement of one state, one city or 
    entire Brazil'''
    select = ""

    if(query.state):
        select = f"SELECT {query.state} FROM states"

    if(query.city):
        select += f"SELECT {query.city} FROM cities"

    if(query.brazil):
        select = "SELECT * FROM cities"

    return select


def main(query: map) -> map:
    select = regional_selector(query)
    select += range_selector(query, 'date')

    return {'status': 200}
