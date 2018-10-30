# ps -ef|grep BotServer|grep -v grep|cut -c 9-15|xargs kill -9
wget http://127.0.0.1:9898/kill/ > /tmp/quit.txt
sleep 2
nohup python3 BotServer.py > log.txt 2>&1 &
