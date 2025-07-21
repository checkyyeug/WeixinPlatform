# 项目架构设计文档

## 1. 项目概述

本项目旨在创建一个通用的微信小程序基础框架。框架采用前后端分离的设计思想，旨在提供一套稳定、可复用、易于扩展的解决方案。

- **前端技术栈:** Vue.js + uni-app
- **后端技术栈:** Python + FastAPI + SQLAlchemy
- **数据库:** MySQL

## 2. 整体架构

```mermaid
graph TD
    subgraph 前端 (uni-app)
        A[用户界面 - Vue Components]
        B[页面路由 - pages.json]
        C[状态管理 - Pinia/Vuex]
        D[API请求层 - api.js]
    end

    subgraph 后端 (Python)
        E[Web服务器 - Nginx]
        F[ASGI服务器 - Uvicorn]
        G[Web框架 - FastAPI]
        H[数据模型层 - Pydantic]
        I[ORM - SQLAlchemy]
    end

    subgraph 数据库
        J[MySQL]
    end

    A --> B
    A --> C
    A --> D

    D -- HTTP/HTTPS --> E
    E -- HTTP Proxy --> F
    F -- ASGI --> G
    G -- Uses --> H
    G -- Uses --> I
    I -- SQL --> J
```

## 3. 组件说明

### 3.1 前端 (uni-app)

- **用户界面 (Vue Components):** 基于 Vue.js 的组件，负责构建小程序的视图层。
- **页面路由 (pages.json):** uni-app 的核心配置文件，用于定义小程序的页面路径、窗口表现和导航行为。
- **状态管理 (Pinia/Vuex):** 用于管理全局应用状态，如用户信息、登录状态、应用配置等，实现跨页面、跨组件的数据共享。
- **API请求层 (api.js):** 一个封装了 `uni.request` 的模块，用于统一处理所有与后端的 HTTP 通信。它将负责添加认证头 (Token)、处理公共错误、管理请求基地址 (Base URL) 等。

### 3.2 后端 (Python)

- **Web服务器 (Nginx):** 作为反向代理服务器，是生产环境的入口。主要负责：
    - 负载均衡
    - 处理 HTTPS (SSL 终止)
    - 托管静态文件 (如果需要)
    - 将 API 请求安全地转发给 ASGI 服务器。
- **ASGI服务器 (Uvicorn):** 一个高性能的异步网关接口 (ASGI) 服务器，负责运行 FastAPI 应用程序，并处理来自 Nginx 的并发请求。
- **Web框架 (FastAPI):** 后端的核心框架，负责：
    - API 路由定义
    - 请求参数的解析与验证
    - 依赖注入
    - 业务逻辑处理
    - 生成自动化的 API 文档 (Swagger UI / ReDoc)。
- **数据模型层 (Pydantic):** FastAPI 的基础，用于定义清晰、类型安全的数据模型，对请求和响应的数据进行自动验证、解析和文档化。
- **ORM (SQLAlchemy):** 对象关系映射器，将 Python 对象 (`class`) 与数据库表进行映射，使开发者可以用面向对象的方式操作数据库，而无需编写原生 SQL 语句。

### 3.3 数据库 (MySQL)

- 使用 MySQL 作为持久化存储方案，负责存储所有业务数据，如用户表、订单表、商品表等。数据库表的设计将遵循第三范式，并通过索引优化查询性能。

## 4. 关键数据流示例：用户登录

1.  **前端:** 用户在小程序中点击登录按钮，调用 `wx.login()` 获取临时 `code`。
2.  **前端:** 将 `code` 通过 API 请求层发送到后端的 `/api/v1/auth/login` 接口。
3.  **后端 (Nginx -> Uvicorn -> FastAPI):** FastAPI 应用接收到请求。
4.  **后端:** 调用微信官方接口，用 `code`、`appid` 和 `app_secret` 换取用户的 `openid` 和 `session_key`。
5.  **后端 (SQLAlchemy):** 查询数据库中是否存在该 `openid`。
    - **如果存在:** 更新用户的 `last_login_time`。
    - **如果不存在:** 创建一条新的用户记录。
6.  **后端:** 使用 JWT (JSON Web Token) 或其他 Token 方案，生成一个代表用户登录状态的 `access_token`。
7.  **后端:** 将 `access_token` 和部分用户信息作为响应返回给前端。
8.  **前端:** 接收到 `access_token`，将其安全地存储在本地 (如 `uni.setStorageSync`)，并更新全局状态管理库中的用户登录状态。
9.  **后续请求:** 前端在之后的所有 API 请求中，都在请求头 `Authorization` 中携带此 `access_token`。
10. **后端:** FastAPI 通过中间件或依赖注入验证每个请求的 `access_token`，以确认用户身份。
