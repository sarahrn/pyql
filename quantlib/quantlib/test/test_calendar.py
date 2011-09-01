import unittest

from quantlib.time.calendar import *
from quantlib.time.calendars.united_kingdom import UnitedKingdom, EXCHANGE
from quantlib.time.calendars.united_states import UnitedStates, NYSE
from quantlib.time.calendars.null_calendar import NullCalendar
from quantlib.time.calendars.germany import Germany, FrankfurtStockExchange
from quantlib.time.date import (
    Date, May, March, June, Jan, August, Months,November, Period, Days, July,
    September, Oct
)

class TestQuantLibCalendar(unittest.TestCase):

    def test_calendar_creation(self):

        calendar = TARGET()
        self.assertEquals('TARGET',  calendar.name())

        ukcalendar = UnitedKingdom()
        self.assertEquals('UK settlement',  ukcalendar.name())

        lse_cal = UnitedKingdom(market=EXCHANGE)
        self.assertEquals('London stock exchange',  lse_cal.name())

        null_calendar = NullCalendar()
        self.assertEquals('Null', null_calendar.name())

    def test_holiday_check(self):

        calendar = TARGET()
        
        date = Date(24,12, 2011)

        self.assertTrue(calendar.is_holiday(date))

    def test_business_day_check(self):

        ukcal = UnitedKingdom()

        bank_holiday_date = Date(3, May, 2010) #Early May Bank Holiday

        self.assertTrue(not ukcal.is_business_day(bank_holiday_date))

        business_day = Date(28, March, 2011)
        self.assertTrue(ukcal.is_business_day(business_day))

    def test_business_days_between_dates(self):

        ukcal = UnitedKingdom()

        date1 = Date(30, May, 2011)

        # 30st of May is Spring Bank Holiday

        date2 = Date(3, June, 2011)

        day_count = ukcal.business_days_between(date1, date2, include_last=True)

        self.assertEquals(4, day_count)

    def test_holiday_list_acces_and_modification(self):

        ukcal = UnitedKingdom()

        holidays = list(
            holiday_list(ukcal, Date(1, Jan, 2011), Date(31, 12,2011) )
        )
        self.assertEquals(8, len(holidays))

        new_holiday_date = Date(23, August, 2011)

        ukcal.add_holiday(new_holiday_date)

        holidays = list(
            holiday_list(ukcal, Date(1, Jan, 2011), Date(31, 12,2011) )
        )
        self.assertEquals(9, len(holidays))

        ukcal.remove_holiday(new_holiday_date)

        holidays = list(
            holiday_list(ukcal, Date(1, Jan, 2011), Date(31, 12,2011) )
        )
        self.assertEquals(8, len(holidays))

    def test_adjust_business_day(self):

        ukcal = UnitedKingdom()

        bank_holiday_date = Date(3, May, 2010) #Early May Bank Holiday

        adjusted_date = ukcal.adjust(bank_holiday_date)
        following_date = bank_holiday_date + 1
        self.assertTrue(following_date == adjusted_date)

        adjusted_date = ukcal.adjust(bank_holiday_date, convention=Preceding)
        following_date = bank_holiday_date - 3 # bank holiday is a Monday
        self.assertTrue(following_date == adjusted_date)

        adjusted_date = ukcal.adjust(bank_holiday_date,
                convention=ModifiedPreceding)
        following_date = bank_holiday_date + 1 # Preceding is on a different
                                               # month
        self.assertTrue(following_date == adjusted_date)

    def test_calendar_date_advance(self):
        ukcal = UnitedKingdom()

        bank_holiday_date = Date(3, May, 2010) #Early May Bank Holiday

        advanced_date = ukcal.advance(bank_holiday_date, step=6, units=Months)
        expected_date = Date(3, November, 2010)
        self.assertTrue(expected_date == advanced_date)

        period_10days = Period(10, Days)
        advanced_date = ukcal.advance(bank_holiday_date, period=period_10days)
        expected_date = Date(17, May, 2010)
        self.assertTrue(expected_date == advanced_date)

    def test_united_states_calendar(self):

        uscal = UnitedStates()
        holiday_date = Date(4, July, 2010) 

        self.assertTrue(uscal.is_holiday(holiday_date))

        uscal = UnitedStates(market=NYSE)
        holiday_date = Date(5, September, 2011) # Labor day 

        self.assertTrue(uscal.is_holiday(holiday_date))

    def test_german_calendar(self):

        frankfcal   = Germany(FrankfurtStockExchange);
        first_date  = Date(31,Oct,2009)
        second_date = Date(1,Jan ,2010);

        print "Date 2       Adv:", frankfcal.adjust(second_date , Preceding)
        print "Date 2       Adv:", frankfcal.adjust(second_date , ModifiedPreceding)

        mat = Period(2,Months)

        print "Date 1 Month Adv:", \
              frankfcal.advance(
                    first_date, period=mat, convention=Following, 
                    end_of_month=False
               )
        print "Date 1 Month Adv:", \
              frankfcal.advance(
                    first_date, period=mat, convention=ModifiedFollowing,
                    end_of_month=False
              )
        print "Business Days Between:", \
              frankfcal.business_days_between(
                    first_date, second_date, False, False
              )
        



class TestDateList(unittest.TestCase):

    def test_iteration_on_date_list(self):


        cal = TARGET()

        date_iterator = holiday_list(TARGET(), Date(1, Jan, 2000), Date(1,
            Jan, 2001))

        print dir(date_iterator)
        print 'next'
        aa =  date_iterator.__next__()
        print type(aa)
        print 'looping'
        for date in date_iterator:
            print date


if __name__ == '__main__':
    unittest.main()