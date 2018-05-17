from Decode import Decode
from Estimate import Estimate
from Contract import Contract

class Switcher(object):
    def __init__(self, ai_con, text):
        self._status = ai_con.get_status()
        self._msg = text
        self._con = ai_con
        
    def execute(self):
        if self._status < 0:
            self._status = 0
        print("STATUS", self._status)
        method_name = 'status_' + str(self._status)
        method = getattr(self, method_name, lambda: "Invalid status")
        return method()
    
    def status_0(self):
        decoded_plans = Decode(self._msg)
        if not decoded_plans.plans:
            plans_text = '無此方案或未提電信名，或關鍵詞中間無空格，例如: " 中699 " 應為 " 中 699 "'
            self._con.set_status(0)
        else:
            plans_text = '請選擇一個方案: (輸入數字)\n'
            index = 0
            for k in decoded_plans.plans.keys():
                plans_text += '{}) {}\n'.format(index, k)
                index += 1
            self._con.set_keywords(self._msg)
            self._con.set_status(1)
            
        return plans_text

    def status_1(self):
        # process selection from status 0       
        print("selected:", self._msg)
        try:
            selection = int(self._msg)
            keywords = self._con.get_keywords()
            decoded_plans = Decode(keywords)
            plans = [k for k in decoded_plans.plans.keys()]
            p = plans[selection]
            tpi = decoded_plans.plans[p] # get the title code            
            c = Contract(tpi)
            
            self._con.set_tele_plan_id(tpi)
            self._con.set_status(2)
            return c.get_plan_list()
        except ValueError:
            print("Invalid selection")
            self._con.set_status(1)
            return "無此選項"
        except IndexError:
            print("Index out of range")
            self._con.set_status(1)
            return "無此選項"
        
    def status_2(self):
        # process selection from status 1
        print("selected:", self._msg)
        try:
            selection = int(self._msg)
            tpi = self._con.get_tele_plan_id()
            c = Contract(tpi)
            plan = c.get_plan_by_index(selection)

            if len(plan) == 0:
                print("Index out of range")
                self._con.set_status(2)
                return "無此選項"
            
            self._con.set_detailed_plan_id(selection)
            self._con.set_status(3)
            return "請輸入合約開始日期(年/月/日)，例: 2018/01/01"
        except ValueError:
            print("Invalid selection")
            self._con.set_status(2)
            return "無此選項"
        except IndexError:
            print("Index out of range")
            self._con.set_status(2)
            return "無此選項"
        
    def status_3(self):
        print("Start date", self._msg)
        start = Estimate.parse_start_time(self._msg)
        # validate start date
        if not start:
            self._con.set_status(3)
            return "日期格式錯誤"
        start = str(start.date()).replace('-','/')
        self._con.set_start_date(start)
        self._con.set_status(4)
        return "請輸入欲解約日期(年/月/日)，例: 2018/01/01\n 倘若格式錯誤會以今日為解約日期"
    
    def status_4(self):
        # parses the end date and evaluate
        print("Users end date", self._msg)
        end_date = Estimate.parse_end_time(self._msg)
        end_str = str(end_date.date()).replace('-','/')
        start_str = self._con.get_start_date()
        start_date = Estimate.parse_start_time(start_str)
        if start_date > end_date:
            print("Start date > end date")
            self._con.set_status(3)
            return "合約開始日期不能比結束晚，請重新輸入合約開始日期"
        else:
            tpi = self._con.get_tele_plan_id()
            dpi = self._con.get_detailed_plan_id()
            plan = Contract(tpi).get_plan_by_index(dpi)
            est = Estimate(plan, start_str, end_str)
            self._con.set_status(-1) # evaluation complete, status reset
            return "違約金約為 ${}".format(est.evaluate())
