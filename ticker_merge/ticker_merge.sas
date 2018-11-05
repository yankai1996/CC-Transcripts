libname ticker 'C:\TEMP\ticker_merge';

%macro txt2sas7bdat(name);

proc delete data=work._all_;
run;

data ticker.&name;
infile "C:\TEMP\ticker_merge\&name..txt" dlm='09'x firstobs=2;
input filename symbol $ CC_Date $ CC_Time $ PresWordNum PresCharNum QandAWordNum QandACharNum ShortWords LongWords NegWordsPres NegWordsQA NegWordsTotal;
run;

%mend;

* %txt2sas7bdat(data_fin);
* %txt2sas7bdat(data_havard);


/* Get distinct permno list */

proc sql;
create table ticker.distinct as 
select distinct p.permno, p.cusip, p.comnam, p.ticker, min(p.date) as date format=mmddyy8.
from ticker.permno as p
where p.permno is not null
and p.cusip is not null
and p.comnam is not null
and p.ticker is not null
group by p.permno, p.cusip, p.comnam
having count(p.permno)>=1
order by p.ticker;
;
quit;



%macro merge(name);

proc sort data=ticker.&name out=&name._sorted;
by symbol;
run;

proc sql;
create table ticker.&name._merged as
select a.*, b.* from ticker.&name as a, ticker.distinct as b
where a.symbol = b.ticker
order by a.filename, b.date
;
quit;

data ticker.&name._merged;
retain filename symbol cc_date date;
set ticker.&name._merged;
cc_date_new = input(cc_date, mmddyy8.);
cc_time_new = input(cc_time, time.);
format cc_date_new MMDDYY10.;
format date mmddyy10.;
format cc_time_new tod.;
if not (filename) then delete;
if not (cc_date_new) then delete;
drop ticker cc_date cc_time;
run;

data ticker.&name._merged;
retain filename symbol cc_date date permno cusip comnam cc_time;
set ticker.&name._merged(rename=(cc_date_new=cc_date cc_time_new=cc_time));
if (cc_date < date) then delete;
run;

proc sql;
create table ticker.&name._merged_check as 
select *, max(date) as max_date
from ticker.&name._merged
group by filename
having date=max_date
;
quit;

data ticker.&name._merged;
retain filename ticker CC_Date CC_Time PresWordNum PresCharNum QandAWordNum QandACharNum ShortWords LongWords NegWordsPres NegWordsQA NegWordsTotal;
set ticker.&name._merged_check(rename=(symbol=ticker comnam=ComnName));
label cusip='CUSIP' ComnName='ComnName';
drop max_date date;
run;

proc sql;
create table ticker.&name._merged as
select * from ticker.&name._merged
group by filename
having count(filename)=1
;
quit;

%mend;

%merge(data_fin);
%merge(data_havard);
