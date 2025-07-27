# 漫游精灵后端项目

## 介绍

漫游精灵后端项目，项目介绍详见前端项目。

用户端前端项目：[MineGuYan/WanderAI-FrontEnd: 一款辅助旅行计划制定的 AI 助手的前端](https://github.com/MineGuYan/WanderAI-FrontEnd)

管理端前端项目：[MineGuYan/wanderai-adminend: 漫游精灵管理层前端](https://github.com/MineGuYan/wanderai-adminend)

## 项目结构

```
WanderAI-backend
│   .env			# 环境配置
│   .gitignore      # .gitignore文件
│   LICENSE.md      # 许可证
│   pyproject.toml	# Python项目配置
│   README.md		# README
│   wander_ai.sql   # 数据库脚本
│
└───src
    └───wanderai
        │   Application.py          # 项目启动入口
        │
        ├───agent                   # Agent模块
        │       llm.py              # 大模型实例对象
        │       message.py          # 自定义消息类
        │       wanderai.model.py   # Pydantic模型类
        │       node.py             # LangGraph节点函数
        │       output_parser.py    # 输出解析器
        │       prompt_template.py  # 提示词模板
        │       runnable.py         # 可调用的Agent或Chain
        │       state.py            # 节点状态类
        │       tool.py             # 工具定义
        │       workflow.py         # LangGraph流程图定义
        │       __init__.py
        │
        ├───common              # 通用模块
        │       constant.py     # 常量类
        │       context.py      # 会话上下文管理器
        │       database.py     # 数据库连接
        │       exception.py    # 异常类
        │       log.py          # 日志类
        │       properties.py   # 配置文件
        │       util.py         # 工具类
        │       __init__.py
        │
        ├───model               # 数据模型类
        │       dto.py          # DTO类
        │       entity.py       # 实体类
        │       result.py       # 响应结果类
        │       schema.py       # 数据库模式类
        │       vo.py           # VO类
        │       __init__.py
        │
        └───server              # 服务端业务模块
            │   app.py          # FastAPI APP配置
            │   handler.py      # 全局异常处理器
            │   interceptor.py  # 请求拦截器
            │   __init__.py
            │
            ├───agent                       # Agent接口层
            │       HotspotAgent.py         # 热门景点推荐Agent
            │       TitleGenerator.py       # 标题生成器
            │       TravelChatAgent.py      # 旅行规划Agent
            │       TravelGuideAgent.py     # 旅游向导Agent
            │       __init__.py
            │
            ├───controller                  # 控制器层
            │       AdminController.py      # 管理端路由
            │       ChatController.py       # 旅游规划路由
            │       HistoryController.py    # 历史记录路由
            │       HotspotController.py    # 热门景点路由
            │       SuggestionController.py # 意见反馈路由
            │       UploadController.py     # 文件上传路由
            │       UserController.py       # 用户路由
            │       __init__.py
            │
            ├───mapper                      # 数据库访问层
            │       AdminMapper.py          # 管理员表
            │       SuggestionMapper.py     # 意见表
            │       UserHistoryMapper.py    # 用户历史会话表
            │       UserMapper.py           # 用户表
            │       __init__.py
            │
            └───service                     # 业务逻辑层
                    AdminService.py         # 管理端业务
                    ChatService.py          # 旅游规划业务
                    GuideService.py         # 旅游向导业务
                    HistoryService.py       # 历史会话业务
                    HotspotService.py       # 热门景点业务
                    SuggestionService.py    # 意见反馈业务
                    UserService.py          # 用户业务
                    __init__.py
```

## 环境

### 依赖说明

#### 软件依赖

- Python 3.12.11

- MySQL

- Redis

#### API 依赖

- 阿里云百炼平台

- 阿里云对象存储服务

- 高德地图 API

- 接口盒子 API

- Tavily Search API

- LangSmith（可选）

### 环境变量配置

在项目根目录下创建一个`.env`文件，并配置以下环境变量：

```properties
# Uvicorn配置（可选）
UVICORN_HOST=0.0.0.0
UVICORN_PORT=8080
UVICORN_TIMEOUT_KEEP_ALIVE=120

# 数据库配置
# 使用MySQL 数据库，也可以使用其他数据库，需要在 properties.py 中修改数据库连接字符串
DB_HOST=localhost
DB_PORT=3306
DB_USER=wanderer
DB_PASSWORD=wanderai
DB_NAME=wander_ai

# 数据库连接池配置（可选）
DB_POOL_SIZE=5
DB_MAX_OVERFLOW=10

# Redis 配置（密码可选）
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=2
REDIS_PASSWORD=<your_redis_password>

# 阿里云 OSS 配置
OSS_ACCESS_KEY_ID=<your_oss_access_key_id>
OSS_ACCESS_KEY_SECRET=<your_oss_access_key_secret>
OSS_REGION=<your_oss_region>
OSS_BUCKET_NAME=<your_oss_bucket_name>
OSS_ENDPOINT=<your_oss_endpoint>

# 日志配置（可选）
LOG_LEVEL=DEBUG
LOG_FORMAT="%(asctime)s [%(levelname)s] [%(name)s] [%(filename)s:%(funcName)s:%(lineno)d] - %(message)s"
LOG_DATEFMT="%Y-%m-%d %H:%M:%S"
LOG_FILE_PREFIX="./logs/app"
LOG_ROLL_WHEN="midnight"
LOG_INTERVAL=1
LOG_FILE_SUFFIX="%Y-%m-%d.log"
LOG_SUFFIX_REGEX="^\d{4}-\d{2}-\d{2}.log$"

# JWT 配置（除密钥，其他可选）
JWT_SECRET_KEY=<your_jwt_secret_key>
JWT_TTL_MINUTES=300
JWT_ALGORITHM=HS256
JWT_TOKEN_NAME=Authentication

# 大模型配置
DASHSCOPE_API_KEY=<your_dashscope_api_key>

# 高德地图 API
AMAP_API_KEY=<your_amap_api_key>

# 接口盒子 API
APIHZ_ID=<your_apihz_id>
APIHZ_KEY=<your_apihz_key>

# Tavily API
TAVILY_API_KEY=<your_tavily_api_key>

# LangSmith 配置（可选）
# 如果不使用 LangSmith 进行追踪，可以忽略以下配置
LANGSMITH_TRACING=true
LANGSMITH_ENDPOINT=https://api.smith.langchain.com
LANGSMITH_API_KEY=<your_langsmith_api_key>
LANGCHAIN_TRACING_V2_CONSOLE=false

```

### 数据库配置

#### 创建关系型数据库模式

如果使用 MySQL 数据库，可以使用以下 SQL 脚本创建数据库和表，
其他关系型数据库可以根据实际情况修改脚本。

```sql
drop database if exists wander_ai;
create database if not exists wander_ai;
use wander_ai;

drop table if exists user;
drop table if exists suggestion;
drop table if exists user_history;
drop table if exists admin;

create table user(
	account_id varchar(10) primary key,
    password varchar(255) not null,
    nickname varchar(20) not null
);

create table suggestion(
	id int primary key auto_increment,
	account_id varchar(10) not null,
    message text
);

create table user_history(
	id int primary key auto_increment,
    session_id varchar(150) not null,
	account_id varchar(10) not null,
    title varchar(255)
);

create table admin(
	admin_id varchar(10) primary key,
    password varchar(255) not null
);

-- 创建一个默认的管理员账户，密码为 123456
insert into admin values("12345678", "8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92");
```

#### 启动数据库

启动 MySQL 或自行配置的数据库，并启动 Redis。

## 安装项目

### 下载 .whl 包并安装

从 [releases]() 页面下载最新的 `wanderai_backend-1.0.0-py3-none-any.whl` 文件。

```bash
pip install wanderai_backend-1.0.0-py3-none-any.whl
```

### 从源码构建项目并安装

```bash
git clone https://github.com/njdldkl666699/WanderAI-backend.git
cd WanderAI-backend
python -m build
pip install dist/wanderai_backend-1.0.0-py3-none-any.whl
```

## 启动项目

### 使用命令行启动

在命令行所在目录下配置.env 文件后，直接运行以下命令：

```bash
wanderai-server
```

### 使用 Uvicorn 启动

在项目根目录下配置.env 文件后，使用以下命令启动：

```bash
pip install -e .
uvicorn src.wanderai.server.app:app [其他参数]
```

#### 使用 Python 启动

在项目根目录下配置.env 文件后，使用以下命令启动：

```bash
pip install -e .
python src/wanderai/Application.py
```

## 项目贡献与联系方式

### 开发者

- [南极大陆的可乐](https://github.com/njdldkl666699) : 2312454@mail.nankai.edu.cn

- [轻舟](https://github.com/2337394436) :

欢迎通过以下方式贡献：

- 提交 Issue

- 提交 Pull Request
