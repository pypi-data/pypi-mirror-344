"""
自动化部署服务实现
提供基于Playwright的浏览器自动化和登录功能
"""
import logging
import asyncio
import os
import time
from typing import Dict, Any
from playwright.async_api import async_playwright

logger = logging.getLogger(__name__)

class PlaywrightService:
    """Playwright 自动化服务，用于处理页面访问相关的功能"""

    def __init__(self, config: Dict[str, Any]):
        """初始化 Playwright 自动化服务

        Args:
            config: 配置信息，包含账号密码等
        """
        logger.info(f"初始化 Playwright 自动化服务")
        self.config = config
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None
        self.user_data = {}
        self.is_initialized = False
        self.is_logged_in = False  # 添加登录状态跟踪
        self.headless = False  # 添加headless属性
        # 存储状态相关配置
        self.storage_state_path = os.path.join(os.path.expanduser("~"), ".playwright_storage_state.json")
        
    async def initialize(self):
        """初始化浏览器服务（不启动浏览器）"""
        try:
            logger.info("初始化Playwright服务")
            self.is_initialized = True
            self.is_logged_in = False
            return True
        except Exception as e:
            logger.error(f"初始化Playwright服务失败: {str(e)}", exc_info=True)
            return False
        
    async def ensure_browser(self):
        """确保浏览器已启动，如果未启动则启动浏览器"""
        # 如果浏览器已启动，检查是否可用
        if self.browser and self.page:
            try:
                await self.page.evaluate("1")  # 简单测试
                return True
            except Exception as e:
                logger.warning(f"浏览器状态检查失败: {e}")
                await self._cleanup_browser()
        
        # 启动新的浏览器实例
        try:
            logger.info("启动浏览器实例")
            if not self.playwright:
                self.playwright = await async_playwright().start()
            
            # 启动浏览器
            self.browser = await self.playwright.chromium.launch(headless=self.headless)
            logger.info("浏览器启动成功")
            
            # 创建上下文
            context_options = {"viewport": {"width": 1280, "height": 800}}
            
            # 如果存在存储状态文件，加载它
            if os.path.exists(self.storage_state_path):
                try:
                    context_options["storage_state"] = self.storage_state_path
                    logger.info(f"加载存储状态: {self.storage_state_path}")
                except Exception as e:
                    logger.warning(f"加载存储状态失败: {e}")
            
            # 创建上下文
            self.context = await self.browser.new_context(**context_options)
            
            # 创建页面
            self.page = await self.context.new_page()
            logger.info("页面创建成功")
            
            return True
        except Exception as e:
            logger.error(f"启动浏览器失败: {str(e)}", exc_info=True)
            return False
    
    async def _cleanup_browser(self):
        """清理浏览器资源"""
        try:
            if self.page:
                await self.page.close()
                self.page = None
            
            if self.context:
                # 保存状态
                try:
                    await self.context.storage_state(path=self.storage_state_path)
                    logger.info(f"保存浏览器状态到: {self.storage_state_path}")
                except Exception as e:
                    logger.warning(f"保存状态失败: {e}")
                
                await self.context.close()
                self.context = None
            
            if self.browser:
                await self.browser.close()
                self.browser = None
            
            if self.playwright:
                await self.playwright.stop()
                self.playwright = None
            
            logger.info("浏览器资源已清理")
        except Exception as e:
            logger.error(f"清理浏览器资源出错: {str(e)}")
    
    async def navigate_to(self, url: str) -> bool:
        """导航到指定URL
        
        Args:
            url: 目标URL
            
        Returns:
            bool: 导航是否成功
        """
        try:
            # 确保浏览器已启动
            if not await self.ensure_browser():
                return False
            
            # 导航到目标页面
            logger.info(f"导航到: {url}")
            await self.page.goto(url, wait_until='networkidle')
            
            # 检查是否被重定向到登录页面
            current_url = self.page.url
            if "login" in current_url.lower() and current_url != url:
                logger.warning(f"被重定向到登录页面: {current_url}")
                self.is_logged_in = False
                return False
            
            # 保存状态
            await self._save_storage_state()
            
            return True
        except Exception as e:
            logger.error(f"导航失败: {str(e)}", exc_info=True)
            return False
    
    async def _save_storage_state(self):
        """保存浏览器状态"""
        if self.context:
            try:
                await self.context.storage_state(path=self.storage_state_path)
                logger.info(f"已保存浏览器状态到: {self.storage_state_path}")
                return True
            except Exception as e:
                logger.error(f"保存状态失败: {e}")
        return False
    
    async def extract_text_content(self) -> str:
        """提取页面文本内容"""
        if not self.page:
            return ""
        try:
            return await self.page.text_content('body')
        except Exception as e:
            logger.error(f"提取页面内容失败: {str(e)}", exc_info=True)
            return ""
    
    async def fill_form(self, selector: str, value: str) -> bool:
        """填写表单字段"""
        try:
            await self.page.fill(selector, value)
            return True
        except Exception as e:
            logger.error(f"填写表单失败: {str(e)}", exc_info=True)
            return False
    
    async def click_element(self, selector: str) -> bool:
        """点击元素"""
        try:
            await self.page.click(selector)
            return True
        except Exception as e:
            logger.error(f"点击元素失败: {str(e)}", exc_info=True)
            return False
    
    async def wait_for_selector(self, selector: str, timeout: int = 30000) -> bool:
        """等待元素出现"""
        try:
            await self.page.wait_for_selector(selector, timeout=timeout)
            return True
        except Exception as e:
            logger.error(f"等待元素出现超时: {str(e)}", exc_info=True)
            return False
    
    def set_headless(self, headless: bool) -> None:
        """设置浏览器可见性"""
        self.headless = headless
        logger.info(f"设置浏览器可见性: {'隐藏' if headless else '显示'}")
    
    async def login(self) -> bool:
        """执行登录操作
        
        Returns:
            bool: 登录是否成功
        """
        try:
            
            # 从配置中获取用户名和密码
            username = self.config.get('username')
            password = self.config.get('password')
            
            if not username or not password:
                logger.error("缺少登录凭据")
                return False
                
            logger.info(f"开始登录操作，用户名: {username}")
            
            # 查找用户名输入框
            username_selectors = ['input[name="username"]', '#username', 'input[placeholder="用户名"]']
            username_filled = False
            for selector in username_selectors:
                try:
                    username_input = await self.page.query_selector(selector)
                    if username_input:
                        await username_input.fill(username)
                        logger.info(f"已填写用户名，使用选择器: {selector}")
                        username_filled = True
                        break
                except Exception as e:
                    logger.warning(f"尝试填写用户名时出错 ({selector}): {e}")
            
            if not username_filled:
                logger.warning("未找到用户名输入框，尝试使用键盘输入")
                try:
                    # 尝试使用按Tab键和输入的方式
                    await self.page.keyboard.press('Tab')
                    await self.page.keyboard.type(username)
                    username_filled = True
                except Exception as e:
                    logger.error(f"键盘输入用户名失败: {e}")
            
            if not username_filled:
                logger.error("无法填写用户名")
                return False
            
            # 查找密码输入框
            password_selectors = ['input[name="password"]', '#password', 'input[type="password"]', 'input[placeholder="密码"]']
            password_filled = False
            for selector in password_selectors:
                try:
                    password_input = await self.page.query_selector(selector)
                    if password_input:
                        await password_input.fill(password)
                        logger.info(f"已填写密码，使用选择器: {selector}")
                        password_filled = True
                        break
                except Exception as e:
                    logger.warning(f"尝试填写密码时出错 ({selector}): {e}")
            
            if not password_filled:
                logger.warning("未找到密码输入框，尝试使用键盘输入")
                try:
                    # 尝试使用按Tab键和输入的方式
                    await self.page.keyboard.press('Tab')
                    await self.page.keyboard.type(password)
                    password_filled = True
                except Exception as e:
                    logger.error(f"键盘输入密码失败: {e}")
            
            if not password_filled:
                logger.error("无法填写密码")
                return False
            
            # 检查是否有验证码
            captcha_selectors = ['input[name="kaptcha"]', 'input[placeholder="验证码"]', '#validateCode']
            captcha_input = None
            for selector in captcha_selectors:
                captcha_input = await self.page.query_selector(selector)
                if captcha_input:
                    logger.info(f"检测到验证码输入框: {selector}")
                    break
                
            if captcha_input:
                # 尝试获取验证码图像
                img_selectors = [
                    'img[alt="kaptcha"]', 
                    '.kaptcha-img', 
                    'img[src*="kaptcha"]', 
                    'img[alt="验证码"]',
                    'img[src*="validateCode"]',
                    'img[src*="captcha"]',
                    '.code-img'
                ]
                captcha_img = None
                for selector in img_selectors:
                    captcha_img = await self.page.query_selector(selector)
                    if captcha_img:
                        logger.info(f"找到验证码图片: {selector}")
                        break
                
                if captcha_img:
                    # 获取验证码图片并保存
                    captcha_path = "captcha.png"
                    await captcha_img.screenshot(path=captcha_path)
                    logger.info(f"已保存验证码图片到: {captcha_path}")
                    
                    # 使用OCR识别验证码
                    try:
                        import ddddocr
                        ocr = ddddocr.DdddOcr()
                        with open(captcha_path, "rb") as f:
                            captcha_text = ocr.classification(f.read())
                        logger.info(f"OCR识别验证码结果: {captcha_text}")
                        
                        # 清理可能的空格和非字母数字字符
                        captcha_text = ''.join(c for c in captcha_text if c.isalnum())
                        logger.info(f"清理后的验证码: {captcha_text}")
                        
                        # 填写验证码
                        await captcha_input.fill(captcha_text)
                        logger.info("已填写验证码")
                    except ImportError:
                        logger.error("无法导入ddddocr，请安装: pip install ddddocr")
                        # 等待用户手动输入验证码
                        print(f"\n请查看验证码图片({captcha_path})并在下方输入验证码:")
                        captcha_text = input("验证码: ").strip()
                        await captcha_input.fill(captcha_text)
                        logger.info("已使用手动输入的验证码")
                else:
                    logger.warning("未找到验证码图片")
            
            # 查找登录按钮并点击
            submit_selectors = [
                'input[type="submit"]', 
                'button[type="submit"]',
                'button:has-text("登录")',
                '.login-btn',
                '.ant-btn-primary',
                'button.ant-btn',
                'input[value="登录"]'
            ]
            
            submit_button = None
            for selector in submit_selectors:
                try:
                    submit_button = await self.page.query_selector(selector)
                    if submit_button:
                        logger.info(f"找到登录按钮: {selector}")
                        break
                except Exception as e:
                    logger.warning(f"查找登录按钮时出错 ({selector}): {e}")
                
            if submit_button:
                logger.info("点击登录按钮")
                # 记录当前URL，用于后续比较
                pre_login_url = self.page.url
                
                # 点击登录按钮
                await submit_button.click()
                
                # 等待页面变化或者响应
                try:
                    # 使用等待页面加载完成代替导航事件
                    await self.page.wait_for_load_state("networkidle", timeout=10000)
                    logger.info("页面加载状态变为networkidle")
                except Exception as e:
                    logger.warning(f"等待页面加载状态变化超时: {e}")
                
                # 等待一小段时间，确保页面有时间响应
                await asyncio.sleep(2)
                
                # 验证登录是否成功
                current_url = self.page.url
                logger.info(f"登录操作后页面URL: {current_url}")
                
                # 如果URL包含登录成功的标志
                if "login?ticket=" in current_url or "login?execution=" in current_url or "login/cas" in current_url:
                    # 这可能是CAS登录过程中的中间页面，再等待一下
                    logger.info("检测到CAS票据页面，等待最终跳转")
                    await asyncio.sleep(2)
                    current_url = self.page.url
                    logger.info(f"等待后的页面URL: {current_url}")
                
                # 成功标志：1. URL不再包含login 2. URL发生了变化
                if "login" not in current_url.lower() or pre_login_url != current_url:
                    page_title = await self.page.title()
                    logger.info(f"登录成功，当前页面标题: {page_title}, URL: {current_url}")
                    self.is_logged_in = True
                    return True
                else:
                    # 检查页面是否包含"登录成功"文本
                    try:
                        page_content = await self.extract_text_content()
                        success_indicators = ["登录成功", "登陆成功", "login success", "登录中央认证系统", "您已经成功登录"]
                        
                        if any(indicator in page_content for indicator in success_indicators):
                            logger.info(f"检测到登录成功页面内容，设置登录状态为成功")
                            self.is_logged_in = True
                            return True
                            
                        # 尝试查找登录成功的元素
                        success_selectors = ['.success-msg', '.login-success', 'div:contains("登录成功")', '.ant-message-success']
                        for selector in success_selectors:
                            try:
                                success_elem = await self.page.query_selector(selector)
                                if success_elem:
                                    success_text = await success_elem.text_content()
                                    if "成功" in success_text:
                                        logger.info(f"检测到登录成功元素: {success_text}")
                                        self.is_logged_in = True
                                        return True
                            except Exception:
                                pass
                    except Exception as e:
                        logger.warning(f"检查登录成功页面内容时出错: {e}")
                    
                    # 尝试查找登录失败消息
                    error_selectors = ['.login-error', '.ant-message-error', '.error-msg', '.alert-danger']
                    error_message = None
                    for selector in error_selectors:
                        try:
                            error_elem = await self.page.query_selector(selector)
                            if error_elem:
                                error_message = await error_elem.text_content()
                                logger.error(f"登录错误信息: {error_message}")
                                break
                        except Exception:
                            pass
                    
                    if error_message:
                        logger.error(f"登录失败，错误信息: {error_message}")
                    else:
                        logger.error(f"登录后仍然停留在登录页面，可能登录失败: {current_url}")
                    
                    return False
            else:
                logger.error("未找到登录按钮")
                # 尝试使用键盘直接回车提交
                try:
                    # 记录当前URL，用于后续比较
                    pre_login_url = self.page.url
                    
                    # 尝试按回车提交
                    await self.page.keyboard.press('Enter')
                    logger.info("使用回车键尝试提交表单")
                    
                    # 等待页面变化
                    await asyncio.sleep(2)
                    
                    # 检查URL是否变化
                    current_url = self.page.url
                    if pre_login_url != current_url or "login" not in current_url.lower():
                        logger.info(f"使用回车键登录成功，当前页面: {current_url}")
                        self.is_logged_in = True
                        return True
                    else:
                        logger.error("使用回车键登录失败")
                        return False
                except Exception as e:
                    logger.error(f"使用回车键提交表单失败: {e}")
                    return False
        except Exception as e:
            logger.error(f"登录过程出错: {str(e)}", exc_info=True)
            return False
    
    async def cleanup(self) -> None:
        """清理资源，但保留浏览器会话状态"""
        await self._cleanup_browser()
        logger.info("清理完成")

    async def count_elements(self, selector: str) -> int:
        """计算页面中匹配选择器的元素数量
        
        Args:
            selector: 元素选择器
            
        Returns:
            元素数量
        """
        try:
            if not self.page:
                logger.error("Page对象未初始化")
                return 0
                
            # 使用evaluateHandle获取元素数量
            count = await self.page.evaluate(f"document.querySelectorAll('{selector}').length")
            return count
        except Exception as e:
            logger.error(f"计算元素数量失败 ({selector}): {str(e)}")
            return 0

    async def store_user_data(self, key: str, value: Any) -> None:
        """存储用户数据
        
        Args:
            key: 数据键
            value: 数据值
        """
        self.user_data[key] = value
        
    async def get_user_data(self, key: str) -> Any:
        """获取用户数据
        
        Args:
            key: 数据键
            
        Returns:
            Any: 数据值
        """
        return self.user_data.get(key) 