DB.DBA.VHOST_REMOVE (
     lhost=>'*ini*',
     vhost=>'*ini*',
     lpath=>'/sparql'
);

DB.DBA.VHOST_DEFINE (
     lhost=>'*ini*',
     vhost=>'*ini*',
     lpath=>'/sparql',
     ppath=>'/!sparql/',
     is_dav=>1,
     def_page=>'',
     vsp_user=>'dba',
     ses_vars=>0,
     opts=>vector ('browse_sheet', '', 'noinherit', 'yes', 'cors', '*', 'cors_restricted', 0),
     is_default_host=>0
);
