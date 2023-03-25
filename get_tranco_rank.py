import requests
# https://tranco-list.eu/api_documentation
'''Note: If you want to call Tranco ranking API, you need to register for free at https://tranco-list.eu/ and get your API key.
Note:this only returns ranking for the last month. For more historical data we can build our own reference db from the 
historic data available on the site and then query it locally'''

def get_tranco_rank(domain):
    params = {"usernmame": "YOUR_USERNAME",
          "password":"YOUR_API_KEY"}

    endpoint = f"https://tranco-list.eu/api/ranks/domain/{domain}"


    #https://tranco-list.eu/api//ranks/domain/news24.com
    ranking = requests.get(endpoint).json()


    print(ranking)

    return ranking

if __name__ == "__main__":
    domain = "news24.com"

    get_tranco_rank(domain)