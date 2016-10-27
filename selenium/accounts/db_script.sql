-- Take care of jonis
select
ac.code as account_code,
ac.name as account_name
,p.code as parent_code,p.name as parent_name,
ac.type as internal_type,
ac_type.name as account_type,
comp.name as company_name ,
ac.company_id,
ac.user_type
from account_account ac 
full outer join account_account p on ac.parent_id= p.id
full outer join res_company comp on comp.id=ac.company_id
inner join account_account_type ac_type on ac_type.id = ac.user_type
where ac.code is not null and ac.company_id in (7,8,9) 
order by  length(ac.code), ac.code

/*
select * from account_account
*/