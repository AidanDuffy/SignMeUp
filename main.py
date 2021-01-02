"""
Author: Aidan Duffy
Creation Date: January 2, 2021
Last Updated: January 2, 2021
Description: This program aids swimmers in scheduling/booking lap swim times
for local YMCAs in the northern New Jersey area.
"""
import requests
from lxml import html

from athlete import Athlete


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
        athlete = list()
        for line in user_info:
            athlete.append(line[:len(line)-1])
        user_info.close()
        athlete = Athlete(athlete[0],int(athlete[1]))
        return athlete
    else:
        return False


def get_user_info():
    """
    This asks the user for their sign-in page and barcode ID and populates the
    user info file with that info.
    :return: the athlete object
    """
    user_info = open("user_info.txt", "w")
    while True:
        check_in_url = input("Please input the URL/link where your YMCA asks"
                             "for your barcode \n(it should say \"Virtual"
                             "Check In\" and be from \"daxko.com\"): ")
        check_in_url.strip()
        try:
            check_in_page = requests.get(check_in_url)
            check_in_page_content = check_in_page.content
            check_in_page_html = html.fromstring(check_in_page.content)
        except requests.exceptions.MissingSchema:
            print("Error: Please enter a URL!")
            continue
        if "operations.daxko.com" not in check_in_url and "Virtual Check In" \
                not in check_in_page_content:
            print("Error: This is not valid URL!")
            continue
        break
    print("Success!")
    while True:
        barcode = input("Please enter your barcode ID: ")
        barcode_int = 0
        try:
            barcode_int = int(barcode)
        except ValueError:
            print("Error: Please enter a valid number value for your barcode!")
            continue
        if len(barcode) < 9:
            print("Error: Your barcode is too short!")
            continue
        elif len(barcode) > 9:
            print("Error: Your barcode is too long!")
            continue
        else:
            break
    user_info.write(check_in_url + "\n" + barcode)
    athlete = Athlete(check_in_url, barcode_int)
    return athlete

def main():
    athlete = check_user_info()
    if athlete is False:
        athlete = get_user_info()
    

if __name__ == '__main__':
    main()
