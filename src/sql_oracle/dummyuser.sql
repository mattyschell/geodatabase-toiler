select 
    max(username) 
from 
    all_users
where 
    oracle_maintained = 'N'
and username <> user