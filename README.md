# Seasonless Repayment App
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
