libname ticker 'C:\TEMP\ticker_merge';

/* Get one-to-one ticker list */
proc sql;
create table ticker.one2one as 
select * from ticker.distinct as d
group by d.ticker
having count(d.ticker)=1
;
quit;

/* Get one-to-many ticker list */
proc sql;
create table ticker.one2many as 
select * from ticker.distinct as d
group by d.ticker
having count(d.ticker)>1
;
quit;

/* Get unmerged filename list */
proc sql;
create table ticker.unmerged as 
select filename, symbol, cc_date as date
from ticker.data_fin_merged1
where permno is null
group by symbol
;
quit;

data ticker.unmerged;
set ticker.unmerged;
date=input(date, MMDDYY8.);
format date mmddyy8.;
run;

/* Get permno list of unmerged data */
proc sort data=ticker.permno out=ticker.permno_sorted;
by ticker date;
run;

proc sql;
create table ticker.permno_sorted as 
select * from ticker.permno_sorted as p
where p.ticker in (select symbol from ticker.unmerged)
order by p.ticker, p.date
;
quit;

/* Get list of companies that are not NASDAQ or NYSE */
data ticker.non_us;
merge ticker.data_fin ticker.distinct(rename=(ticker=symbol date=date2));
by symbol;
if (permno) then delete;
run;

/* Get duplication */
proc sql;
create table ticker.duplication as
select filename, symbol as ticker, cc_date, date, permno, cusip, comnam
from ticker.data_fin_merged_check
group by filename
having count(comnam)>1
;
quit;
