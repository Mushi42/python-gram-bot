from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

client = MongoClient('mongodb://localhost:27017')
db = client['scrapper']
commissionersCollection = db['commissioners']
organizationsCollection = db['organizations']
rolesCollection = db['roles']

BASE_URL = "https://commissioners.ec.europa.eu"


def init_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    return webdriver.Chrome(options=options)


# Set up the webdriver
driver = init_driver()

# Load the webpage
driver.get(f'{BASE_URL}/index_en')

# Wait for the page to load
wait = WebDriverWait(driver, 10)
wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "ecl-u-mb-2xl")))

# Find all the commissioner boxes
mainDivs = driver.find_elements(By.CLASS_NAME, 'ecl-u-mb-2xl')
commissioners = mainDivs[4].find_elements(By.CLASS_NAME, 'ecl-content-item')

# Extract the commissioners' information
commissionersList = [{
    'image': commissioner.find_element(By.CLASS_NAME, 'ecl-content-item__image').get_attribute('src'),
    'profileLink': commissioner.find_element(By.CLASS_NAME, 'ecl-link').get_attribute('href'),
    'role': commissioner.find_element(By.CLASS_NAME, 'ecl-content-block__primary-meta-item').text,
    'name': commissioner.find_element(By.CLASS_NAME, 'ecl-content-block__title').text,
    'organization': commissioner.find_element(By.CLASS_NAME, 'ecl-content-block__description').text,
} for commissioner in commissioners]

# Extract additional information for each commissioner
for commissioner in commissionersList:
    driver.get(commissioner['profileLink'])

    wait = WebDriverWait(driver, 10)
    wait.until(EC.visibility_of_element_located(
        (By.CLASS_NAME, "ecl-list-illustration__description")))

    addressDiv = driver.find_element(
        By.CLASS_NAME, 'ecl-list-illustration__description')
    pTags = addressDiv.find_elements(By.TAG_NAME, 'p')
    commissioner['address'] = pTags[1].text

    myTeamDiv = driver.find_elements(By.CLASS_NAME, 'ecl-link--secondary')
    commissioner['myTeamsLink'] = myTeamDiv[1].get_attribute('href')
    
teamMembers = []
memberObject = {}
for commissioner in commissionersList:
    driver.get(commissioner['myTeamsLink'])

    wait = WebDriverWait(driver, 10)
    wait.until(EC.visibility_of_element_located(
        (By.CLASS_NAME, "ecl-featured-item__item")))

    addressDiv = driver.find_elements(By.CLASS_NAME, 'ecl-featured-item__item')
    if len(addressDiv) > 1:
        pTags = addressDiv[1].find_elements(By.TAG_NAME, 'p')
    else:
        pTags = addressDiv[0].find_elements(By.TAG_NAME, 'p')
    commissioner['address2'] = pTags[1].text

    teamsDiv = driver.find_elements(
        By.CLASS_NAME, 'ecl-content-item-block__item')
    for member in teamsDiv:
        memberObject['title'] = member.find_element(
            By.CLASS_NAME, 'ecl-content-block__title').text
        userDetails = member.find_elements(
            By.CLASS_NAME, 'ecl-description-list__definition')
        if len(userDetails) > 0:
            memberObject['email'] = userDetails[0].text
        if len(userDetails) > 1:
            memberObject['phone'] = userDetails[1].text
        if len(userDetails) > 2:
            memberObject['responsibilties'] = userDetails[2].text

        memberObject['image'] = member.find_element(
            By.CLASS_NAME, 'ecl-content-item__image').get_attribute('src')

        teamMembers.append(memberObject)
        memberObject = {}

    commissioner['team'] = teamMembers
    teamMembers = []
    memberObject = {}
# Close the webdriver
driver.quit()

# Print the list of commissioners

for commissioner in commissionersList:
    # Update or create the organization document
    query = {'name': commissioner['organization']}
    update = {'$set': {"name": commissioner['organization']}}
    org = organizationsCollection.update_one(query, update, upsert=True)
    
    # Update or create the role document
    query = {'name': commissioner['role']}
    update = {'$set': {"name": commissioner['role']}}
    role = rolesCollection.update_one(query, update, upsert=True)

    # Update or create the commissioner document
    query = {'name': commissioner['name']}
    update = {'$set': commissioner}
    commissionersCollection.update_one(query, update, upsert=True)



client.close()
