from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import DesiredCapabilities
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service as ChromeService
from helium import *
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import *
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
import time

username = "username"
password = "password"

default_options = ["--disable-extensions", "--disable-user-media-security=true",
                   "--allow-file-access-from-files", "--use-fake-device-for-media-stream",
                   "--use-fake-ui-for-media-stream", "--disable-popup-blocking",
                   "--disable-infobars", "--enable-usermedia-screen-capturing",
                   "--disable-dev-shm-usage", "--no-sandbox",
                   "--auto-select-desktop-capture-source=Screen 1",
                   "--disable-blink-features=AutomationControlled"]
headless_options = ["--headless", "--use-system-clipboard",
                    "--window-size=1920x1080"]

def browser_options(chrome_type):
	webdriver_options = webdriver.ChromeOptions()
	notification_opt = {"profile.default_content_setting_values.notifications": 1}
	webdriver_options.add_experimental_option("prefs", notification_opt)

	if chrome_type == "headless":
		var = default_options + headless_options
	else:
		var = default_options

	for d_o in var:
		webdriver_options.add_argument(d_o)
		return webdriver_options

def get_webdriver_instance(browser=None):
	base_url = "https://accounts.teachmint.com/"
	caps = DesiredCapabilities().CHROME
	caps["pageLoadStrategy"] = "normal"
	# driver = webdriver.Chrome(desired_capabilities=caps,executable_path=driver_path(), chrome_options=browser_options(browser))
	# driver = Chrome(service=ChromeService(ChromeDriverManager().install()),
	#                 options=browser_options(browser))
	driver = webdriver.Chrome(options=browser_options(browser))
	driver.command_executor._commands["send_command"] = ("POST",
	                            '/session/$sessionId/chromium/send_com,mand')
	driver.maximize_window()
	driver.get(base_url)
	set_driver(driver)
	return driver


def enter_phone_number_otp(driver, creds):
	driver.find_element("xpath", "//input[@type='text']").send_keys(creds[0])
	time.sleep(1)
	print("entered user phone number {}".format(creds[0]))
	driver.find_element("id", "send-otp-btn-id").click()
	WebDriverWait(driver, 30).until(EC.invisibility_of_element((By.CSS_SELECTOR, "loader")))
	WebDriverWait(driver, 30).until(EC.invisibility_of_element((By.CLASS_NAME, "loader")))
	time.sleep(1)
	_input_otp_field = "//input[@data-group-idx='{}']"

	for i, otp in enumerate(creds[1]):
		otp_field = _input_otp_field.format(str(i))
		write(otp, into=S(otp_field))

	print("entered otp {}".format(creds[1]))
	time.sleep(1)
	driver.find_element("id", "submit-otp-btn-id").click()
	time.sleep(2)

	driver.find_element("xpath", "//img[@alt='arrow']").click()
	WebDriverWait(driver, 30).until( EC.invisibility_of_element((By.CSS_SELECTOR, "loader")))
	WebDriverWait(driver, 30).until( EC.invisibility_of_element((By.CLASS_NAME, "loader")))
	time.sleep(1)
	print("successfully entered user phone number and otp")

def Navigating_To_Certificates(driver):
	WebDriverWait(driver, 30).until(EC.invisibility_of_element((By.CSS_SELECTOR, "loader")))
	WebDriverWait(driver, 30).until(EC.invisibility_of_element((By.CLASS_NAME, "loader")))
	time.sleep(1)
	action = ActionChains(driver)
	dashboard = driver.find_element("xpath",'//span[@data-qa="icon-dashboard1"]')
	time.sleep(2)
	action.move_to_element(dashboard).perform()
	administration = driver.find_element("xpath",'//span[@data-qa="icon-administrator"]')
	action.click(administration).perform()
	time.sleep(2)
	certificate = driver.find_element("xpath","//a[text()='Certificates']")
	action.click(certificate).perform()
	print("navigated to the certificate")

def select_certificate(driver):
	driver.implicitly_wait(2)
	driver.find_element("xpath", "(//div[@class='Cards_templateList__2UnqV'])[2]/..//h6[text()='School leaving certificate']").click()
	time.sleep(10)
	print("school_leaving_certificate_is_selected")

def click_on_generate(driver):
	driver.implicitly_wait(2)
	driver.find_element("xpath","//div[text()='Generate']").click()
	print("generator is clicked")

def search_select_student(driver):
	driver.implicitly_wait(2)
	driver.find_element("xpath","//input[@name='search']").send_keys("sam")
	driver.find_element("xpath","//div[text()='Generate']").click()
	print("sam is selected")

def update_remark(driver):
	driver.find_element("xpath", '//div[@class="krayon__TextInput-module__2hxFp"]//input[@placeholder="Remarks"]').send_keys(10)
	time.sleep(1)
	driver.find_element("xpath", "//div[text()='Generate']").click()
	time.sleep(1)
	print("remark is generated")
	time.sleep(2)



def download(driver):
	driver.implicitly_wait(2)
	driver.find_element("xpath", "//div[@data-qa='popup']//div[text()='Download']").click()
	print("downloaded is done")


def validate(driver):
	driver.implicitly_wait(2)
	displayed_file = driver.find_element("xpath", "//p[text()='School leaving certificate']").is_displayed()
	assert displayed_file, 'it is not displayed'
	print("validation is done")


def login(admin_credentials=["0000020232", "120992", "@Automation-2"], account_name="@Automation-2"):
	driver = get_webdriver_instance()
	driver.implicitly_wait(5)
	WebDriverWait(driver, 30).until(EC.invisibility_of_element((By.CSS_SELECTOR, "loader")))
	WebDriverWait(driver, 30).until(EC.invisibility_of_element((By.CLASS_NAME, "loader")))
	time.sleep(1)
	enter_phone_number_otp(driver, admin_credentials)
	# user_name = "//div[@class='profile-user-name']/..//div[text()=' + account_name +']"
	# WebDriverWait(driver, 30).until(EC.element_to_be_clickable(("XPATH", user_name)))
	# driver.find_element("xpath", user_name).click()
	# driver.find_element("xpath", user_name).click()

	dashboard_xpath = "//a[text()='Dashboard']"
	WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, dashboard_xpath)))
	# time.sleep(10)
	refresh()
	Navigating_To_Certificates(driver)
	# time.sleep(2)
	select_certificate(driver)
	click_on_generate(driver)
	# time.sleep(3)
	search_select_student(driver)
	time.sleep(2)
	update_remark(driver)
	time.sleep(2)
	download(driver)
	time.sleep(2)
	validate(driver)
	return driver



def main():
	driver = login()


if __name__ == "__main__":
	print("start")
	main()
	print("end")

