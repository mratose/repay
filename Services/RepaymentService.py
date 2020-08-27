import json
from Data.SaveRepayments import SaveRepay
from Data.CustomerSummaries import CustomerSummaries


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
        summarycust = CustomerSummaries()

        summary = summarycust.get_customer_summaries(customerid)

        return json.loads(summary[0][0])

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
                if repay['totalrepaid'] != repay['credit'] and repay['credit'] > repay['totalrepaid']:
                    to_pay = repay['credit'] - repay['totalrepaid']

                    repay_dict['customerid'] = customer_id
                    repay_dict['seasonid'] = repay['seasonid']
                    repay_dict['Date'] = date
                    repay_dict['season_due_amt'] = to_pay
                    repay_dict['current_repay_amt'] = repayment_amt
                    repay_list.append(repay_dict.copy())

            return repay_list
        else:
            repay_dict['customerid'] = customer_id
            repay_dict['seasonid'] = seasonid
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

        #if theres nothing to pay update the most recent season else go ahead and create repayments
        if len(determine_season) == 0:
            summary = CustomerSummaries()
            summary.upd_summary_max_season(customer_id, repayment_amt)
            print("Updated max season")
        else:
            repay_dict = {}
            repay_list = []
            global avail_bal
            avail_bal = repayment_amt

            for i in determine_season:

                while avail_bal > 0:
                    due = i['season_due_amt']
                    repay_dict['customerid'] = customer_id
                    repay_dict['seasonid'] = i['seasonid']
                    repay_dict['Date'] = i['Date']
                    repay_dict['Amount'] = avail_bal
                    repay_list.append(repay_dict.copy())

                    avail_bal = avail_bal - due

                    if avail_bal > 0:

                        repay_dict['customerid'] = customer_id
                        repay_dict['seasonid'] = i['seasonid']
                        repay_dict['Date'] = i['Date']
                        repay_dict['Amount'] = avail_bal * -1
                        repay_list.append(repay_dict.copy())
                    break

            #insert the repayments to the database
            createRepay = SaveRepay()
            createRepay.insertrepayment(repay_list)

            #update the Customer summary
            updSummary = CustomerSummaries()
            updSummary.upd_customer_summaries()


if __name__ == '__main__':
    repay = RepaymentService()
    repay.repay(11)

















