DIR_WITH_DATA_TO_UPLOAD="/upload"
GRAPH_NAME="http://foodpedia.tk/"
SERVER_PORT=1111
USERNAME=dba
PASSWORD=dba

if [ "$(ls -A $DIR_WITH_DATA_TO_UPLOAD)" ]
then
  isql-vt $SERVER_PORT $USERNAME $PASSWORD exec="ld_dir_all('$DIR_WITH_DATA_TO_UPLOAD', '*', '$GRAPH_NAME');"
  isql-vt $SERVER_PORT $USERNAME $PASSWORD exec="rdf_loader_run();" 
  #wait 
  #isql-vt 1111 dba dba exec="checkpoint;" 
else
  echo "$DIR_WITH_DATA_TO_UPLOAD is empty. Nothing to upload."
fi
