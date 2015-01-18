DIR_WITH_DATA_TO_UPLOAD="/upload"
GRAPH_NAME="http://foodpedia.tk"

if [ "$(ls -A $DIR_WITH_DATA_TO_UPLOAD)" ]
then
  isql-vt 1111 dba dba exec="ld_dir_all('$DIR_WITH_DATA_TO_UPLOAD', '*.ttl', '$GRAPH_NAME');"
  isql-vt 1111 dba dba exec="rdf_loader_run();" 
  #wait 
  #isql-vt 1111 dba dba exec="checkpoint;" 
else
  echo "$DIR_WITH_DATA_TO_UPLOAD is empty. Nothing to upload."
fi
