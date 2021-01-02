"""
Author: Aidan Duffy
Creation Date: January 2, 2021
Last Updated: January 2, 2021
Description: This class is for the athlete, storing their YMCA sign in link
and their YMCA barcode ID number.
"""

class Athlete:

    def __init__(self, sign_in_url, barcode):
        """
        This is the constructor for the athlete class.
        :param sign_in_url: is the url where the athlete normally inputs their
        barcode id number.
        :param barcode: is the athlete's unique identifier, their barcode ID
        number.
        """
        self.url = sign_in_url
        self.__id = barcode

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