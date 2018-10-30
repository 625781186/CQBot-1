# 这是创建酷Q服务
#docker run --name=coolq -d -p 8080:9000 -v /coolq-data:/home/user/coolq -e VNC_PASSWD=qq517653943 -e COOLQ_ACCOUNT=10000 coolq/wine-coolq

#启动命令
docker start coolq

#停止命令
#docker stop coolq
