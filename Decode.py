import ast

class Decode(object):
    def __init__(self, keywords, title_file='title.txt'):
        self._titles = ast.literal_eval(open(title_file, encoding="utf8").read())
        self._telecoms = set([d['telecom'] for d in self._titles]) # set of all possible telecoms
        self._plans = {(_d['telecom']+_d['plan']) : _i for _d,_i in zip(self._titles, range(len(self._titles)))}
        self._terms = keywords.split()
        
        self.telecoms = self._get_telecoms()
        self.plans = self._get_plans() # mapping telecom name + plan to title code
    def _get_telecoms(self):
        candidates = set()
        for term in self._terms:
            if term:
                candidates.update([t for t in self._telecoms if term in t])
        return candidates
    
    def _is_telecoms_plan(self, plan_name):
        # plan name includes telecom and plan name
        return bool([True for _t in self.telecoms if _t in plan_name])
    
    def _get_plans(self):
        candidates = {}
        for term in self._terms:
            if term:
                candidates = {_k:_v for _k,_v in self._plans.items() if self._is_telecoms_plan(_k) and term in _k}
        return candidates
