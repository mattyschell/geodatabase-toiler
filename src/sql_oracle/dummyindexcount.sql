select count(*) 
from 
    user_indexes
where 
    table_owner = user
and table_name = 'TOILERTESTFC'
and index_name LIKE 'TOILERTESTFCBORO%'