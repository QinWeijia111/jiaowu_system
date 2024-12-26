# 教务系统设计

这是一个基于 Vue.js + Flask 的教务管理系统，实现了学生信息管理、课程管理和选课管理等功能。

## 项目结构

```
jiaowu_system_design/
├── sys_frontend/                # 前端项目
│   ├── build/                  # 构建配置文件
│   ├── config/                 # 项目配置文件
│   ├── src/                    # 源代码
│   │   ├── components/        # Vue组件
│   │   ├── router/           # 路由配置
│   │   └── views/            # 页面视图
│   └── static/                # 静态资源
└── sys_backend/                # 后端项目
    ├── sys_back.py           # Flask后端服务
    └── requirements.txt      # Python依赖
```

## 主要功能

### 学生管理

- 查看学生列表
- 添加学生信息
- 修改学生信息
- 删除学生信息

### 课程管理

- 查看课程列表
- 添加课程信息
- 修改课程信息
- 删除课程信息

### 选课系统

- 查看选课信息
- 学生选课
- 录入成绩
- 退选课程

## 技术栈

### 前端

- Vue.js
- Vue Router
- Element UI
- Axios

### 后端

- Flask
- PyMySQL
- Flask-CORS

### 数据库

- MySQL

## 使用说明

1. 启动后端服务

```bash
cd sys_backend
python sys_back.py
```

2. 启动前端开发服务器

```bash
cd sys_frontend
npm install
npm run dev
```

3. 访问系统
   打开浏览器访问: `http://localhost:8080`

## API 说明

### 用户接口

- `/login/login`: POST 请求，用户登录

### 学生管理接口

- `/student/stu_list`: POST 请求，获取学生列表
- `/student/stu_insert`: POST 请求，添加学生
- `/student/stu_update`: POST 请求，更新学生信息
- `/student/stu_delete`: POST 请求，删除学生

### 课程管理接口

- `/course/course_list`: POST 请求，获取课程列表
- `/course/course_insert`: POST 请求，添加课程
- `/course/course_update`: POST 请求，更新课程信息
- `/course/course_delete`: POST 请求，删除课程

### 选课系统接口

- `/sc_system/list`: POST 请求，获取选课信息
- `/sc_system/insert`: POST 请求，添加选课记录
- `/sc_system/delete`: POST 请求，删除选课记录

## 数据库设计

系统使用了以下主要数据表：

- `student`: 学生信息表
- `course`: 课程信息表
- `sc`: 选课记录表
- `user`: 用户表

## 贡献指南

欢迎提交 Issue 和 Pull Request 来帮助改进项目。
