import re
import time

import undetected_chromedriver
from selenium.common import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from db import insert_number
from tg import send_notification

driver = undetected_chromedriver.Chrome()

driver.get(
    '''https://www1.pinnacle.com/en/casino''')
time.sleep(120)  # Логинимся, переходим во вкладку в 'Aviator'

last_number = None
nums = []
last_sent_number = None
print_nums = None
last_num_clicked = None

while True:
    try:
        iframe = driver.find_element(By.ID, "GameflexWidget-1")
        driver.switch_to.frame(iframe)
        time.sleep(0.5)

        iframe_1 = driver.find_element(By.ID, "GameObjectContainer")
        driver.switch_to.frame(iframe_1)
        time.sleep(0.3)

        iframe_2 = driver.find_element(By.XPATH, "//iframe[contains(@src, 'https://aviator-next.spribegaming.com')]")
        driver.switch_to.frame(iframe_2)
        time.sleep(0.4)

        try:
            element = driver.find_element(By.CSS_SELECTOR, 'app-bubble-multiplier.payout')
            element.click()
            time.sleep(0.4)

            # Получаем число
            try:
                element = driver.find_element(By.CLASS_NAME, 'modal-content')
                html = element.get_attribute('innerHTML')
                match = re.search(r'([\d.]+)x', html)

                if match:
                    number = float(match.group(1))
                    last_number = nums[-1] if nums else None
                    if last_number is None or number != last_number:
                        insert_number(number)
                        nums.append(number)
                    if len(nums) > 3:
                        nums = nums[-3:]

                    # Проверяем условие: все числа в списке меньше 1.5 (Можно выставить свои требования)
                    if all(x < 1.2 for x in nums) and last_sent_number != number:
                        # Отправляем уведомление только если оно еще не было отправлено для текущего числа
                        send_notification(f"Условие выполнено")
                        last_sent_number = number
                        time.sleep(0.3)
                        actions = ActionChains(driver)
                        actions.send_keys(Keys.ESCAPE).perform()
                        time.sleep(0.3)
                        # Пожатие ставки
                        button = driver.find_element(By.CLASS_NAME, 'buttons-block')
                        button.click()
                        last_num_clicked = number
                        print(nums)
                        time.sleep(0.3)
            except NoSuchElementException as e:
                print("Не удалось найти modal-content")
                time.sleep(0.4)

        except NoSuchElementException as e:
            print("Не удалось найти элемент app-bubble-multiplier.payout")
            time.sleep(0.4)

        actions = ActionChains(driver)
        actions.send_keys(Keys.ESCAPE).perform()
        print(nums)
        time.sleep(0.3)
        driver.switch_to.default_content()

    except Exception as e:
        print(f"Произошла ошибка: {e}")
        time.sleep(0.3)
        continue
