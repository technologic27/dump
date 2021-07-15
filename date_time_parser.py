#!/usr/bin/python3

import re
from datetime import datetime

import logging
logging.basicConfig(format='%(asctime)s [%(filename)s:%(lineno)s - %(module)s:%(funcName)10s() : %(levelname)s] %(message)s',
                    level=logging.INFO)


class DateTime(object):
    log = logging.getLogger('Date')

    year = None
    month = None
    day = None

    hour = None
    minute = None
    second = None

    utc_offset = None

    year_pattern = re.compile("^(\d{4})[^0-9]*")
    month_pattern = re.compile("^((?:0[1-9])|(?:[1][0-2])|(?:[1-9]))[^0-9]*")
    day_pattern = re.compile("^((?:0[1-9])|(?:[1-2][0-9])|(?:3[01])|(?:[1-9]))[^0-9]*")

    delimiter_regex_pattern = re.compile("\-|:|T|\s+")

    # Remove the 'T' and 'Z' characters in the following type of date format:
    # 2017-05-22T02:58:53Z
    # Remove the colon character in the time zone portion of the following type of date format:
    # 2017-08-11T00:37:19+00:00

    replacement_regex_strings = [ ('(?<=\d{4}[/\-]\d{2}[/\-]\d{2})T', ' '),
                                  ('(?<=\d{2}[:\-]\d{2}[:\-]\d{2})Z', ' '),
                                  ('(?<=[+\-]\d{2}):(?=\d{2})', ''),
                                  ('[:\/]', '-')]
    replacement_regex_patterns = [(re.compile(pattern), replacement) for pattern, replacement in replacement_regex_strings]

    # see https://docs.python.org/3/library/datetime.html
    #
    # Examples of dates:
    # 2017-08-11T00:37:19+00:00
    # 2017-08-11 Fri 00:37:19 +0000
    # 2017-05-22T02:58:53Z
    #
    datetime_formats = ['%Y-%m-%d',
                        '%Y-%m-%d %a',
                        "%Y-%m-%d %H-%M-%S",
                        "%Y-%m-%d %a %H-%M-%S",
                        "%Y-%m-%d %H-%M-%S%Z",
                        "%Y-%m-%d %a %H-%M-%S%Z",
                        "%Y-%m-%d %H-%M-%S %Z",
                        "%Y-%m-%d %a %H-%M-%S %Z",
                        "%Y-%m-%d %H-%M-%S%z",
                        "%Y-%m-%d %a %H-%M-%S%z",
                        "%Y-%m-%d %H-%M-%S %z",
                        "%Y-%m-%d %a %H-%M-%S %z"
                        ]

    def __init__(self, year: int =None, month: int =None, day: int =None,
                 hour: int=None, minute: int=None, second: int=None,
                 utc_offset: int=None):
        if year is not None and year > 0:
            self.year = year

        if month is not None and month > 0 and month <= 12:
            self.month = month

        if day is not None and day > 0 and day <= 31:
            self.day = day

        if hour is not None and hour >= 0 and hour <= 23:
            self.hour = hour

        if minute is not None and minute >= 0 and minute <= 59:
            self.minute = minute

        if second is not None and second >= 0 and second <= 59:
            self.second = second

        if utc_offset is not None and utc_offset > - 24 * 60 and utc_offset < 24 * 60:
            self.utc_offset = utc_offset

    def get_year(self) -> int:
        return self.year

    def get_month(self) -> int:
        return self.month

    def get_day(self) -> int:
        return self.day

    def get_hour(self) -> int:
        return self.hour

    def get_minute(self) -> int:
        return self.minute

    def get_second(self) -> int:
        return self.second

    def get_utc_offset(self) -> int:
        return self.utc_offset

    def set_year(self, year: int):
        self.year = year

    def __eq__(self, a_date) -> bool:
        result = False

        if a_date is not None:
            if self.year == a_date.year and self.month == a_date.month and self.day == a_date.day:
                result = True

        return result

    def __lt__(self, a_date) -> bool:
        '''

        :param a_date:
        :return: True if a_date is newer, for example, the current date is 2017-10-02 and a_date is 2017-10-03
        '''

        result = False

        if a_date is not None:
            if self.year is not None and a_date.year == None:
                return False

            if self.year is None and a_date.year is not None:
                return True

            if self.year is not None and a_date.year is not None:
                if self.year < a_date.year:
                    return True

            if self.month is not None and a_date.month == None:
                return False

            if self.month is None and a_date.month is not None:
                return True

            if self.month is not None and a_date.month is not None:
                if self.month < a_date.month:
                    return True

            if self.day is not None and a_date.day == None:
                return False

            if self.day is None and a_date.day is not None:
                return True

            if self.day is not None and a_date.day is not None:
                if self.day < a_date.day:
                    return True

        return result

    def is_less_precise(self, a_date) -> bool:
        '''

        :param a_date:
        :return: True if a_date is less precise, for example, the current date is 2017-10-02 and a_date is 2017-10
        '''

        result = False

        if a_date is not None:
            if self.year == a_date.year:
                if self.month is not None and a_date.month is None:
                    result = True
                elif self.month == a_date.month:
                    if self.day is not None and a_date.day is None:
                        result = True

        return result

    @staticmethod
    def is_date(date_string: str) -> bool:
        result = False

        if DateTime.create_datetime(date_string) is not None:
            result = True

        return result

    @staticmethod
    def create_datetime(date_string: str) -> datetime:
        date_time_object = None

        if date_string is not None and len(date_string) > 0:
            new_date_string = date_string
            for pattern, substitution_string in DateTime.replacement_regex_patterns:
                new_date_string = re.sub(pattern, substitution_string, new_date_string)
            new_date_string = new_date_string.strip()

            for datetime_format in DateTime.datetime_formats:
                try:
                    date_time_object = datetime.strptime(str(new_date_string), datetime_format)
                    if date_time_object is not None:
                        break
                except ValueError as e:
                    #self.log.error(e)
                    #self.log.error('Date Time format: %s', datetime_format)
                    date_time_object = None
                    pass

        return date_time_object

    def set_from_string(self, date_string: str):
        year = None
        month = None
        day = None
        hour = None
        minute = None
        second = None
        utc_offset = None

        date_time_object = DateTime.create_datetime(date_string)
        if date_time_object is not None:
            year = date_time_object.year
            month = date_time_object.month
            day = date_time_object.day
            hour = date_time_object.hour
            minute = date_time_object.minute
            second = date_time_object.second
            utc_offset = date_time_object.utcoffset()
            if utc_offset is not None:
                utc_offset = utc_offset.total_seconds()/60 #convert to minutes

        elif date_string is not None and len(date_string) > 0:
            value_list = re.split(self.delimiter_regex_pattern, date_string)
            number_of_values = len(value_list)

            if number_of_values >= 1:
                match = re.match(self.year_pattern, value_list[0])
                if match is not None and match.lastindex == 1:
                    year = int(match.group(1))
                else:
                    #self.log.warning("Cannot find year in date string: %s", date_string)
                    pass

                if number_of_values >= 2:
                    match = re.match(self.month_pattern, value_list[1])
                    if match is not None and match.lastindex == 1:
                        month = int(match.group(1))
                    else:
                        #self.log.warning("Cannot find month in date string: %s", date_string)
                        pass

                    if number_of_values >= 3:
                        match = re.match(self.day_pattern, value_list[2])
                        if match is not None and match.lastindex == 1:
                            day = int(match.group(1))
                        else:
                            #self.log.warning("Cannot find day in date string: %s", date_string)
                            pass
        else:
            #self.log.warning("Failed to parse date string: %s", date_string)
            pass

        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute
        self.day = day
        self.utc_offset = utc_offset

    @staticmethod
    def create_from_string(date_string:str):
        date_time = DateTime()
        date_time.set_from_string(date_string)
        return date_time

    def __str__(self):
        return self.str()

    def str(self):
        date_string = ''

        if self.year is not None:
            date_string += str(self.year)

            if self.month is not None:
                date_string += '-' + str(self.month)

                if self.day is not None:
                    date_string += '-' + str(self.day)

                    if self.hour is not None:
                        date_string += ' ' + str(self.hour)

                        if self.minute is not None:
                            date_string += ':' + str(self.minute)

                            if self.second is not None:
                                date_string += ':' + str(self.second)

                    utc_offset_string = self.__get_utc_offset_string()
                    if utc_offset_string is not None:
                        date_string += ' ' + utc_offset_string

        return date_string

    def date_str(self):
        date_string = ''

        if self.year is not None:
            date_string += str(self.year)

            if self.month is not None:
                date_string += '-' + str(self.month)

                if self.day is not None:
                    date_string += '-' + str(self.day)

        return date_string

    def str_YYYYMMDD(self):
        date_string = ''

        if self.year is not None:
            date_string += str(self.year).zfill(4)

            if self.month is not None:
                date_string += '-' + str(self.month).zfill(2)

                if self.day is not None:
                    date_string += '-' + str(self.day).zfill(2)

                    if self.hour is not None:
                        date_string += ' ' + str(self.hour).zfill(2)

                        if self.minute is not None:
                            date_string += ':' + str(self.minute).zfill(2)

                            if self.second is not None:
                                date_string += ':' + str(self.second).zfill(2)

                    utc_offset_string = self.__get_utc_offset_string()
                    if utc_offset_string is not None:
                        date_string += ' ' + utc_offset_string

        return date_string

    def  __get_utc_offset_string(self):
        result = None

        if self.utc_offset is not None:
            utc_offset = abs(self.utc_offset)
            offset_hour = utc_offset // 60
            offset_minutes = utc_offset % 60
            if self.utc_offset >= 0:
                result = '+'
            else:
                result = '-'

            result += str(int(offset_hour)).zfill(2) + str(int(offset_minutes)).zfill(2)

        return result

    def to_datetime(self) -> datetime:
        datetime_object = None

        try:
            datetime_object = datetime.strptime(self.str_YYYYMMDD(), self.__get_date_format_string())
        except Exception as e:
            #self.log.error(e)
            #self.log.error("Date: %s , Date format string: %s", self.str_YYYYMMDD(), self.__get_date_format_string())
            pass

        return datetime_object

    def __get_date_format_string(self):
        date_format_string = ''

        if self.year is not None:
            date_format_string += '%Y'

            if self.month is not None:
                date_format_string += '-%m'

                if self.day is not None:
                    date_format_string += '-%d'

                    if self.hour is not None:
                        date_format_string += ' ' + '%H'

                        if self.minute is not None:
                            date_format_string += ':' + '%M'

                            if self.second is not None:
                                date_format_string += ':' + '%S'

                    utc_offset_string = self.__get_utc_offset_string()
                    if utc_offset_string is not None:
                        date_format_string += ' ' + '%z'

        return date_format_string