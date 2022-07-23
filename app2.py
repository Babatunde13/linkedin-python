import os
from webbrowser import Chrome
from linkedin import linkedin
from dotenv import load_dotenv
from urllib.parse import urlparse

load_dotenv()

class LinkedInWrapper:
    def __init__(self) -> None:
        self.application = None
        self.APPLICATION_KEY = os.getenv("APPLICATION_KEY") or "YOUR_APPLICATION_KEY"
        self.APPLICATION_SECRET = os.getenv("APPLICATION_SECRET") or "YOUR_APPLICATION_SECRET"
        self.CHROME_PATH = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome' # Path to your Chrome executable
        self.RETURN_URL = 'http://localhost:8000'
        try:
            self.authentication = linkedin.LinkedInAuthentication(
                            self.APPLICATION_KEY,
                            self.APPLICATION_SECRET,
                            self.RETURN_URL,
                            ['r_emailaddress', 'r_liteprofile', 'w_member_social'],
                        )
            print("Please visit this URL to authorize the application: " + self.authentication.authorization_url)
            query = self.get_authorization_query(self.authentication.authorization_url)
            self.authentication.state = query.get('state')
            self.authentication.authorization_code = query.get('code')
            token_result = self.authentication.get_access_token()
            self.application = linkedin.LinkedInApplication(token=token_result.access_token)

        except linkedin.LinkedInError as e:
            print(e)
            raise ValueError("Error while creating LinkedInWrapper")

    def get_authorization_query(self, url: str):
        print("Open the browser and get the authorization code")
        print("The url will be in this format http://localhost:8000/?code=AUTHORIZATION_CODE&state=STATE")
        chrome = Chrome(self.CHROME_PATH)
        chrome.open_new_tab(url)
        final_url = input("Enter the url in the browser below: ")
        return self.params_to_dictionary(final_url)
    
    def params_to_dictionary(self, params: str):
        return {
            l[0]: l[1] for l in [j.split('=') for j in urlparse(params).query.split('&')]
        }

    def get_profile(self):
        try:
            profile = self.application.get_profile(selectors=['id', 'first-name', 'last-name', 'email-address'])
            return profile
        except linkedin.LinkedInError as e:
            print(e)
            return

    def create_post(
        self,
        comment: str=None,
        title: str=None,
        description: str=None,
        submitted_url: str=None,
        submitted_image_url: str=None,
        visibility='connections-only'
    ):
        try:
            post = self.application.submit_share(
                comment=comment,
                title=title,
                description=description,
                submitted_url=submitted_url,
                submitted_image_url=submitted_image_url,
                visibility_code=visibility,
            )
            return post
        except linkedin.LinkedInError as e:
            print(e)
            return

    def get_connections(self):
        try:
            connections = self.application.get_connections()
            return connections
        except linkedin.LinkedInError as e:
            print(e)
            return

lkdn_application = LinkedInWrapper()
post = lkdn_application.create_post(
    comment="This is a test post from the Python API",
    title="Test Post",
    description="This is a test post",
    submitted_url="https://www.google.com",
    submitted_image_url="https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png"
)
