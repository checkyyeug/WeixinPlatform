# 前端设计文档

## 1. 目录结构

我们将采用功能清晰、易于维护的目录结构。

```
/
|-- api/                  # API 请求模块
|   |-- auth.js
|   |-- user.js
|-- components/           # 可复用的 Vue 组件
|   |-- Common/           # 通用基础组件
|   |-- Business/         # 业务相关组件
|-- pages/                # 页面
|   |-- index/
|   |-- my/
|-- static/               # 静态资源 (图片等)
|-- store/                # 状态管理 (Pinia/Vuex)
|   |-- modules/
|   |   |-- user.js       # 用户模块
|   |-- index.js          # Store 入口
|-- utils/                # 工具函数
|   |-- request.js        # 请求封装
|-- App.vue               # 应用入口
|-- main.js               # Vue 入口
|-- pages.json            # 页面配置
|-- uni.scss              # 全局样式变量
```

## 2. 状态管理 (Pinia 为例)

我们将使用 Pinia 作为首选的状态管理库，它更轻量，且完美支持 Vue 3。

### 2.1 User Store (`store/modules/user.js`)

这个模块负责管理用户的登录状态、Token 和个人信息。

**State:**

- `token`: (String) 用户的 `access_token`，从本地存储初始化。
- `userInfo`: (Object) 用户的详细信息。

**Getters:**

- `isLoggedIn`: (Boolean) 计算属性，通过检查 `token` 是否存在来判断用户是否已登录。
- `userProfile`: (Object) 返回 `userInfo`。

**Actions:**

- `login(code)`:
    1. 调用 `api/auth.js` 中的登录接口。
    2. 成功后，将获取到的 `token` 保存到 state 和本地存储中。
    3. 返回 Promise。
- `getUserInfo()`:
    1. 调用 `api/user.js` 中的获取用户信息接口。
    2. 成功后，将用户信息保存到 `userInfo` state 中。
- `logout()`:
    1. 清空 state 中的 `token` 和 `userInfo`。
    2. 清空本地存储中的 `token`。

## 3. API 请求封装 (`utils/request.js`)

为了统一处理请求，我们将封装 `uni.request`。

**核心功能:**

1.  **基础配置:** 设置基础 URL (`baseURL`) 和超时时间 (`timeout`)。
2.  **请求拦截器:**
    - 在每个请求发送前被调用。
    - 检查 `user` store 中是否存在 `token`。
    - 如果存在，则在请求头中自动添加 `Authorization: Bearer <token>`。
3.  **响应拦截器:**
    - 在接收到响应后被调用。
    - **业务成功判断:** 检查后端返回的业务 `code` 是否为 `0`。如果不是，则统一处理错误（如 `uni.showToast`）。
    - **Token 失效处理:** 如果后端返回 `401 Unauthorized`，则自动调用 `user` store 中的 `logout` action，并导航到登录页。
    - **数据剥离:** 如果业务成功，直接返回响应体中的 `data` 部分，简化页面中的调用。

**示例:**

```javascript
// utils/request.js
import { useUserStore } from '@/store/modules/user';

const request = (options) => {
  return new Promise((resolve, reject) => {
    const userStore = useUserStore();

    uni.request({
      ...options,
      header: {
        ...options.header,
        Authorization: userStore.token ? `Bearer ${userStore.token}` : ''
      },
      success: (res) => {
        // ... 响应拦截逻辑
        if (res.data.code === 0) {
          resolve(res.data.data);
        } else {
          // ... 错误处理
          reject(res.data);
        }
      },
      fail: (err) => {
        // ... 网络错误处理
        reject(err);
      }
    });
  });
};

export default request;
```

## 4. 通用业务组件示例

### `LoginButton` 组件

一个封装了完整登录流程的按钮。

**Props:**

- `text`: (String) 按钮显示的文字，默认为 "一键登录"。

**Events:**

- `@success`: 登录成功后触发，返回用户信息。
- `@fail`: 登录失败后触发，返回错误信息。

**内部逻辑:**

1.  按钮被点击。
2.  调用 `uni.getUserProfile` 获取用户授权（头像、昵称）。
3.  调用 `uni.login` 获取 `code`。
4.  调用 `user` store 中的 `login` action，传入 `code` 和用户信息。
5.  调用 `user` store 中的 `getUserInfo` action。
6.  根据结果触发 `@success` 或 `@fail` 事件。
