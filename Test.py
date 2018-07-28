from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from datetime import date
from time import sleep
from tqdm import tqdm
from dateutil import parser
import re
import sys
reload(sys)
sys.setdefaultencoding('utf8')

list_of_criminals = []

driver = webdriver.Chrome(executable_path=r"C:\new\chromedriver.exe")
driver.get('http://199.242.69.70/pls/ds/ds_docket_search')
f = open('courtresults.csv','w')

counties_of_commitment = {'ALL': 0,
                          'ALACHUA': 1,
                          'BAKER': 2,
                          'BAY': 3,
                          'BRADFORD': 4,
                          'BREVARD' : 5,
                          'BROWARD': 6,
                          'CALHOUN': 7,
                          'CHARLOTTE': 8,
                          'CITRUS': 9,
                          'CLAY': 10,
                          'COLLIER': 11,
                          'COLUMBIA': 12,
                          'DESOTO': 13,
                          'DIXIE': 14,
                          'DUVAL': 15,
                          'ESCAMBIA': 16,
                          'FLAGLER': 17,
                          'FRANKLIN': 18,
                          'GADSDEN': 19,
                          'GILCHRIST': 20,
                          'GLADES': 21,
                          'GULF': 22,
                          'HAMILTON': 23,
                          'HARDEE': 24,
                          'HENDRY': 25,
                          'HERNANDO': 26,
                          'HIGHLANDS': 27,
                          'HILLSBOROUGH': 28,
                          'HOLMES': 29,
                          'INDIAN RIVER': 30,
                          'JACKSON': 31,
                          'JEFFERSON': 32,
                          'LAFAYETTE': 33,
                          'LAKE': 34,
                          'LEE': 35,
                          'LEON': 36,
                          'LEVY': 37,
                          'LIBERTY': 38,
                          'MADISON': 39,
                          'MANATEE': 40,
                          'MARION': 41,
                          'MARTIN': 42,
                          'MIAMI-DADE': 43,
                          'MONROE': 44,
                          'NASSAU': 45,
                          'OKALOOSA': 46,
                          'OKEECHOBEE': 47,
                          'ORANGE': 48,
                          'OSCEOLA': 49,
                          'PALM BEACH': 50,
                          'PASCO': 51,
                          'PINELLAS': 52,
                          'POLK': 53,
                          'PUTNAM': 54,
                          'SANTA ROSA': 55,
                          'SARASOTA': 56,
                          'SEMINOLE': 57,
                          'ST. JOHNS': 58,
                          'ST. LUCIE': 59,
                          'SUMTER': 60,
                          'SUWANNEE': 61,
                          'TAYLOR': 62,
                          'UNION': 63,
                          'VOLUSIA': 64,
                          'WAKULLA': 65,
                          'WALTON': 66,
                          'WASHINGTON': 67}

class Criminal(object):
    """holds data for each individual criminal"""
    def __init__(self,full_name,first_name,last_name,type_of_appeal,county,case_number,date_of_filing,link_to_page,
                 race=None,sex=None,dc_number=None,hair_color=None,eye_color=None,height=None,weight=None,birth_date=None,
                 initial_receipt_date=None,current_facility=None,current_custody=None,current_release_date=None,relevant_actions=None):
        self.full_name = full_name
        self.first_name = first_name
        self.last_name = last_name
        self.type_of_appeal = type_of_appeal
        self.county = county
        self.case_number = case_number
        self.date_of_filing = date_of_filing
        self.link_to_page = link_to_page
        self.relevant_actions = []
        self.race = None
        self.sex = None
        self.dc_number = None
        self.hair_color = None
        self.eye_color = None
        self.height = None
        self.weight = None
        self.birth_date = None
        self.initial_receipt_date = None
        self.current_facility = None
        self.current_custody = None
        self.current_release_date = None



