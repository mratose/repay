import utility.constant as Constant
import pyodbc


class SaveRepay:
    def insertrepayment(self, repayments):

        try:

            conn = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};"
                                "Server=repayment.cublrxeg7c38.us-east-2.rds.amazonaws.com;"
                                "Database=repayment;"
                                "uid=repayment;pwd=repayment"
                                )

            cursor = conn.cursor()

            repaymentParam = []

            query = "INSERT INTO repayment (CustomerID,SeasonID, Date,Amount, parentID) VALUES (?,?,?,?,?)"
            repay = SaveRepay()
            max_record = repay.getmaxrecord()
            max_record = max_record[0] + 1


            for payments in repayments:

                repaymentParam.append(
                    (
                        payments['customerid'],
                        payments['seasonid'],
                        payments['Date'],
                        payments['Amount'],
                        max_record

                    )
                )
            print("Inserting into repayment table on SQL SERVER")
            for i in repaymentParam:
                cursor.execute(query, i)
                conn.commit()
            conn.close()
            print("Successfully inserted")


        except Exception as error:
            print("Error while Inserting data to SQLSERVER", error)

    def getmaxrecord(self):

        try:

            conn = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};"
                                  "Server=repayment.cublrxeg7c38.us-east-2.rds.amazonaws.com;"
                                  "Database=repayment;"
                                  "uid=repayment;pwd=repayment"
                                  )

            cursor = conn.cursor()

            query = "select isnull(max(repaymentid),0) from repayment"
            record = []
            cursor.execute(query)
            row = cursor.fetchone()
            record.append(row[0])
            conn.commit()
            conn.close()
            return record


        except Exception as error:
            print("Error while fetching maxrcord data from SQLSERVER", error)

