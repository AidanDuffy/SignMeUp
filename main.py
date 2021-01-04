"""
Author: Aidan Duffy
Creation Date: January 2, 2021
Last Updated: January 2, 2021
Description: This program aids swimmers in scheduling/booking lap swim times
for local YMCAs in the northern New Jersey area.
"""
import os

import appJar
import requests
from selenium import webdriver
from selenium.webdriver.support.select import Select

from athlete import Athlete

info_app = appJar.gui("YMCA Sign-in and Personal Info", "800x800")

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
        if len(info) != 10:
            if len(info) == 2:
                info_app.stop()
                get_athlete_info()
                check_user_info()
            else:
                return get_barcode_info()
        url = "https://operations.daxko.com/online/5029/checkin?area_id="
        athlete = Athlete(info[0], int(info[1]), info[2], info[3], info[4],
                          int(info[5]), int(info[6]), int(info[7]), info[8],
                          info[9])
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
                url = "https://operations.daxko.com/online/5029/checkin?area_id=" \
                      + area_id
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
    info_app = appJar.gui("Athlete Info", "600x600")
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
        driver.switch_to.frame(driver.find_element_by_xpath("/html/body/div[7]/"
                                                            "div/div[2]/div[2]/"
                                                            "div/div[2]/p/iframe"))
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
    info_app.addLabelOptionBox("Location", locations)
    info_app.addLabelEntry("First Name")
    info_app.addLabelEntry("Last Name")
    info_app.addLabelSpinBoxRange("Birthday Month", 1, 12)
    info_app.addLabelSpinBoxRange("Birthday Day", 1, 31)
    info_app.addLabelNumericEntry("Birthday Year")
    info_app.addLabelEntry("Email")
    info_app.addLabelNumericEntry("Phone Number(Digits only!)")
    def press_athlete(button):
        """
        This is the function that executes a button push for athlete info window
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
                month = info_app.getSpinBox("Birthday Month")
                day = info_app.getSpinBox("Birthday Day")
                year = info_app.getEntry("Birthday Year")
                if year > 2021 or year < 1921:
                    if info_app.retryBox("Error", "Please enter a valid birth "
                                                  "year!"):
                        info_app.go()
                email = info_app.getEntry("Email")
                if "@" not in email:
                    if info_app.retryBox("Error",
                                         "Please enter a valid email!"):
                        info_app.go()
                number = info_app.getEntry("Phone Number(Digits only!)")
                if len(str(number)) != 10:
                    if info_app.retryBox("Error", "Please enter a valid phone "
                                                  "number!"):
                        info_app.go()
                break
            user_info.write(loc + "\n" + first + "\n" + last + "\n" + month
                            + "\n" + day + "\n" + year + "\n"
                            + email + "\n" + number)
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


def main():
    athlete = check_user_info()
    if athlete is False:
        athlete = get_barcode_info()


if __name__ == '__main__':
    main()
