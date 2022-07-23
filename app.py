import os
from webbrowser import Chrome
from linkedin import linkedin
from dotenv import load_dotenv
from urllib.parse import urlparse

load_dotenv()

APPLICATiON_KEY    = os.getenv("APPLICATION_KEY") or "YOUR_APPLICATION_KEY"
APPLICATiON_SECRET = os.getenv("APPLICATION_SECRET") or "YOUR_APPLICATION_SECRET"
CHROME_PATH = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome' # Path to your Chrome executable

RETURN_URL = 'http://localhost:8000'
params_to_d = lambda params: {
    l[0]: l[1] for l in [j.split('=') for j in urlparse(params).query.split('&')]
}

def get_authorization_query(url):
    print("Open the browser and get the authorization code")
    print("The url will be in this format http://localhost:8000/?code=AUTHORIZATION_CODE&state=STATE")
    chrome = Chrome(CHROME_PATH)
    chrome.open_new_tab(url)
    final_url = input("Enter the url in the browser below: ")
    return params_to_d(final_url)

def linkedin_application():
    try:
        authentication = linkedin.LinkedInAuthentication(
                        APPLICATiON_KEY,
                        APPLICATiON_SECRET,
                        RETURN_URL,
                        ['r_emailaddress', 'r_liteprofile', 'w_member_social'],
                    )
        print("Please visit this URL to authorize the application: " + authentication.authorization_url)
        query = get_authorization_query(authentication.authorization_url)
        authentication.state = query.get('state')
        authentication.authorization_code = query.get('code')
        token_result = authentication.get_access_token()
        application = linkedin.LinkedInApplication(token=token_result.access_token)
        return application

    except linkedin.LinkedInError as e:
        print(e)
        return

def get_profile(application: linkedin.LinkedInApplication):
    try:
        profile = application.get_profile(selectors=['id', 'first-name', 'last-name', 'email-address'])
        return profile
    except linkedin.LinkedInError as e:
        print(e)
        return

def create_post(
    application: linkedin.LinkedInApplication,
    comment=None,
    title=None,
    description=None,
    submitted_url=None,
    submitted_image_url=None,
    visibility='connections-only'
):
    try:
        post = application.submit_share(
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

def get_connections(application: linkedin.LinkedInApplication):
    try:
        connections = application.get_connections()
        return connections
    except linkedin.LinkedInError as e:
        print(e)
        return

lkdn_application = linkedin_application()
post = create_post(
    lkdn_application,
    comment="This is a test post from the Python API",
    title="Test Post",
    description="This is a test post",
    submitted_url="https://www.google.com",
    submitted_image_url="https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png"
)
