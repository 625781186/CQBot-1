# ps -ef|grep BotServer|grep -v grep|cut -c 9-15|xargs kill -9
rm index.html
wget http://127.0.0.1:9898/kill/
sleep 2
nohup python3 BotServer.py > log.txt 2>&1 &
