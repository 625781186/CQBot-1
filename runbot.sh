ps -ef|grep BotServer|grep -v grep|cut -c 9-15|xargs kill -9
nohup python3 BotServer.py > log.txt 2>&1 &