class Scraper(object):
    def __init__(self,driver):
        self.driver = driver
        self.links_to_cases = []
        self.dict_of_cases = {}

    def initial_url_grab(self):
        search_by = driver.find_element_by_xpath('/html/body/table[2]/tbody/tr/td[2]/table[3]/tbody/tr[2]/td[2]/select')
        search_by.click()
        search_by.send_keys('d')
        search_by.send_keys(Keys.TAB)
        sleep(1)
        
    def date_checker(self):
        """Finds the date, and sets the number of scrolls for day/month.."""
        todays_date = date.today()
        todays_date = str(todays_date)
        todays_date_split = todays_date.split('-')
        self.year,self.month,self.day = int(todays_date_split[0]), int(todays_date_split[1]),int(todays_date_split[2])
        if self.year==2016:
            self.is_2016 = True
        elif self.year!=2016:
            self.is_2016 = False
        self.number_of_scrolls_month = self.month
        self.number_of_scrolls_day = self.day - 2

    def date_and_court(self,court_number):
        court_selector = driver.find_element_by_xpath('/html/body/table[2]/tbody/tr/td[2]/table[3]/tbody/tr[2]/td[3]/select')
        court_selector.click()
        if court_number == 1:
            court_selector.send_keys(Keys.DOWN)
            court_selector.send_keys(Keys.TAB)
        elif court_number == 2:
            court_selector.send_keys(Keys.DOWN)
            court_selector.send_keys(Keys.DOWN)
            court_selector.send_keys(Keys.TAB)
        elif court_number == 3:
            court_selector.send_keys(Keys.DOWN)
            court_selector.send_keys(Keys.DOWN)
            court_selector.send_keys(Keys.DOWN)
            court_selector.send_keys(Keys.TAB)
        elif court_number == 4:
            court_selector.send_keys(Keys.DOWN)
            court_selector.send_keys(Keys.DOWN)
            court_selector.send_keys(Keys.DOWN)
            court_selector.send_keys(Keys.DOWN)
            court_selector.send_keys(Keys.TAB)
        sleep(0.5)
        month_selector = driver.find_element_by_xpath('/html/body/table[2]/tbody/tr/td[2]/table[3]/tbody/tr[4]/td[2]/font[1]/select')
        month_selector.click()
        month_selector.send_keys(Keys.DOWN * (self.number_of_scrolls_month - 1))
        month_selector.click()
        sleep(0.5)
        days_selector = driver.find_element_by_id('pdtStartDate2')
        days_selector.click()
        days_selector.send_keys(Keys.DOWN * (self.number_of_scrolls_day - 1))
        days_selector.click()
        submit_button = driver.find_element_by_name('psButton').click()

    def search_thru_cases(self):
        all_links = driver.find_elements_by_tag_name('a')
        for i in all_links:
            if 'ds_docket?' in i.get_attribute('href'):
                self.links_to_cases.append(i.get_attribute('href'))

    def scrape_individual_cases(self):
        for _ in tqdm(self.links_to_cases):
            driver.get(_)
            html = driver.page_source
            soup = BeautifulSoup(html,'lxml')
            headers = soup.find_all('h3')
            temporary_relevant_actions = []
            final_criminal_judgement_area = driver.find_element_by_xpath('/html/body/table[2]/tbody/tr/td[2]/center[2]/h3').text
            if 'Final Criminal Judgment and Sentence Notice' in final_criminal_judgement_area or 'Final Criminal 3.8' in final_criminal_judgement_area:
                type_of_appeal = final_criminal_judgement_area.replace('  ','')
                type_of_appeal_parsed = re.search('(Final Criminal .*) from .*',type_of_appeal)
                type_of_appeal_final = type_of_appeal_parsed.group(1)
                table_of_actions = soup.find('table',{'width':'100%','border':'1','cellpadding':'1','cellspacing':'0'})
                for row in table_of_actions.find_all("tr")[1:]:  # skipping header row
                    cells = row.find_all("td")
                    date_of_action, type_of_action = cells[0].text, cells[1].text # retrieve table contents
                    if 'Initial Brief on the Merits' in type_of_action:
                        temporary_relevant_actions.append((date_of_action,type_of_action))
                    elif 'Answer Brief' in type_of_action:
                        temporary_relevant_actions.append((date_of_action,type_of_action))
                    elif 'Affirmed' in type_of_action:
                        temporary_relevant_actions.append((date_of_action,type_of_action))
                    elif 'Mandate' in type_of_action:
                        temporary_relevant_actions.append((date_of_action,type_of_action))
                link_to_page = str(driver.current_url)
                county = re.search('from(.*)',final_criminal_judgement_area)
                county_parsed = county.group(1)
                case_number = driver.find_element_by_xpath('/html/body/table[2]/tbody/tr/td[2]/center[1]/h3/b/font').text
                name = driver.find_element_by_xpath('/html/body/table[2]/tbody/tr/td[2]/center[3]/h3').text
                name_parsed = re.search('(.*)vs.*',name)
                name_final = name_parsed.group(1)
                notice_of_appeal_filed = soup.find_all('td',{'valign':'top'})
                county_parsed = county_parsed.strip()
                county_parsed_final = county_parsed.replace('County','')
                try:
                    h4_tag = soup.find('h4').text
                    h4_tag = h4_tag.replace('\n','')
                    if 'Lower Tribunal Case' in h4_tag:
                        lower_tribunal_case_number =  h4_tag.replace('Lower Tribunal Case(s):               ','')
                    else:
                        continue
                except:
                    continue
                for i in notice_of_appeal_filed:
                    if i.text == 'Notice of Appeal Filed':
                        date_of_filing = i.find_previous_sibling()
                        date_of_filing = date_of_filing.text
                    else:
                        continue
                self.dict_of_cases[str(name_final)] = [str(county_parsed_final),str(case_number),str(date_of_filing.replace('\n','')),str(type_of_appeal_final)]
                list_of_criminals.append(Criminal(name_final,'null','null',type_of_appeal_final,county_parsed_final,str(case_number),date_of_filing.replace('\n',''),link_to_page,temporary_relevant_actions))
        
    def department_of_corrections_scraper(self):
        for key,value in tqdm(self.dict_of_cases.iteritems()):
            driver.get('http://www.dc.state.fl.us/activeinmates/search.asp')
            list_of_names = key.split()
            first_name = list_of_names[0]
            last_name = list_of_names[-1]
            last_name_input_field = driver.find_element_by_name('lastname')
            last_name_input_field.send_keys(last_name)
            first_name_input_field = driver.find_element_by_name('firstname')
            first_name_input_field.send_keys(first_name)
            for county, number_of_downs in counties_of_commitment.iteritems():
                if county in self.dict_of_cases[key][0].upper():
                    commitment_county_item = driver.find_element_by_id('commitmentcounty')
                    commitment_county_item.click()
                    commitment_county_item.send_keys(Keys.DOWN * (number_of_downs - 3))
                else:
                    continue
            submit_button_click = driver.find_element_by_xpath('//*[@id="dcCSScontentContainer"]/div/form/input[2]').click()
            associated_links = driver.find_elements_by_tag_name('a')
            correct_links = []
            for link in associated_links:
                if 'detail.asp?' in link.get_attribute('href'):
                    correct_links.append(link.get_attribute('href'))
            correct_links = list(set(correct_links))
            if 0<len(correct_links)>1:
                print 'more than one prisoner found'
                break
            else:
                print'continuing to DOC page..'
            try:
                driver.get(correct_links[0])
            except IndexError:
                continue
            full_page = driver.page_source
            soup = BeautifulSoup(full_page,'lxml')
            left_tds = soup.find_all('td',{'align':'LEFT', 'width':"60%"})
            left_tds_text = [i.text for i in left_tds]
            for i in list_of_criminals:
                if first_name in i.full_name:
                    i.sex = left_tds_text[3]
                    i.first_name = first_name
                    i.last_name = last_name
                    i.dc_number = left_tds_text[0]
                    i.race = left_tds_text[2]
                    i.hair_color = left_tds_text[4]
                    i.eye_color = left_tds_text[5]
                    i.height = left_tds_text[6]
                    i.weight = left_tds_text[7]
                    #birth_date_date_time = parser.parse(left_tds_text[8])
                    i.birth_date = left_tds_text[8]
                    i.initial_receipt_date = left_tds_text[9]
                    i.current_facility = driver.find_element_by_xpath('//*[@id="dcCSScontentContainer"]/div/table[2]/tbody/tr/td[2]/table/tbody/tr[11]/td[2]').text
                    i.current_custody = left_tds_text[11]
                    try:
                        i.current_release_date = left_tds_text[12]
                    except IndexError:
                        i.current_release_date = left_tds_text[-1]


