# 阿里云服务器部署指南 (Ubuntu)

本文档旨在指导您如何将 FastAPI 后端应用部署到阿里云轻量应用服务器 (Ubuntu 20.04+)。

我们将使用 Nginx 作为反向代理，Gunicorn 作为 ASGI 服务器来运行生产环境的 FastAPI 应用，并使用 Supervisor 来保证服务的稳定性。

## 1. 服务器初始化

1.  **更新系统:**
    ```bash
    sudo apt update && sudo apt upgrade -y
    ```
2.  **安装必要工具:**
    ```bash
    sudo apt install -y python3-pip python3-venv git nginx
    ```

## 2. 部署代码

1.  **克隆项目:**
    ```bash
    git clone https://github.com/checkyyeug/WeixinPlatform.git
    cd WeixinPlatform
    ```
2.  **创建虚拟环境并安装依赖:**
    ```bash
    cd my-fastapi-backend
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt 
    ```
    *(注意: `requirements.txt` 将在开发过程中生成)*

## 3. 配置 Gunicorn

Gunicorn 是一个成熟的 Python WSGI/ASGI HTTP 服务器，比 Uvicorn 的独立运行模式更适合生产环境。

1.  **安装 Gunicorn:**
    ```bash
    pip install gunicorn
    ```
2.  **测试 Gunicorn:**
    在 `my-fastapi-backend` 目录下，运行以下命令测试 Gunicorn 是否能成功启动应用。
    ```bash
    gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
    ```
    - `-w 4`: 启动 4 个 worker 进程。
    - `-k uvicorn.workers.UvicornWorker`: 使用 uvicorn 的 worker 类来处理异步请求。

## 4. 配置 Supervisor

Supervisor 是一个进程管理工具，可以在应用意外退出时自动重启，保证服务的高可用性。

1.  **安装 Supervisor:**
    ```bash
    sudo apt install -y supervisor
    ```
2.  **创建配置文件:**
    在 `/etc/supervisor/conf.d/` 目录下创建一个新的配置文件，例如 `fastapi_app.conf`。
    ```bash
    sudo nano /etc/supervisor/conf.d/fastapi_app.conf
    ```
3.  **写入配置:**
    将以下内容复制到文件中，并根据您的实际路径进行修改。
    ```ini
    [program:fastapi_app]
    command=/path/to/your/project/my-fastapi-backend/venv/bin/gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
    directory=/path/to/your/project/my-fastapi-backend
    user=your_user_name
    autostart=true
    autorestart=true
    stderr_logfile=/var/log/fastapi_app.err.log
    stdout_logfile=/var/log/fastapi_app.out.log
    ```
4.  **启动服务:**
    ```bash
    sudo supervisorctl reread
    sudo supervisorctl update
    sudo supervisorctl start fastapi_app
    ```

## 5. 配置 Nginx

Nginx 作为反向代理，将外部的 HTTP 请求转发到 Gunicorn 运行的本地端口 (默认为 8000)。

1.  **创建 Nginx 配置文件:**
    ```bash
    sudo nano /etc/nginx/sites-available/fastapi_app
    ```
2.  **写入配置:**
    将以下内容复制到文件中，并将 `your_domain.com` 替换为您的域名或服务器 IP。
    ```nginx
    server {
        listen 80;
        server_name your_domain.com;

        location / {
            proxy_pass http://127.0.0.1:8000;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }
    }
    ```
3.  **创建软链接以启用配置:**
    ```bash
    sudo ln -s /etc/nginx/sites-available/fastapi_app /etc/nginx/sites-enabled
    ```
4.  **测试并重启 Nginx:**
    ```bash
    sudo nginx -t
    sudo systemctl restart nginx
    ```

## 6. 配置防火墙

如果您的服务器开启了防火墙 (如 `ufw`)，请确保开放了 HTTP (80) 和 HTTPS (443) 端口。

```bash
sudo ufw allow 'Nginx Full'
```

至此，您的 FastAPI 应用已成功部署到阿里云服务器上。