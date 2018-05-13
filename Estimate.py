import ast

class Estimate(object):
    def __init__(self, title_file='title.txt', contract_file='contract.csv'):
        self.titles = ast.literal_eval(open(title_file, encoding="utf8").read())
        self.telecoms = set([d['telecom'] for d in self.titles]) # set of all possible telecoms
        self.plans = [d['plan'] for d in self.titles] # list of possible plans from the telecoms
        self.telecom_candidates = [] # telecom candidates based on given keywords
        self.plan_candidates = [] # plan candidates based on given keywords
        
    def find_telecom_candidates(self, term):
        if not term:
            return False
        l = [t for t in self.telecoms if term in t]
        self.telecom_candidates = l
        self.plans = [d['plan'] for d in self.titles if d['telecom'] in l]
        return True if l else False
    
    def find_plan_candidates(self, term):
        if not term:
            return False
        l = [p for p in self.plans if term in p]
        self.plan_candidates = l
        return True if l else False
        
if __name__ == '__main__':
    est = Estimate()
    est.find_telecom_candidates('中華')
    est.find_plan_candidates('4G')
    est.plan_candidates