for i in range(1, 4):
    driver.get('http://199.242.69.70/pls/ds/ds_docket_search')
    s = Scraper(driver)
    s.initial_url_grab()
    s.date_checker()
    s.date_and_court(i)
    s.search_thru_cases()
    s.scrape_individual_cases()
    s.department_of_corrections_scraper()
driver.close()

for i in tqdm(list_of_criminals):
    print 'writing criminal #{0}'.format(list_of_criminals.index(i))
    f.write(i.full_name)
    f.write('|')
    f.write(i.first_name)
    f.write('|')
    f.write(i.last_name)
    f.write('|')
    f.write(i.type_of_appeal)
    f.write('|')
    f.write(i.county)
    f.write('|')
    f.write(i.case_number)
    f.write('|')
    f.write(i.date_of_filing)
    f.write('|')
    f.write(str(i.race))
    f.write('|')
    f.write(str(i.sex))
    f.write('|')
    f.write(str(i.dc_number))
    f.write('|')
    f.write(str(i.hair_color))
    f.write('|')
    f.write(str(i.eye_color))
    f.write('|')
    f.write(str(i.height))
    f.write('|')
    f.write(str(i.weight))
    f.write('|')
    f.write(str(i.birth_date))
    f.write('|')
    f.write(str(i.initial_receipt_date))
    f.write('|')
    f.write(str(i.current_facility))
    f.write('|')
    f.write(str(i.current_custody))
    f.write('|')
    f.write(str(i.current_release_date))
    f.write('|')
    f.write(str(i.link_to_page))
    f.write('\n')