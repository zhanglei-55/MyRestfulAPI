### 使用Python Flask实现Rest API

#### 1. 克隆仓库代码

```shell
git clone https://github.com/zhanglei-55/MyRestfulAPI.git
```

#### 2. 安装相关依赖

> **注意**
>
> 在此之前，你需要先创建一个Python的虚拟机环境=>我使用Pychram会自己创建
>
> 目前请自行解决

```shell
pip install -r ./requirements.txt
```

#### 3.修改app.py文件

```py
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://user:password@host/databases'
# 将16行的这行修改为自己的数据库, 或者使用测试数据库
```

#### 4.创建或修改数据库表结构

- 在数据库中创建如下表结构的数据库:

```sql
+------------+--------------+------+-----+-------------------+-----------------------------------------------+
| Field      | Type         | Null | Key | Default           | Extra                                         |
+------------+--------------+------+-----+-------------------+-----------------------------------------------+
| id         | int          | NO   | PRI | NULL              | auto_increment                                |
| phone      | varchar(255) | NO   | UNI | NULL              |                                               |
| username   | varchar(255) | NO   | UNI | NULL              |                                               |
| password   | varchar(255) | NO   |     | NULL              |                                               |
| createtime | datetime     | YES  |     | CURRENT_TIMESTAMP | DEFAULT_GENERATED                             |
| updatetime | datetime     | YES  |     | CURRENT_TIMESTAMP | DEFAULT_GENERATED on update CURRENT_TIMESTAMP |
+------------+--------------+------+-----+-------------------+-----------------------------------------------+
```

- 执行如下sql语句创建

```sql
use yourdatabase;
CREATE TABLE user (
  id int NOT NULL AUTO_INCREMENT,
  phone varchar(255) NOT NULL UNIQUE,
  username varchar(255) NOT NULL UNIQUE,
  password varchar(255) NOT NULL,
  createtime datetime DEFAULT CURRENT_TIMESTAMP,
  updatetime datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id)
);
```

#### 5. 运行app.py

```shell
python app.py
```

