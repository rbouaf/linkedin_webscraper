import linkedinparameters
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from parsel import Selector
from selenium.common.exceptions import InvalidArgumentException
import csv
import selenium

'''

--------------------------------  T H I N G S    T O    C O N S I D E R  --------------------------------

1. THIS WEBSCRAPER WAS MADE ON July ‎3rd, ‎2020. It may not function anymore, depending on when you run it. 
EDIT: It is October 19th 2020, and it still works. 

2. YOU NEED TO INSTALL CHROMEDRIVER TO RUN THIS CODE. 
MAKE SURE YOU INSTALL IT FOR THE RIGHT VERSION OF CHROME (YOURS) (You can check this by going opening Google Chrome and going in Help > About Chrome).
IT IS FREE TO DOWNLOAD.

3. As of July 3rd 2020 (and now as of 19-10-2020), when you open linkedin.com, there are 2 different versions of the site that can appear. 
This is completely random, as far as I'm aware. The code only works with one version of the site. 
If the code gives you an error during the login phase, just close the window and re-run the code until you get the different site.

4. This webscraper has issues returning phone numbers. I would consider commenting out the phone part of the code. 

5. At lines 47, 51 and 55, you are asked to give:
- a path to ChromeDriver, this will change depending on where you installed ChromeDriver



'''

################ CHECKS IF A FIELD IS EMPTY AND RETURNS "NO RESULTS" IF IT IS. ################
def validate_field(field):
	if field:
		return field
	else:
		field = 'No results'
		return field


####################### CREATES THE EXCEL FILE WE WILL PUT THE DATA IN. #######################

writer = csv.writer(open(linkedinparameters.file_name, 'w'))
writer.writerow(['First name','Last name','Job Title','Company', 'Location','Email','Phone number', 'URL'])


########################### OPENS CHROME, OPENS LINKEDIN, LOGS IN. ############################

driver = webdriver.Chrome(executable_path=linkedinparameters.chromedriver_path)
driver.get('https://www.linkedin.com')

username = driver.find_element_by_id('session_key')
username.send_keys(linkedinparameters.linkedin_username)
sleep(0.5)

password = driver.find_element_by_id('session_password')
password.send_keys(linkedinparameters.linkedin_password)
sleep(0.5)

log_in_button = driver.find_element_by_class_name('sign-in-form__submit-button')
log_in_button.click()
sleep(0.5)

############################### GOES TO THE CONTACTS LIST PAGE ################################

driver.get('https://www.linkedin.com/mynetwork/invite-connect/connections/')
sleep(4)



#################################### GETTING ALL CONTACTS #####################################
all_contacts = driver.find_elements_by_css_selector('a[data-control-name="connection_profile"]')

all_contact_links = [contact.get_attribute('href') for contact in all_contacts]
all_contact_links = list(set(all_contact_links))


##################### EVERYTHING HAPPENS IN THIS SINGLE CODE BLOCK. R A W #####################

for contact_url in all_contact_links:
   
   driver.get(contact_url)
   sleep(2)



   sel = Selector(text=driver.page_source)

   name = sel.xpath('//*[starts-with(@class, "inline t-24 t-black t-normal break-words")]/text()').extract_first()
   if name:
      name = name.strip()
   FirstName = name.split()[0]
   LastName = name.split()[1]

   job_title = sel.xpath('//*[starts-with(@class, "mt1 t-18 t-black t-normal break-words")]/text()').extract_first()
   if job_title:
      job_title = job_title.strip()

   company = sel.xpath('//*[starts-with(@class,"text-align-left ml2 t-14 t-black t-bold full-width lt-line-clamp lt-line-clamp--multi-line ember-view")]/text()').get()
   if company:
      company = company.strip()

   location = sel.xpath('//*[starts-with(@class, "t-16 t-black t-normal inline-block")]/text()').extract_first()
   if location:
      location = location.strip()



   linkedin_url = driver.current_url
   sleep(3)


   contact_info = driver.find_element_by_xpath('//*[starts-with(@data-control-name, "contact_see_more")]')
   contact_info.click()
   contact_info.click()
   contact_info.click() #sometimes it doesn't click right away, so I got frustrated while writing the code.
   sleep(3)

   sel2 = Selector(text=driver.page_source)

   email = sel2.xpath('//*[@class = "pv-contact-info__contact-link t-14 t-black t-normal" and @rel="noopener noreferrer"]/text()').extract_first()
   if email:
      email = email.strip()

   # SOMETIMES THIS DOESN'T WORK AND I CAN'T FIGURE OUT WHY. 
   # SOMETIMES IT DOESN'T RETURN THE PHONE NUMBER AND RETURNS GIBBERISH. 
   # BE CAREFUL, MIGHT WANT TO COMMENT IT OUT
   phone = sel2.xpath('//*[@class = "t-14 t-black t-normal"]/text()').extract_first()
   if phone:
      phone = phone.strip()

   sleep(3)

   # CHECKING IF NO VALUE IS RETURNED, AND RETURNS "NO RESULTS" IF SO. SEE CODE AT THE VERY TOP.
   FirstName = validate_field(FirstName)
   LastName = validate_field(LastName)
   job_title = validate_field(job_title)
   company = validate_field(company)
   location = validate_field(location)
   email = validate_field(email)
   phone = validate_field(phone)
   linkedin_url = validate_field(linkedin_url)


   # PRINT RESULTS INTO CONSOLE
   print('\n')
   print('First name: ' + FirstName)
   print('Last name: ' + LastName)
   print('Job Title: ' + job_title)
   print('Company: ' + company)
   print('Location: ' + location)
   print('Email: ' + email)
   print('Phone number: '+ phone)
   print('URL: ' + linkedin_url)
   print('\n')

   # ENCODING SO IT CAN BE EXPORTED INTO THE EXCEL FILE
   FirstName.encode('utf-8')
   LastName.encode('utf-8')
   job_title.encode('utf-8')
   company.encode('utf-8')
   location.encode('utf-8')
   email.encode('utf-8') 
   phone.encode('utf-8') 
   linkedin_url.encode('utf-8')

   #THIS PUTS IT IN THE EXCEL FILE
   writer.writerow([FirstName, LastName, job_title, company, location, email, phone, linkedin_url])

##########################################

driver.quit()
