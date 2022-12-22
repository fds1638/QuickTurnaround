import sys
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Notes:
# Done on Dec 21, 2022.
# I had never scraped before and it had been a while since I had used pandas.
# I wanted a project showing a quick turnaround doing something that I didn't already know how to do.

def get_billions(s):
    """ Assume s is of the form: $xx.x B
    Extract s to a float.
    """
    f = s.split()[0][1:]
    return float(f)

def get_employee_count(e):
    """ Assume e is an integer """
    return float(e.replace(',',''))

def main():
    """ Get table from Forbes 2022 largest private companies,
    and print the company with highest revenue per employee in each industry.
    """

    # Given the URL, get the tables (the tables are split up in the hmtl, with ads in between).
    URL = "https://www.forbes.com/lists/largest-private-companies/?sh=41d16995bac4"
    r = requests.get(URL)
    soup = BeautifulSoup(r.content, 'html5lib')
    tables = soup.find_all('div', attrs = {'class':'table-row-group'}) 

    # Go through the tables, put the information in a list. Transform some strings to numbers.    
    companies_data = []
    for table in tables:
        for row in table.findAll('a'):
            rank = row.find('div', attrs = {'class':'rank first table-cell rank'}).text
            name = row.find('div', attrs = {'class':'organizationName second table-cell name'}).text
            state = row.find('div', attrs = {'class':'state table-cell state'}).text
            industry = row.find('div', attrs = {'class':'industries table-cell industry'}).text
            revenue = row.find('div', attrs = {'class':'revenue table-cell revenue'}).text
            employees = row.find('div', attrs = {'class':'employees table-cell employees'}).text
    
            company_data = (rank, name, state, industry, get_billions(revenue), get_employee_count(employees))
            companies_data.append(company_data)
    
    # Create a dataframe out of the list, calculate revenue per employee.
    df = pd.DataFrame(companies_data, columns=['rank','name','state','industry','revenue(B)','employees'])
    df['revenue_per_employee'] = df['revenue(B)']/df['employees']*1000000000.0
    df['revenue_per_employee'] = df['revenue_per_employee'].apply(pd.to_numeric)

    # Get the company with the max revenue_per_employee in each industry.   
    df=df[df['revenue_per_employee']==df.groupby('industry')['revenue_per_employee'].transform('max')]
   
    # Sort the maxima in descending order. 
    df = df.sort_values(by=['revenue_per_employee'], ascending=False)

    # Format and print.    
    format_mapping = {"revenue(B)": "{:,.1f}", "employees": "{:,.0f}", "revenue_per_employee": "{:,.0f}"}
    for key, value in format_mapping.items():
        df[key] = df[key].apply(value.format)
    print(df)

    return 0

if __name__ == '__main__':
    sys.exit(main())
