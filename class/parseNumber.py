class ParseNumber:
    def is_225(self, phone_number: str) -> bool:
        """
        This function verify if a phone number start with 225

        Args:
            phone_number (str): The phone number to verify

        Returns:
            bool: The result of the verification
        """
        if phone_number.startswith("225"):
            return True
        return False


    def height_to_ten(self, phone_number: str) -> str:
        """
        This function transform height digit ivorian number to 10 digit ivorian number

        Args:
            phone_number (str): The phone number to transform

        Returns:
            str: The new number
        """
        mtn_numbers = [
            "04",
            "05",
            "06",
            "44",
            "45",
            "46",
            "54",
            "55",
            "56",
            "64",
            "65",
            "66",
            "74",
            "75",
            "76",
            "84",
            "85",
            "86",
            "94",
            "95",
            "96",
        ]
        moov_numbers = [
            "01",
            "02",
            "03",
            "40",
            "41",
            "42",
            "43",
            "50",
            "51",
            "52",
            "53",
            "70",
            "71",
            "72",
            "73",
        ]
        orange_numbers = [
            "07",
            "08",
            "09",
            "47",
            "48",
            "49",
            "57",
            "58",
            "59",
            "67",
            "68",
            "69",
            "77",
            "78",
            "79",
            "87",
            "88",
            "89",
            "97",
            "98",
        ]

        if self.is_225(phone_number):
            if len(phone_number) == 13:
                return phone_number
            
            elif len(phone_number) == 11:
                number_without_indicatif = phone_number[-8:]  # get the last 8 digits
                first_two_digit = number_without_indicatif[:2]  # get the first 2 digits

                if first_two_digit in mtn_numbers:
                    new_number = "22505" + number_without_indicatif
                    return new_number

                if first_two_digit in moov_numbers:
                    new_number = "22501" + number_without_indicatif
                    return new_number

                if first_two_digit in orange_numbers:
                    new_number = "22507" + number_without_indicatif
                    return new_number
            else: return False
        return False


    def whatsapp_to_civ(self, phone_number: str) -> str:
        """
        This function transform whatsapp api 'from' number to 10 digit ivorian number

        Args:
            phone_number (str): The phone number to transform

        Returns:
            str: The new number
        """
        new_phone = phone_number.split("@")
        return self.height_to_ten(new_phone[0])