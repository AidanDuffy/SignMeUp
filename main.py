"""
Author: Aidan Duffy
Creation Date: January 2, 2021
Last Updated: January 2, 2021
Description: This program aids swimmers in scheduling/booking lap swim times
for local YMCAs in the northern New Jersey area.
"""
import sys, os, site, requests
from lxml import html

def main():
    while True:
        check_in_url = input("Please input the URL/link where your YMCA asks"
                             "for your barcode (it should say \"Virtual"
                             "Check In\" and be from \"daxko.com\"): ")
        check_in_url.strip()
        try:
            check_in_page = requests.get(check_in_url)
            check_in_page_content = check_in_page.content
            check_in_page_html = html.fromstring(check_in_page.content)
            check_in_page_form = check_in_page_html.form_values()
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
        try:
            barcode = input("Please enter your barcode ID: ")
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

        print("test")


if __name__ == '__main__':
    main()