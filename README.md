# 漫游精灵后端项目

## 介绍

漫游精灵后端项目，项目介绍详见前端项目。

## 项目结构

```
WanderAI-backend
│   .env						# 环境配置
│   .gitignore					# .gitignore文件
│   Application.py				# 项目启动入口
│   README.md					# README
│   requirements.txt			# 项目依赖
│
├───agent						# Agent模块
│       llm.py					# 大模型实例对象
│       message.py				# 自定义消息类
│       model.py				# Pydantic模型类
│       node.py					# LangGraph节点函数
│       output_parser.py		# 输出解析器
│       prompt_template.py		# 提示词模板
│       runnable.py				# 可调用的Agent或Chain
│       state.py				# 节点状态类
│       tool.py					# 工具定义
│       workflow.py				# LangGraph流程图定义
│
├───common						# 通用模块
│       constant.py				# 常量类
│       context.py				# 会话上下文管理器
│       database.py				# 数据库连接
│       exception.py			# 异常类
│       log.py					# 日志类
│       properties.py			# 配置文件
│       util.py					# 工具类
│
├───model						# 数据模型类
│       dto.py					# DTO类
│       entity.py				# 实体类
│       result.py				# 响应结果类
│       schema.py				# 数据库模式类
│       vo.py					# VO类
│
└───server						# 服务端业务模块
    │   app.py					# FastAPI APP配置
    │   handler.py				# 全局异常处理器
    │   interceptor.py			# 请求拦截器
    │
    ├───agent						# Agent接口层
    │       HotspotAgent.py			# 热门景点推荐Agent
    │       TitleGenerator.py		# 标题生成器
    │       TravelChatAgent.py		# 旅行规划Agent
    │       TravelGuideAgent.py		# 旅游向导Agent
    │
    ├───controller					# 控制器层
    │       AdminController.py		# 管理端路由
    │       ChatController.py		# 旅游规划路由
    │       HistoryController.py	# 历史记录路由
    │       HotspotController.py	# 热门景点路由
    │       SuggestionController.py	# 意见反馈路由
    │       UploadController.py		# 文件上传路由
    │       UserController.py		# 用户路由
    │
    ├───mapper						# 数据库访问层
    │       AdminMapper.py			# 管理员表
    │       SuggestionMapper.py		# 意见表
    │       UserHistoryMapper.py	# 用户历史会话表
    │       UserMapper.py			# 用户表
    │
    └───service						# 业务逻辑层
            AdminService.py			# 管理端业务
            ChatService.py			# 旅游规划业务
            GuideService.py			# 旅游向导业务
            HistoryService.py		# 历史会话业务
            HotspotService.py		# 热门景点业务
            SuggestionService.py	# 意见反馈业务
            UserService.py			# 用户业务
```

## 环境依赖

### 软件依赖

- Python 3.12.11

- MySQL

- Redis

### API 依赖

- 阿里云百炼平台

- 阿里云对象存储服务

- 高德地图 API

- 接口盒子 API

- Tavily Search API

- LangSmith（可选）

## 构建和运行

### 克隆项目

```bash
git clone https://github.com/njdldkl666699/WanderAI-backend.git
```

### 安装依赖

按照`pyproject.toml`中的依赖安装项目所需的 Python 包。

### 配置环境变量

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

### 启动数据库

启动 MySQL 或自行配置的数据库，并启动 Redis。

### 运行项目

项目启动本身非常简单，只需运行 `src/Application.py` 即可。

```bash
python src/Application.py
```

## 项目贡献与联系方式

### 开发者

- [南极大陆的可乐](https://github.com/njdldkl666699) : 2312454@mail.nankai.edu.cn

- [轻舟](https://github.com/2337394436) :

欢迎通过以下方式贡献：

- 提交 Issue

- 提交 Pull Request
