import requests
from bs4 import BeautifulSoup

class WebScraper:
    #============================================================================================  
    def __init__(self, configs):
        self.configs = configs

        # Create a session to maintain the authentication session
        self.session = requests.Session()     
    #============================================================================================  
    def login(self):
        try:
            # Send a POST request to the login page with authentication credentials
            login_url = self.configs['login_url']
            login_data = {
                'username': self.configs["username"],
                'password': self.configs["password"]
            }
            response = self.session.post(login_url, data=login_data)
            response.raise_for_status()
                
        except requests.exceptions.RequestException as e:
            return f"Error: {e}"
    #============================================================================================  
    # get all values 
    def get_value(self):
        results = None
        try:
            for target_url, find_value in self.configs["target_values"].items():
                # After successful authentication, make a GET request to the desired URL
                response = self.session.get(target_url)
                response.raise_for_status()

                # Parse the HTML content and extract the desired string
                soup = BeautifulSoup(response.content, 'html.parser')
                target_element = soup.find('p', class_='content')

                if target_element:
                    results[find_value] = target_element.get_text()
                else:
                    results[find_value] = None                

        except Exception as e:
            print(e)
        finally:
            return results
    #============================================================================================   
# end of class WebScraper       
