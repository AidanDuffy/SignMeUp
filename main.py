"""
Author: Aidan Duffy
Creation Date: January 2, 2021
Last Updated: January 2, 2021
Description: This program aids swimmers in scheduling/booking lap swim times
for local YMCAs in the northern New Jersey area.
"""
import requests
from lxml import html
import appJar
from athlete import Athlete

info_app = appJar.gui("YMCA Sign-in Info", "600x600")

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
            info.append(line[:len(line)-1])
        user_info.close()
        athlete = Athlete(info[0],int(info[1]), info[2], info[3],info[4],
                          int(info[5]),int(info[6]),int(info[7]),info[8],
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
    else:
        user_info = open("user_info.txt", "w")
        url = info_app.getEntry("Barcode URL(daxko.com)")
        barcode = info_app.getEntry("Barcode ID")
        try:
            check_in_page = requests.get(url)
            check_in_page_content = check_in_page.content
        except requests.exceptions.MissingSchema:
            print("Error: Please enter a URL!")
        if "operations.daxko.com" not in url and "Virtual Check In" \
                not in check_in_page_content:
            print("Error: This is not valid URL!")
        try:
            barcode_int = int(barcode)
        except ValueError:
            print("Error: Please enter a valid number value for your barcode!")
        if len(barcode) < 9:
            print("Error: Your barcode is too short!")
        elif len(barcode) > 9:
            print("Error: Your barcode is too long!")
        user_info.write(url + "\n" + barcode)
        user_info.close()

def get_barcode_info():
    """
    This asks the user for their sign-in page and barcode ID and populates the
    user info file with that info.
    :return: the athlete object
    """
    info_app.addLabel("title",
                      "Please provide your YMCA and login information")
    info_app.addLabelEntry("Barcode URL(daxko.com)")
    info_app.addLabelEntry("Bardcode ID")
    info_app.addButtons(["Submit", "Cancel"], press)
    info_app.setFocus("Barcode URL(daxko.com)")
    info_app.go()



def main():
    athlete = check_user_info()
    if athlete is False:
        athlete = get_barcode_info()



if __name__ == '__main__':
    main()
