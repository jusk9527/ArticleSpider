docker pull mongo
docker run --name mongodb -p 27017:27017 -d mongo
docker exec -it mongodb mongo admin
db.createUser({ user: 'root', pwd: 'root', roles: [ { role: "userAdminAnyDatabase", db: "admin" } ] });
exit


docker exec -it mongodb mongo admin
db.auth("root","root");
db.createUser({ user: 'xiaohua', pwd: 'xiaohua123456', roles: [ { role: "readWrite", db: "app" } ] });
exit


docker exec -it mongodb mongo admin

db.auth("xiaohua","xiaohua123456");
use app
db.test.save({name:"xiaohua"});
exit