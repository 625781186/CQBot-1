ps -ef|grep botserver|grep -v grep|cut -c 9-15|xargs kill -9
nohup python3 botserver.py > log.txt 2>&1 &
