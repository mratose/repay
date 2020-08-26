import json
from Data.SaveRepayments import SaveRepay


class RepaymentService:

    def __init__(self):
        # loading our json file here to use it across different class methods
        self.repayment = json.load(open('Repayment.json'))
        self.repaymentUpload = self.repayment['RepaymentUploads']
        self.seasons = self.repayment['Seasons']
        self.customersummaries = self.repayment['CustomerSummaries']


# get repayment information per client
    def get_repayment(self, customerid):
        repayment = self.repaymentUpload
        for key in repayment:
            if key['CustomerID'] == customerid:
                return key


# get customer summary information per client
    def get_cust_summary(self, customerid):
        summary_list = []
        summary = self.customersummaries
        for key in summary:
            if key['CustomerID'] == customerid:
                summary_list.append(key)
        return summary_list

#determine season that requires repayment based on client repayment upload
    def determine_season(self, customer_id):
        repayment = self.get_repayment(customer_id)
        repayment_amt = repayment['Amount']
        seasonid = repayment['SeasonID']
        date = repayment['Date']

        repay_dict = {}
        repay_list = []
        if seasonid == 0:
            cust_summary = self.get_cust_summary(customer_id)
            #print(cust_summary)

            for repay in cust_summary:
                if repay['TotalRepaid'] != repay['Credit'] and repay['Credit'] > repay['TotalRepaid']:
                    to_pay = repay['Credit'] - repay['TotalRepaid']

                    repay_dict['CustomerID'] = customer_id
                    repay_dict['SeasonId'] = repay['SeasonID']
                    repay_dict['Date'] = date
                    repay_dict['season_due_amt'] = to_pay
                    repay_dict['current_repay_amt'] = repayment_amt
                    repay_list.append(repay_dict.copy())

            return repay_list
        else:
            repay_dict['CustomerID'] = customer_id
            repay_dict['SeasonId'] = seasonid
            repay_dict['Date'] = date
            repay_dict['season_due_amt'] = repayment_amt
            repay_dict['current_repay_amt'] = repayment_amt
            repay_list.append(repay_dict.copy())
            return repay_list

#Now lets create the repayment records
    def repay(self, customer_id):
        determine_season = self.determine_season(customer_id)
        repayment = self.get_repayment(customer_id)
        repayment_amt = repayment['Amount']
        repay_dict = {}
        repay_list = []
        track = repayment_amt

        for i in determine_season:
            print(i)

            avail_bal = repayment_amt
            due = i['season_due_amt']
            while track > 0:
                repay_dict['CustomerID'] = customer_id
                repay_dict['SeasonId'] = i['SeasonId']
                repay_dict['Date'] = i['Date']
                repay_dict['Amount'] = track
                repay_list.append(repay_dict.copy())

                track = avail_bal - due

                if avail_bal > due:
                    track = avail_bal - due
                    repay_dict['CustomerID'] = customer_id
                    repay_dict['SeasonId'] = i['SeasonId']
                    repay_dict['Date'] = i['Date']
                    repay_dict['Amount'] = track * -1
                    repay_list.append(repay_dict.copy())
                    track = avail_bal - due
                    #break
                #avail_bal = avail_bal - due

        createRepay = SaveRepay()
        createRepay.insertrepayment(repay_list)
        #return repay_list


repay = RepaymentService()
#print(repay.get_repayment(1))
#print(repay.get_cust_summary(11))
#print(repay.determine_season(11))
repay.repay(11)













