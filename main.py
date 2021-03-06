"""
Author: Aidan Duffy
Creation Date: January 2, 2021
Last Updated: January 2, 2021
Description: This program aids swimmers in scheduling/booking lap swim times
for local YMCAs in the northern New Jersey area.
"""
import os
from datetime import date
from datetime import datetime
from datetime import timedelta
import appJar
import requests
import time
from selenium import common
from selenium import webdriver
from selenium.webdriver.support.select import Select

from athlete import *

info_app = appJar.gui("YMCA Sign-in and Personal Info", "800x800")
weekdays = {0: "Monday", 1: "Tuesday", 2: "Wednesday", 3: "Thursday",
            4: "Friday",
            5: "Saturday", 6: "Sunday"}
months = {1:"Jan",2:'Feb',3:'Mar',4:'Apr',5:'May',6:'Jun',
          7:'Jul',8:'Aug',9:'Sep',10:'Oct',11:'Nov',12:'Dec'}


def check_user_info_length():
    """
    This checks the number of lines in the user info file.
    :return: the number of lines in user_info.txt
    """
    user_info = open("user_info.txt", "r")
    info = 0
    for line in user_info:
        info += 1
    user_info.close()
    return info


def check_user_info():
    """
    This checks whether or not the user info file has already been populated
    :return: True or False depending on the file's contents.
    """
    user_info = open("user_info.txt", "r")
    file_len = len(user_info.read())
    user_info.close()
    if file_len != 0:
        user_info = open("user_info.txt", "r")
        info = list()
        for line in user_info:
            info.append(line[:len(line) - 1])
        user_info.close()
        if len(info) != 11:
            if len(info) == 2:
                info_app.stop()
                get_athlete_info()
                check_user_info()
                user_info = open("user_info.txt", "r")
                info = list()
                for line in user_info:
                    info.append(line[:len(line) - 1])
            else:
                return get_barcode_info()
        url = "https://operations.daxko.com/online/5029/checkin?area_id="
        athlete = Athlete(info[0], int(info[1]), info[2], info[3], info[4],
                          info[5], int(info[6]), int(info[7]), info[8],
                          int(info[9]), info[10])
        return athlete
    else:
        return False


def get_barcode_info():
    """
    This asks the user for their sign-in page and barcode ID and populates the
    user info file with that info.
    :return: the athlete object
    """
    info_app.setFont(20)
    info_app.addLabel("title",
                      "Please provide your YMCA and login information")
    info_app.addLabelEntry("Area ID(4-digits at end of Virtual Check In URL)")
    info_app.addNumericLabelEntry("Barcode ID")
    info_app.setFocus("Area ID(4-digits at end of Virtual Check In URL)")

    def press(button):
        """
        This is the function that executes a button push
        :param button: is the button being pressed.
        :param app: is the application
        :return: None
        """
        if button == "Cancel":
            info_app.stop()
        elif button == "Submit":
            user_info = open("user_info.txt", "w")
            while True:
                area_id = info_app.getEntry(
                    "Area ID(4-digits at end of Virtual"
                    " Check In URL)")
                url = "https://operations.daxko.com/online/5029/checkin?" \
                      "area_id=" + area_id
                barcode = int(info_app.getEntry("Barcode ID"))
                barcode = str(barcode)
                try:
                    check_in_page = requests.get(url)
                    check_in_page_content = check_in_page.content
                except requests.exceptions.MissingSchema:
                    print("Error: Please enter a URL!")
                if "operations.daxko.com" not in url:
                    if info_app.retryBox("Error", "You input an invalid URL,"
                                                  " try again!"):
                        info_app.go()
                if len(barcode) < 9:
                    if info_app.retryBox("Error",
                                         "Your barcode is too short!"):
                        info_app.go()
                elif len(barcode) > 9:
                    if info_app.retryBox("Error", "Your barcode is too long!"):
                        info_app.go()
                else:

                    break
            user_info.write(area_id + "\n" + barcode + "\n")
            user_info.close()
            info_app.stop()

    info_app.addButtons(["Submit", "Cancel"], press)
    info_app.go()
    get_athlete_info()
    return check_user_info()


