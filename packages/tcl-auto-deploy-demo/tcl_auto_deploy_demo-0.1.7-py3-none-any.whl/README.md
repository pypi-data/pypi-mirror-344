## 用户登录态保存功能

系统现在支持保存用户的登录状态，这意味着用户只需要登录一次，后续使用时将自动恢复登录状态，无需重复输入用户名和密码。

### 使用方法

1. 正常完成登录流程
2. 调用保存登录状态API
   ```python
   await playwright_tool.save_login_state()
   ```
3. 下一次启动时，系统会自动检测并加载已保存的登录状态

### 技术说明

- 登录状态保存在用户主目录下的 `.playwright_storage_state.json` 文件中
- 用户数据保存在用户主目录下的 `.playwright_user_data` 目录中
- 保存的数据包括cookies、localStorage和sessionStorage等浏览器状态信息

### 注意事项

- 如果网站更新了登录机制或者登录状态过期，可能需要重新登录
- 如果遇到登录问题，可以尝试删除保存的状态文件和目录，然后重新登录 