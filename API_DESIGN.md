# 后端 API 详细设计文档

## 1. 通用约定

- **Base URL:** `/api/v1`
- **认证方式:** Bearer Token (JWT)
  - 需要认证的接口，请求头需包含 `Authorization: Bearer <your_token>`。
- **成功响应结构:**
  ```json
  {
    "code": 0,
    "message": "Success",
    "data": { ... }
  }
  ```
- **失败响应结构:**
  ```json
  {
    "code": 40001, // 业务错误码
    "message": "Invalid input parameters",
    "data": null
  }
  ```

## 2. 模块: 认证 (Auth)

### 2.1 用户登录或注册

此接口处理小程序用户的首次登录和后续登录。后端通过 `code` 换取 `openid`，如果 `openid` 不存在则创建新用户，否则视为登录。

- **Endpoint:** `POST /auth/login`
- **描述:** 使用小程序提供的临时 code 进行登录或注册。
- **认证:** 无需

#### 请求体 (Request Body)

- **Content-Type:** `application/json`

```json
{
  "code": "string", // wx.login() 获取的临时 code
  "user_info": { // 可选，用户授权后传入
    "nickName": "string",
    "avatarUrl": "string",
    "gender": "number" // 0:未知, 1:男, 2:女
  }
}
```

#### 成功响应 (200 OK)

```json
{
  "code": 0,
  "message": "Success",
  "data": {
    "access_token": "string", // JWT Token
    "token_type": "bearer"
  }
}
```

#### 失败响应

- **422 Unprocessable Entity:** 请求体验证失败 (如 `code` 缺失)。
  ```json
  {
    "detail": [
      {
        "loc": ["body", "code"],
        "msg": "field required",
        "type": "value_error.missing"
      }
    ]
  }
  ```
- **500 Internal Server Error:** 微信接口调用失败或数据库错误。
  ```json
  {
    "code": 50001,
    "message": "Failed to fetch openid from weixin server",
    "data": null
  }
  ```

## 3. 模块: 用户 (Users)

### 3.1 获取当前用户信息

获取当前已登录用户的详细信息。

- **Endpoint:** `GET /users/me`
- **描述:** 获取当前用户的个人资料。
- **认证:** **需要**

#### 成功响应 (200 OK)

```json
{
  "code": 0,
  "message": "Success",
  "data": {
    "id": "integer",
    "openid": "string",
    "nickname": "string",
    "avatar_url": "string",
    "gender": "integer",
    "mobile": "string",
    "last_login_time": "string (datetime)"
  }
}
```

#### 失败响应

- **401 Unauthorized:** Token 无效、过期或未提供。
  ```json
  {
    "detail": "Not authenticated"
  }
  ```
