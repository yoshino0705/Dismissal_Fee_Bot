import datetime
class Estimate(object):
    def __init__(self, plan, start_date, end_date):
        self._length = plan['length']
        self._rent = plan['rent']
        self._subsidy = plan['subsidy']
        self._discount = plan['discount']
        self._start = self.parse_start_time(start_date)
        self._end = self.parse_end_time(end_date)
        
    def parse_start_time(self, start_date):
        try:
            return datetime.datetime.strptime(start_date, '%Y/%m/%d')
        except ValueError:
            print("Invalid date format", start_date)
            return None
        
    def parse_end_time(self, end_date):
        try:
            return datetime.datetime.strptime(end_date, '%Y/%m/%d')
        except ValueError:
            print("Invalid date format", end_date, ". Will use current date instead.")
            return datetime.datetime.now()
        
    def evaluate(self):
        days_passed = (self._end - self._start).days
        if days_passed < 0:
            print("starting date is greater than ending date")
            return -1
        contract_days = (self._length / 24) * 365
        days_left = contract_days - days_passed
        penalty = ((self._discount / 30) * days_passed)
        penalty += self._subsidy
        penalty *= (days_left / contract_days)
        return round(penalty)
        
