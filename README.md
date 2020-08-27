# Seasonless Repayment App 
# (Note: Post - mortem is at the bottom )
This app helps to process repayment of outstanding credits that have been previously been approved.
Each season, clients purchase products on credit, and over the course of a season, they repay their credit, and so clients have credit associated with them on a 
season-by-season basis.

Repayments are processed whether the clients have specified the season that wants to be repaid or not.


# Getting Started

- Clone the repo and run the Repay repo
- I have hosted a database on AWS 
- Details of database would be found in constant file in utility file.
- All data schema has been created on database.
- Table Structure
```
create table Seasons(
SeasonID int not null
,SeasonName nvarchar(50) null
,StartDate date null
,EndDate date null
)
go

create table CustomerSummaries
(
CustomerID int not null
,SeasonID int not null
,TotalRepaid decimal(21,6) not null
,Credit decimal(21,6) not null
)
go

create table Customers
(
CustomerID int null
,CustomerName nvarchar(100) null
)
go
```


# Project Flow
- The goal is to allow clients and/or in house employees process repayments for outstanding payments without specifying the outstaning season.
- This project gets the repaymentUpload of all clients and process all payments in the repayment upload
- All outstanding seasons are determined when no season is specified.
- For every season that is outstanding a repayment record is created and customer summary is updated.
- Customer summary is updated using the stored procedure below. The stored procedure is called once a repayment record is created for any season :
``` 
create procedure oafsp_upd_customer_summ

as

BEGIN
SET NOCOUNT ON
update CustomerSummaries
set totalrepaid = totalrepaid + b.amt
from CustomerSummaries a,  (
								select seasonid, sum(amount) amt, customerid, parentId
								from repayment 
								group by seasonid, customerid, parentid
																				) b
where a.customerid = b.customerid
and a.seasonid = b.seasonid
and a.totalrepaid != a.credit
and b.parentid = (select max(parentid) from repayment where customerid =b.customerid and seasonid=b.seasonid )
END
return 0
go
```
- For Overpaid scenarios where a client does not have an outstanding credit in a later season or does not have an outstanding at all. The stored procedure below 
is called to update the maximum season for that client with the full overpaid amount. These stored procedures have already been compiled on the database(AWS) and there are just 2 of them.:
```
create procedure oafsp_upd_max_season
@nCustomerid int,
@nRepayAmt decimal(26,6)

as

declare 
@nMaxSeason int

select @nMaxSeason = max(seasonid) from CustomerSummaries where customerid = @nCustomerid

BEGIN
SET NOCOUNT ON
update CustomerSummaries
set TotalRepaid = TotalRepaid + @nRepayAmt
where customerid = @nCustomerid
and seasonid = @nMaxSeason
END
return 0
go

```

# Class Details


 ## Data
   This module consists of all the classes that stores and retrieves information from the database. THis contains 2 classes:
   - CustomerSummaries.py ; handles operations such as get customer summaries, update customer summaries, update customer summary max season
   - SaveRepayments.py ; handles operations such as saving created repayments to database, handling association of adjustments repayments to original payments.
 ## Service
   This includes the repayment service that contains the main logic of this application:
   -RepaymentService.py ; this service determines the outstanding season for any client, it also gets customer summary, as well as create repayments based on outstanding             seasons .


 ##Template
  This includes my HTML file(home.htl and chart.html) for the basic interfaces. This module is not yet completed.
  
 ## Utility
COntains a constant class that holds Constansts such as  Database parameters and other information which do not change.

 ## app.py
 This is my flask web application to display basic interface. THis module is not yet completed.
 
 
 
 
# Post-mortem - 
## Current project status : The Project is about 80% complete. The following is the status:

	1. Service class has been implemented and can do the following:
	 - Receive repayment upload based on clients.
	 - Determine the season repayment should be applied to.
	 - Output a list of repayments for the correct client, season, and amount for each repayment.
	 - Shows adjustment repayments as well as original repayment
	 - Every adjusted repayment can be associated back to the original repayment.
	 - Takes care of the overpaid for those client that do not have outstanding payments in later season or any season at all.
	 - Takes care of the override for the client that specify a repayment season.
	 - Takes care of the cascade situation.

	2. Basic interface is yet to be completed.

## Estimate on the outstanding work. 
	-Outstanding work can be completed in a day or less.
	
## Successes/what went well
	-Logic implentation to create repayments and also update of customer summary.
	- Being able to handle some of the implentation at the database level.
	
## Bumps/what you wished went better
	- UI/UX
	- Use of list comprehensions for a more readable code.
	
## How you would improve your approach in future projects:
	- Draw up a proper and detailed design for the app.
	- Using generators & yield for memory efficiency.
	- 
## Improvements/enhancements to this project for future consideration:
	- Error Handling
	- Use generators & yield to make code faster and handle large data should incase data grows. 
	- TDD