def get_athlete_info():
    """
    This asks the user for their personal info and populates the
    user info file.
    :return: None
    """
    info_app = appJar.gui("Athlete Info", "800x800")
    info_app.setFont(20)
    info_app.addLabel("title",
                      "Please provide your personal information below:")
    user_info = open("user_info.txt", "r")
    info = list()
    for line in user_info:
        info.append(line[:len(line) - 1])
    user_info.close()
    url = "https://operations.daxko.com/online/5029/checkin?area_id=" + info[0]
    page = submit_barcode(url, info[1])
    location_file = open("locations.txt", "r")
    locations = list()
    if len(location_file.read()) == 0:
        location_file = open("locations.txt", "w")
        path, file = os.path.split(os.path.realpath(__file__))
        chrome_path = path + "\\chromedriver.exe"
        driver = webdriver.Chrome(executable_path=chrome_path)
        driver.get(page.url)
        driver.implicitly_wait(1)
        driver.switch_to.frame(driver.find_element_by_xpath("/html/body/div[7]"
                                                            "/div/div[2]/div"
                                                            "[2]/div/div[2]"
                                                            "/p/iframe"))
        driver.implicitly_wait(1)
        selector = Select(driver.find_element_by_id("location"))
        for option in selector.options:
            locations.append(option.text)
            location_file.write(option.text + "\n")
        driver.close()
    else:
        location_file = open("locations.txt", "r")
        for line in location_file:
            locations.append(line)
    location_file.close()
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep",
              "Oct",
              "Nov", "Dec"]
    days = list()
    for i in range(1, 32):
        days.append(i)
    info_app.addLabelOptionBox("Location", locations)
    info_app.addLabelEntry("First Name")
    info_app.addLabelEntry("Last Name")
    info_app.addLabelOptionBox("Birthday Month", months)
    info_app.addLabelOptionBox("Birthday Day", days)
    info_app.addLabelNumericEntry("Birthday Year")
    info_app.addLabelEntry("Email")
    info_app.addLabelNumericEntry("Phone Number(Digits only!)")

    def press_athlete(button):
        """
        This is the function that executes a button push for athlete info
        window
        :param button: is the button being pressed.
        :param app: is the application
        :return: None
        """
        if button == "Cancel":
            info_app.stop()
        elif button == "Submit":
            user_info = open("user_info.txt", "a")
            while True:
                loc = info_app.getOptionBox("Location")
                if loc == "Select Location":
                    if info_app.retryBox("Error", "Please select a valid "
                                                  "location!"):
                        info_app.go()
                first = info_app.getEntry("First Name")
                last = info_app.getEntry("Last Name")
                month = info_app.getOptionBox("Birthday Month")
                day = info_app.getOptionBox("Birthday Day")
                year = int(info_app.getEntry("Birthday Year"))
                if year > 2021 or year < 1921:
                    if info_app.retryBox("Error", "Please enter a valid birth "
                                                  "year!"):
                        info_app.go()
                email = info_app.getEntry("Email")
                if "@" not in email:
                    if info_app.retryBox("Error",
                                         "Please enter a valid email!"):
                        info_app.go()
                number = int(info_app.getEntry("Phone Number(Digits only!)"))
                if len(str(number)) != 10:
                    if info_app.retryBox("Error", "Please enter a valid phone "
                                                  "number!"):
                        info_app.go()
                break
            user_info.write(loc + "\n" + first + "\n" + last + "\n" + month
                            + "\n" + day + "\n" + str(year) + "\n"
                            + email + "\n" + str(number) + "\n" + page.url)
            user_info.close()
            info_app.stop()

    info_app.addButtons(["Submit", "Cancel"], press_athlete)
    info_app.go()


def submit_barcode(url, barcode):
    """
    This returns the YMCA reservation page after inputting the user's barcode.
    :param url: barcode submission page
    :param barcode: is the barcode ID
    :return: the reservation page.
    """
    session = requests.session()
    alt_url = url[:len(url) - 13] + "/submit"
    url_number = url[len(url) - 4:]
    page = session.post(alt_url, data={"area_id": int(url_number),
                                       "barcode": int(barcode)},
                        allow_redirects=True)
    return page


def book_it(tomorrow):
    """
    This uses all of the aggregated data and input of time to book the user's
    next swim time.
    :param tomorrow: True if the program needs to run for the next day.
    :return: None
    """
    reservation = open("res.txt", "r")
    res_time = reservation.readline()[:4]
    reservation.close()
    athlete = check_user_info()
    today = date.today()
    if tomorrow:
        weekday = weekdays[(today.weekday() + 1)%7][:3]
        weekday_int = (today.weekday() + 1) % 7
    else:
        weekday = weekdays[today.weekday()][:3]
        weekday_int = (today.weekday()) % 7
    now = datetime.now()
    current_time = now.strftime("%H%M")
    url = athlete.get_url()
    current_day = now.weekday()
    while current_time != res_time or current_day != weekday_int:
        now = datetime.now()
        current_time = now.strftime("%H%M")
        current_day = now.weekday()
        if current_day != weekday_int:
            time.sleep(18000) #Wait 5 hours
    final_time = now.strftime("%I:%M %p")
    path, file = os.path.split(os.path.realpath(__file__))
    chrome_path = path + "\\chromedriver.exe"
    driver = webdriver.Chrome(executable_path=chrome_path)
    driver.get(url)
    driver.implicitly_wait(5)
    src = driver.find_element_by_xpath("/html/body/div[7]"
                                       "/div/div[2]/div"
                                       "[2]/div/div[2]"
                                       "/p/iframe").get_attribute("src")
    driver.implicitly_wait(5)
    driver.get(src)
    driver.implicitly_wait(5)
    driver.get(src)
    driver.implicitly_wait(5)
    data = {'first_name':athlete.first,'last_name':athlete.last,
            'dob_day':athlete.day,'dob_year':athlete.year,
            'email':athlete.email,'phone':athlete.phone}
    selector = Select(driver.find_element_by_id("location"))
    selector.select_by_visible_text(athlete.location)
    selector = Select(driver.find_element_by_id("dob_month"))
    selector.select_by_visible_text(athlete.month)
    for key in data:
        input_element = driver.find_element_by_id(key)
        input_element.send_keys(data[key])
    input_element.submit()
    driver.implicitly_wait(5)
    res_date = today + timedelta(days=7)
    day = str(res_date.day)
    if len(day) == 1:
        day = "0" + day
    full_date = weekday + ", " + months[res_date.month] + " " + day
    selector = Select(driver.find_element_by_id("date-filter"))
    selector.select_by_visible_text(full_date)
    selector = Select(driver.find_element_by_id("appointment-type-filter"))
    selector.select_by_visible_text("Lap Swimming")
    input_element = driver.find_element_by_xpath("/html/body/div/div/div[1]/"
                                                 "div[2]/input[1]")
    input_element.click()
    if final_time[:1] == "0":
        final_time = final_time[1:]
    if booking(driver, final_time) is False:
        book_it()
    return


