echo 'Preparing to run the tests...'
echo 'Starting the webserver...'

current_dir=`pwd`

python "$current_dir/testsuite/webapp.py" &> /dev/null  & 

webserver_pid="$!"

python "$current_dir/testsuite/test_seleasy.py"

echo 'Shutting down webserver...'
pkill -P $webserver_pid
