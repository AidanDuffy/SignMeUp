"""
Author: Aidan Duffy
Creation Date: January 2, 2021
Last Updated: January 2, 2021
Description: This program aids swimmers in scheduling/booking lap swim times
for local YMCAs in the northern New Jersey area.
"""
from webbrowser import Chrome

import appJar
import requests
from lxml import html
from selenium.webdriver.support.ui import Select
from selenium import webdriver
from athlete import Athlete

info_app = appJar.gui("YMCA Sign-in and Personal Info", "600x600")


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
        athlete = Athlete(info[0], int(info[1]), info[2], info[3], info[4],
                          int(info[5]), int(info[6]), int(info[7]), info[8],
                          info[9])
        return athlete
    else:
        return False


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
            url = info_app.getEntry("Barcode URL(daxko.com)")
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
                if info_app.retryBox("Error", "Your barcode is too short!"):
                    info_app.go()
            elif len(barcode) > 9:
                if info_app.retryBox("Error", "Your barcode is too long!"):
                    info_app.go()
            else:

                break
        user_info.write(url + "\n" + barcode + "\n")
        user_info.close()
        info_app.stop()


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
        print("Hi")


def get_barcode_info():
    """
    This asks the user for their sign-in page and barcode ID and populates the
    user info file with that info.
    :return: the athlete object
    """
    info_app.addLabel("title",
                      "Please provide your YMCA and login information")
    info_app.addLabelEntry("Barcode URL(daxko.com)")
    info_app.addNumericLabelEntry("Barcode ID")
    info_app.setFocus("Barcode URL(daxko.com)")
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
    page = submit_barcode(info[0], info[1])
    test = html.fromstring(page.text)
    driver = Chrome()
    driver.get(page.url)
    selector = Select(driver.find_element_by_id('location'))
    info_app.addLabelEntry("")
    info_app.addLabelEntry("First Name")
    info_app.addLabelEntry("Last Name")
    info_app.addLabelEntry("Birthday Month")
    info_app.addLabelEntry("Birthday Day")
    info_app.addLabelEntry("Birthday Year")
    info_app.addLabelEntry("Email")
    info_app.addLabelEntry("Phone Number")
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
