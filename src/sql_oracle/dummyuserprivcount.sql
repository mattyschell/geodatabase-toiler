select 
    count(*) 
from 
    user_tab_privs
where 
    owner = user
and table_name = 'TOILERTESTFC'
and grantee = (select 
                    max(username) 
               from 
                    all_users
               where 
                    oracle_maintained = 'N'
               and username <> user)