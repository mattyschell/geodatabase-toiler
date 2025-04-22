-- if you follow the ESRI PL/SQL down the rabbit hole
-- at the end this is what happens
-- alternatively request the nutty elevated privileges required 
insert into sde.server_config (
     prop_name
    ,char_prop_value
    ,num_prop_value )
select 
     'OPEN_CURSORS'
    ,NULL
    ,value 
from 
    v$parameter 
where 
    name = 'open_cursors';
commit;