"""
Author: Aidan Duffy
Creation Date: January 2, 2021
Last Updated: January 2, 2021
Description: This class is for the athlete, storing their YMCA sign in link
and their YMCA barcode ID number.
"""


class Athlete:

    def __init__(self, area_id, barcode, location, first, last, month, day,
                 year, email, phone):
        """
        This is the constructor for the athlete class.
        :param sign_in_url: is the url where the athlete normally inputs their
        barcode id number.
        :param barcode: is the athlete's unique identifier, their barcode ID
        number.
        :param location: is the selected YMCA.
        :param first: is the first name
        :param last: is the last name
        :param month: is the month for the birthday
        :param day: is the birthday day
        :param year: is the birthday year
        :param email: is the user's email
        :param phone: is the user's phone
        """
        self.area_id = area_id
        self.__id = barcode
        self.location = location
        self.first = first
        self.last = last
        self.month = month
        self.day = day
        self.year = year
        self.email = email
        self.phone = phone

    def set_barcode(self, barcode):
        """
        This alters the users barcode ID number.
        :param barcode: is the athlete's unique identifier.
        :return: None
        """
        self.__id = barcode

    def get_barcode(self):
        """
        This retrieves the athlete's ID number.
        :return: the barcode ID number for this athlete.
        """
        return self.__id