def booking(driver, final_time):
    """

    :param driver:
    :return:
    """
    count = 12
    while count > 0:
        time.sleep(2)
        try:
            fieldset = driver.find_element_by_xpath(
                "/html/body/div/div/div[1]/"
                "div[3]/fieldset[" +
                str(count) + "]")
            driver.implicitly_wait(40)
        except common.exceptions.NoSuchElementException:
            count -= 1
            continue
        driver_class = Select(fieldset.find_element_by_class_name("time"))
        times = driver_class.options
        for cur_times in times:
            if final_time == cur_times.text:
                driver_class.select_by_visible_text(final_time)
                driver.implicitly_wait(5)
                submit = fieldset.find_element_by_xpath(
                    "/html/body/div/div/div"
                    "[1]/div[3]/fieldset["
                    + str(count) + "]/table/"
                                   "tbody/tr[5]/td/div"
                                   "/button")
                driver.implicitly_wait(5)
                submit.click()
                time.sleep(10)
                return True
        count -= 1
    return False

def main():
    user_info_len = check_user_info_length()
    athlete = check_user_info()
    if athlete is False:
        athlete = get_barcode_info()
    today = date.today()
    now = datetime.now()
    weekday = weekdays[today.weekday()]
    tomorrow = weekdays[(today.weekday() + 1)%7]
    current_time = now.strftime("%I:%M %p")
    info_app.setFont(20)
    info_app.addLabel("title",
                      "What time next " + weekday + " or " + tomorrow
                      + " after " + current_time +
                      " do\n you want to make your reservation?")
    info_app.addLabelNumericEntry("Time (HHMM, military style)")
    info_app.addCheckBox("Run Tomorrow?")
    current_time_military = now.strftime("%H%M")
    def press_res(button):
        """
        This is the function that executes a button push for athlete info
        window
        :param button: is the button being pressed.
        :param app: is the application
        :return: None
        """
        if button == "Cancel":
            info_app.stop()
        elif button == "Submit":
            while True:
                time = str(int(info_app.getEntry("Time (HHMM, military"
                                                 " style)")))
                tom = info_app.getCheckBox("Run Tomorrow?")
                tom_str = str(tom)
                if len(time) == 3:
                    time = "0" + time
                if len(time) != 4:
                    if info_app.retryBox("Error",
                                         "Please enter a valid time!"):
                        info_app.go()
                hour = time[:2]
                min = time[2:]
                if int(hour) > 23 or int(hour) < 0 or int(min) > 59 or int(
                        min) < 0:
                    if info_app.retryBox("Error",
                                         "Please enter a valid time!"):
                        info_app.go()
                if tom is False and int(hour) <= int(current_time_military[:2])\
                        and int(min) < int(current_time_military[2:]):
                    if info_app.retryBox("Error",
                                         "Please enter a valid time!"):
                        info_app.go()
                break
            reservation = open("res.txt", "w")
            reservation.write(hour + min)
            reservation.write("\n" + tom_str)
            reservation.close()
            info_app.stop()

    info_app.addButtons(["Submit", "Cancel"], press_res)
    info_app.go()
    reservation = open("res.txt", "r")
    res_time = reservation.readline()
    tomorrow = reservation.readline()
    if tomorrow == "False":
        tomorrow = False
    else:
        tomorrow = True
    hour = res_time[:2]
    mins = res_time[2:]
    if int(hour) >= 12:
        am_or_pm = "PM"
        if int(hour) > 12:
            hour = str(int(hour) - 12)
    else:
        am_or_pm = "AM"
    res_time = hour + ":" + mins + " " + am_or_pm
    today_date = int(today.__str__()[-2:])
    today_date += 7
    if today_date < 10:
        res_date = "0" + str(today_date)
    else:
        res_date = str(today_date)
    res_date = today.__str__()[:-2] + res_date
    book_it(tomorrow)


if __name__ == '__main__':
    main()
