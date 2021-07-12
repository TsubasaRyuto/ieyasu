from config.settings import SETTINGS
import time
import datetime
from distutils.util import strtobool
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

dt_now = datetime.datetime.now()

driver = webdriver.Chrome()
driver.get(SETTINGS['ieyasu_url'])
wait = WebDriverWait(driver, 10)

# ログイン処理
wait.until(
    EC.visibility_of_element_located((By.ID, 'user_login_id'))
)
login_id_element = driver.find_element_by_id('user_login_id')
login_id_element.send_keys(SETTINGS['login_id']) # ここは変数の値を入れる

login_pass_element = driver.find_element_by_id('user_password')
login_pass_element.send_keys(SETTINGS['login_pass'])

submit_login = driver.find_element_by_name('Submit')
submit_login.click()

# 日時勤怠ページ
wait.until(
    EC.visibility_of_element_located((By.ID, 'work_navi'))
)
work_navi = driver.find_element_by_id('work_navi')
work_navi.click()

# 月選択
# select_month = driver.find_element_by_id('select')
# select_month_element = Select(select_month)
# select_month_element.select_by_value(dt_now.strftime('%Y-%m'))



# 登録処理
attendance_table = driver.find_element_by_id("editGraphTable")

table_body = attendance_table.find_element_by_tag_name("tbody")
table_trs = table_body.find_elements_by_tag_name('tr')

attendance_page_infos = []
for tr in table_trs:
    dictionaly = { 'work_start': '', 'work_end': '', 'url': '' }
    status = tr.find_element_by_class_name('cellType').find_element_by_class_name('item02').text
    if status == '出勤':
        date_element = tr.find_element_by_class_name('cellDate')

        if len(date_element.find_element_by_class_name('view_work').find_elements_by_tag_name('a')) > 0:
            dictionaly['url'] = date_element.find_element_by_class_name('view_work').find_element_by_tag_name('a').get_attribute('href')
            attendance_page_infos.append(dictionaly)
        else:
            continue

        day = date_element.find_element_by_class_name('day').text
        if day == '月' or SETTINGS['only_9_oclock']:
            dictionaly['work_start'] = SETTINGS['work_start1']
            dictionaly['work_end'] = SETTINGS['work_end1']
        else:
            dictionaly['work_start'] = SETTINGS['work_start2']
            dictionaly['work_end'] = SETTINGS['work_end2']


for info in attendance_page_infos:
    driver.get(info['url'])
    wait.until(
        EC.text_to_be_present_in_element((By.TAG_NAME, 'h1'), '日次勤怠')
    )

    # 出退勤
    login_id = driver.find_element_by_id('work_start_at_str')
    login_id.send_keys(info['work_start'])
    login_id = driver.find_element_by_id('work_end_at_str')
    login_id.send_keys(info['work_end'])

    # 休憩
    login_id = driver.find_element_by_id('work_break_1_start_at_str')
    login_id.clear()
    login_id.send_keys(SETTINGS['break_start'])
    login_id = driver.find_element_by_id('work_break_1_end_at_str')
    login_id.clear()
    login_id.send_keys(SETTINGS['break_end'])

    register_submit = driver.find_element_by_name('add_application')
    register_submit.click()

driver.close()
