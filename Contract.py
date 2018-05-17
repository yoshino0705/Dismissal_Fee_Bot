import pandas as pd
class Contract(object):
    def __init__(self, plan_code, contract_file='contract.csv'):
        # plan_code is from the title column in contract.csv and titles.txt
        self._code = plan_code
        self._df = pd.read_csv(contract_file, header=0, sep='\t')
        self._df_plan_code = self._df[self._df['title'] == self._code]
        self._df_rows = [r for i,r in self._df_plan_code.iterrows()]
        
    def get_plan_list(self):
        s = '請選擇以下方案\n'
        i = 0
        for r in self._df_rows:
            s += '{}) ${} {}個月\n'.format(i, r['rent'], r['length'])
            i += 1
        return s
    
    def get_plan_by_index(self, index=0):
        try:
            return self._df_rows[index]
        except IndexError:
            print('Invalid index', index)
            return {}
