docker stop $(docker ps -a -q) 或者 docker stop $(docker ps -aq)
docker rm $(docker ps -a -q) 或者 docker rm $(docker ps -aq)
docker rmi $(docker images -q)

