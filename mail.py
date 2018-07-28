import csv
import datetime
import requests
from bs4 import BeautifulSoup

date = str(datetime.datetime.today())
todays_date = date.split(' ')[0]
headers = {"Content-Type": "application/xml"}
address_list_ids = []
job_ids = []
index= [0]
#login_info = open('login_info.txt', 'r').read()
#if len(login_info) > index: 
#	username, password = login_info.split(',')[0], login_info.split(',')[1]
global username
username='dmlamos'
global password
password='ylWni826'
court_results = open('courtresults.csv', 'r')


class Request_Handler():
    """Handles the different types of requests that one can make to
    the click2mail API.  Data is an optional argument that will carry
    the parameters of a post request (if any) to their delivery place!"""

    def handler(self, request_type, link, data=None):
        if request_type == 'GET':
            if not data:
                r = requests.get(link, headers=headers)
                soup = BeautifulSoup(r.content, 'html.parser')
                return soup
            else:
                r = requests.get(link, headers=headers, data=data)
                soup = BeautifulSoup(r.content, 'html.parser')
                return soup
        elif request_type == 'POST':
            r = requests.post(link, headers=headers, data=data)
            soup = BeautifulSoup(r.content, 'html.parser')
            return soup

r = Request_Handler()


def authenticate():
    """Authenticates the user given a text file."""
    soup = r.handler(
        'POST', 'https://{0}:{1}@rest.click2mail.com/molpro/account/authorize'.format(username, password))
    if soup.find('status').text == '0':
        print('Successfully authenticated!')


def create_project(project_name):
    """Given a project_name, this method creates a project and
    returns the Project ID to be worked on from there."""
    payload = {'projectName': project_name}
    soup = r.handler(
        'POST', 'https://{0}:{1}@rest.click2mail.com/molpro/projects'.format(username, password),
        data=payload)
    if 'Created' in soup.find('description'):
        print('Project {0} successfully created.'.format(project_name))
    else:
        print('Error: {0}'.format(soup.find('description').text))
    project_id = soup.find('id').text
    return project_id


def retrieve_jobs_in_project(project_name):
    payload = {'projectName': project_name}
    soup = r.handler(
        'GET', 'https://{0}:{1}@rest.click2mail.com/molpro/projects/jobs/'.format(username, password),
        data=payload)
    print(soup)


def retrieve_project_list():
    payload = {'numberOfProjects': '1'}
    soup = r.handler(
        'GET', 'https://{0}:{1}@rest.click2mail.com/molpro/projects'.format(username, password),
        data=payload)
    print(soup.prettify())


def retrieve_document_list():
    payload = {'numberOfDocuments': '10'}
    soup = r.handler(
        'GET', 'https://{0}:{1}@rest.click2mail.com/molpro/documents'.format(username, password))
    print(soup.prettify())

def create_job_from_template():
    payload = {'addressId': 946961,
               'jobtemplateId': 485877}
    soup = r.handler(
        'POST', 'https://{0}:{1}@rest.click2mail.com/molpro/jobs/template'.format(username, password),
        data=payload)
    print(soup.prettify())


def create_address_list(first_name, last_name, dc_number,
                        prison_name, street_address, city,
                        state, zip_code):
    r = requests.post('https://ntucker1:5i9j1rKu@rest.click2mail.com/molpro/addressLists',
                       headers=headers,
                       data="""<addressList>
    <addressListName>{0} Prisoner</addressListName>
    <addressMappingId>2</addressMappingId>
    <addresses>
    <address>
      <First_name>{1}</First_name>
      <Last_name>{2}</Last_name>
      <Organization>{3}</Organization>
      <Address1>{4}</Address1>
      <Address2>{5}</Address2>
      <Address3></Address3>
      <City>{6}</City>
      <State>{7}</State>
      <Zip>{8}</Zip>
      <Country_non-US></Country_non-US>
    </address>
    </addresses>
    </addressList>""".format(date, first_name, last_name, dc_number,
                         prison_name, street_address, city,
                         state, zip_code))


def retrieve_todays_address_lists(todays_date):
    r = requests.get('https://ntucker1:5i9j1rKu@rest.click2mail.com/molpro/addressLists',
                     data= {'searchkey': todays_date})
    soup = BeautifulSoup(r.content, 'html.parser')
    for i in soup.find_all('id'):
        address_list_ids.append(i.text)


def create_job_from_template(address_list):
    payload = {'addressId': address_list,
               'jobtemplateId': 485877}
    soup = r.handler(
        'POST', 'https://{0}:{1}@rest.click2mail.com/molpro/jobs/template'.format('ntucker1', '5i9j1rKu'),
        data=payload)
    job_ids.append(soup.find('id').text)


def submit_a_job(job_id):
    payload = {'billingType': 'User Credit'}
    soup = r.handler(
        'POST', 'https://{0}:{1}@rest.click2mail.com/molpro/jobs/{2}/submit'.format(username, password, job_id),
        data=payload)
    print(soup.prettify())


def job_cost_estimate(job_id):
    soup = r.handler(
        'GET', 'https://{0}:{1}@rest.click2mail.com/molpro/jobs/{2}/cost'.format(username, password, job_id))
    print(soup.prettify())

authenticate()
csv_reader = csv.reader(court_results, delimiter='|')
for row in csv_reader:
	try:
		first_name = row[1]
		last_name = row[2]
		dc_number = row[9].replace('Â ', '')
		if dc_number:
			create_address_list(first_name, last_name, dc_number, 'prison_name,', 'street', 'city', 'state', 'zip')
	except IndexError:
		pass
#create_project()
#create_address_list('nick', 'tucker', 'org', 'address', 'address', 'NY', 'ny', '13045')
#project_id = create_project('ijsidsa')
#print(project_id)
#retrieve_jobs_in_project('June 2016')
#retrieve_project_list()
#retrieve_document_list()
retrieve_todays_address_lists(todays_date)
for i in address_list_ids:
    create_job_from_template(i)
for job in job_ids:
    job_cost_estimate(job)
for job in job_ids:
    submit_a_job(job)