SELECT 
    start_state_count - end_state_count 
FROM 
    sde.compress_log 
WHERE 
    compress_end = (SELECT MAX (compress_end) FROM sde.compress_log)