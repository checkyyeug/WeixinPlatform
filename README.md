# Uni-App & FastAPI 通用小程序框架

这是一个基于 `uni-app` 和 `FastAPI` 的现代化、前后端分离的微信小程序通用基础框架。它旨在提供一个稳定、高效、易于扩展的开发起点。

## ✨ 项目特性

- **前后端分离:** 清晰的权责分离，便于团队协作和独立部署。
- **现代化技术栈:** 前端采用 Vue 3 和 uni-app，后端采用 Python 3 和 FastAPI。
- **类型安全:** 后端使用 FastAPI 和 Pydantic 保证 API 的类型安全和自动文档生成。
- **ORM 支持:** 使用 SQLAlchemy Core，既提供了强大的数据库操作能力，又保持了灵活性。
- **状态管理:** 前端集成 Pinia，提供清晰、简单的全局状态管理方案。
- **详细文档:** 提供完整的架构、API 和前端设计文档。

## 🛠️ 技术栈

- **前端:**
  - [Vue.js](https://vuejs.org/)
  - [uni-app](https://uniapp.dcloud.io/)
  - [Pinia](https://pinia.vuejs.org/)
- **后端:**
  - [Python 3](https://www.python.org/)
  - [FastAPI](https://fastapi.tiangolo.com/)
  - [Uvicorn](https://www.uvicorn.org/)
  - [SQLAlchemy](https://www.sqlalchemy.org/)
- **数据库:**
  - [MySQL](https://www.mysql.com/)

## 🚀 如何开始

### 后端

1.  **克隆项目:** `git clone <your-repo-url>`
2.  **进入后端目录:** `cd my-fastapi-backend`
3.  **创建并激活虚拟环境:**
    ```bash
    python -m venv venv
    # Windows: .\venv\Scripts\activate
    # macOS/Linux: source venv/bin/activate
    ```
4.  **安装依赖:** `pip install -r requirements.txt` (注: 我们稍后会创建 `requirements.txt`)
5.  **配置环境变量:** 创建 `.env` 文件，并填入数据库连接信息和微信小程序 `appid` 等。
6.  **运行服务:** `uvicorn main:app --reload`
7.  **访问文档:** 打开浏览器访问 `http://127.0.0.1:8000/docs`

### 前端

1.  **安装 HBuilderX:** 从 [DCloud 官网](https://www.dcloud.io/hbuilderx.html) 下载并安装。
2.  **导入项目:** 在 HBuilderX 中导入前端项目目录。
3.  **安装依赖:** `npm install`
4.  **运行到小程序模拟器:** 在 HBuilderX 中点击 "运行" -> "运行到小程序模拟器" -> "微信开发者工具"。

## 📂 项目文档

- **[架构设计 (ARCHITECTURE.md)](ARCHITECTURE.md)**: 了解项目的整体架构和组件设计。
- **[API 设计 (API_DESIGN.md)](API_DESIGN.md)**: 查看详细的后端 API 接口文档。
- **[前端设计 (FRONTEND_DESIGN.md)](FRONTEND_DESIGN.md)**: 查看前端状态管理、组件和目录结构设计。
- **[开发计划 (ROADMAP.md)](ROADMAP.md)**: 查看详细的项目开发任务和路线图。
- **[部署指南 (DEPLOYMENT.md)](DEPLOYMENT.md)**: 查看如何将项目部署到生产服务器。

---
*该项目由 AI 辅助设计和生成。*