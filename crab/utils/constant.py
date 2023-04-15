FACEBOOK_EMAIL = 'test@example.com'
FACEBOOK_PASSWORD = 'password'

DRIVER_PATH_AT_SPIDER = './chromedriver_linux64/chromedriver'

GMAIL = 'm9389354@gmail.com'
GMAIL_PASSWORD = 'softsuave'
# GMAIL = 'softsuave125@gmail.com'
# GMAIL_PASSWORD = 'softsuave123'

# YOUTUBE_SIGNIN_PAGE = "https://accounts.google.com/signin/v2/identifier?service=youtube&uilel=3&continue=https%3A%2F%2Fwww.youtube.com%2Fsignin%3Fapp%3Ddesktop%26next%3D%252F&hl=en&passive=true&flowName=GlifWebSignIn&flowEntry=ServiceLogin"
YOUTUBE_SIGNIN_PAGE = "https://accounts.google.com/v3/signin/identifier?dsh=S1023855467%3A1680531238205517&continue=http%3A%2F%2Fsupport.google.com%2Fmail%2Fanswer%2F8494%3Fhl%3Den%26co%3DGENIE.Platform%253DDesktop&ec=GAZAdQ&hl=en&ifkv=AQMjQ7QOZNZLQ-WlzyVOTiLdjAamOW_k28Czx_ojqYdcQokmW_Ur2y-smdiROa1GIaaHfWWt_UBc&passive=true&flowName=GlifWebSignIn&flowEntry=ServiceLogin"
# YOUTUBE_SIGNIN_PAGE = "https://www.google.com/"


PAGE_LOAD_LOOP = 10


SEARCH_KEY = [
    'live',
    'live now',
    'live stream',
    'live concert',
    'live sports',
    'live gaming',
    'live TV',
    'live event',
    'live performance',
    'live show',
    'live webinar',
    'live workshop',
    'live interview',
    'live talk',
    'live discussion',
    'live debate',
    'live cooking',
    'live workout',
    'live meditation',
    'live yoga'
]


# XPATH case sentive
SEARCH_BOX_XPATH = [
    '//*[@type="search"]',
    '//input[@type="search"]',
    '//*[@id="search"]',
    '//*[@id="Search"]',
    '//input[@id="search"]',
    '//input[@id="Search"]',
    '//input[@placeholder="Search"]',
    '//input[@placeholder="search"]',
    '//input[@aria-label="Search"]',
    '//input[@aria-label="search"]',
]

XPATH_PLACEHOLDER_ARIA_LABEL_KEYS = [
    'search',
    'seach videos'
]