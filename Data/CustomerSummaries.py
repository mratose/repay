import utility.constant as Constant
import pyodbc


class CustomerSummaries:

    def get_customer_summaries(self, customerid):
        try:

            conn = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};"
                                  "Server=repayment.cublrxeg7c38.us-east-2.rds.amazonaws.com;"
                                  "Database=repayment;"
                                  "uid=repayment;pwd=repayment"
                                  )

            cursor = conn.cursor()

            query = "select customerid, seasonid, totalrepaid, credit from customersummaries where customerid = ? FOR JSON AUTO"
            record = []
            cursor.execute(query, customerid)
            row = cursor.fetchall()
            for i in row:
                record.append(i)
            conn.close()
            return record


        except Exception as error:
            print("Error while fetching data from SQLSERVER", error)


    def upd_customer_summaries(self):
        try:

            conn = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};"
                                  "Server=repayment.cublrxeg7c38.us-east-2.rds.amazonaws.com;"
                                  "Database=repayment;"
                                  "uid=repayment;pwd=repayment"
                                  )

            cursor = conn.cursor()

            sql = "DECLARE @RC int EXEC @RC = [repayment].[dbo].[oafsp_upd_customer_summ] SELECT @RC AS rc"



            print("Calling update customer summary SP")
            cursor.execute(sql)
            conn.commit()
            print("Customer summary updated succesfully")

            return "Customer summary updated succesfully"



        except Exception as error:
            print("Error while fetching data from SQLSERVER", error)


    def upd_summary_max_season(self, customer_id, repayment_amt):
        try:

            conn = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};"
                                  "Server=repayment.cublrxeg7c38.us-east-2.rds.amazonaws.com;"
                                  "Database=repayment;"
                                  "uid=repayment;pwd=repayment"
                                  )

            cursor = conn.cursor()

            sql = "DECLARE @RC int EXEC @RC = [repayment].[dbo].[oafsp_upd_max_season]  ?, ? SELECT @RC AS rc"

            values = (customer_id, repayment_amt)

            print("Calling update customer summary SP")
            cursor.execute(sql, values)
            conn.commit()
            print("Customer summary updated succesfully")

            return "Customer summary updated succesfully"



        except Exception as error:
            print("Error while fetching data from SQLSERVER", error)

