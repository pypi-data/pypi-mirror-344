"""
自动化部署工具实现，封装浏览器自动化操作为高级部署流程
"""
from typing import Dict, Any, List, Annotated
import logging
import asyncio
import re
from pydantic import Field
from tools.base import BaseTool, tool_method
from core.utils import RequestTimer
from .service import PlaywrightService
import traceback
import re
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class PlaywrightTool(BaseTool):
    """系统部署工具
    
    提供少儿信息流的自动化部署功能
    """

    def __init__(self, config: Dict[str, Any]):
        """初始化工具类
        
        Args:
            config: 配置参数
        """
        super().__init__(config)
        self.service = PlaywrightService(config)
        self.username = config.get("username", "")
        self.password = config.get("password", "")
        
        if not self.username or not self.password:
            logger.warning("未配置用户名或密码，请在环境变量中设置DEPLOY_USERNAME和DEPLOY_PASSWORD")
        
        self.pending_submission = None
        self.last_created_page_id = None
        self.pending_column_submission = None
        
        # 添加表单会话和参数存储
        self.form_sessions = {}  # 存储表单会话
        
    async def initialize(self) -> None:
        """初始化服务（仅初始化数据结构，不启动浏览器）"""
        try:
            self.service = PlaywrightService(self.config)
            success = await self.service.initialize()
            if success:
                logger.info("浏览器自动化服务初始化成功")
            else:
                logger.error("浏览器自动化服务初始化失败")
                raise RuntimeError("浏览器自动化服务初始化失败")
        except Exception as e:
            logger.error(f"浏览器自动化服务初始化失败 {str(e)}", exc_info=True)
            raise
    
    async def cleanup(self) -> None:
        """清理资源"""            
        if self.service:
            await self.service.cleanup()
            
        self.service = None
        self.pending_submission = None
        self.last_created_page_id = None
        self.pending_column_submission = None
        logger.info("浏览器自动化服务资源已清理")

    @tool_method(description="填写信息流栏目表单")
    async def fill_column_form(
        self,
        page_id: Annotated[str, Field(description="信息流ID")],
        title: Annotated[str, Field(description="栏目标题")],
        description: Annotated[str, Field(description="栏目描述")],
        template_names: Annotated[List[str], Field(description="模板名称，例如ai绘本专用模板3")],
        publish_start_time: Annotated[str, Field(description="发布开始时间，格式: YYYY-MM-DD HH:mm:ss")],
        publish_end_time: Annotated[str, Field(description="发布结束时间，格式: YYYY-MM-DD HH:mm:ss")],
        hide_title: Annotated[bool, Field(description="是否隐藏标题")] = False,
        enable_sub: Annotated[bool, Field(description="二级栏目")] = False,
        img_title: Annotated[bool, Field(description="图片标题")] = False,
        is_recommend: Annotated[bool, Field(description="使用推荐算法")] = False,
        sort_number: Annotated[str, Field(description="栏目序号")] = "",
        is_top: Annotated[bool, Field(description="置顶")] = False,
    ) -> Dict[str, Any]:
        """填写信息流栏目表单，准备添加栏目

        NOTES:
            必填参数必须从对话中获取，不允许自动生成
        Args:
            page_id: 信息流ID
            title: 栏目标题
            description: 栏目描述
            template_names: 模板名称列表
            hide_title: 是否隐藏标题
            enable_sub: 二级栏目
            img_title: 图片标题
            is_recommend: 使用推荐算法
            sort_number: 栏目序号
            is_top: 置顶
            publish_start_time: 发布开始时间
            publish_end_time: 发布结束时间
            
        Returns:
            表单填写结果
        """
        

        with RequestTimer(f"fill_column_form - {title}"):
            try:
                if not self.service:
                    raise RuntimeError("浏览器自动化服务未初始化")
                
                # 确保浏览器已启动
                if not await self.service.ensure_browser():
                    return {
                        "success": False,
                        "message": "浏览器启动失败，无法填写表单",
                        "data": {}
                    }
                
                # 1. 如果提供了page_id，导航到对应的页
                if not page_id and self.last_created_page_id:
                    page_id = self.last_created_page_id
                    
                if not page_id:
                    return {
                        "success": False,
                        "message": "未提供信息流ID，无法添加栏",
                        "data": {}
                    }
                
                # 导航到信息流编辑页面
                column_url = f"https://idsaas-qcl.test.leiniao.com/page/cms-lite-launcher/#/page/addPage?id={page_id}"
                logger.info(f"导航到栏目编辑页 {column_url}")
                
                # 尝试导航，最多重
                success = False
                max_retries = 3
                
                for attempt in range(1, max_retries + 1):
                    try:
                        logger.info(f"导航尝试 {attempt}/{max_retries}")
                        success = await self.service.navigate_to(column_url)
                        if success:
                            break
                        # 如果页面提示需要登录，则先登录
                        if "登录" in await self.service.page.content():
                            logger.info("页面提示需要登录，先登录")
                            result = await self.login_to_system()
                            if result["success"]:
                                continue
                            else:
                                return {
                                    "success": False,
                                    "message": "登录失败，无法填写表",
                                    "data": {}
                                }
                        
                        # 再尝试一
                        success = await self.service.navigate_to(column_url)
                        if success:
                            break
                        
                    except Exception as e:
                        logger.error(f"导航尝试{attempt}出错: {str(e)}")
                        if attempt < max_retries:
                            await asyncio.sleep(2)
                
                if not success:
                    return {
                        "success": False,
                        "message": "导航到栏目编辑页面失败，已尝试多次",
                        "data": {}
                    }
                
                # 等待页面加载完成，确保已进入编辑页面
                await self.service.page.wait_for_selector('#title', state='visible')
                logger.info("页面加载完成，页面标题输入框可见")

                 # 如果当前页面有添加分众标签字段，直接认为调用失败，应该调用select_column_resource工具
                if "添加分众标签" in await self.service.page.content():
                    return {
                    "success": False,
                    "message": "当前页面有新增栏目字段，直接认为调用失败，应该调用select_column_resource工具",
                    "data": {}
                    }

                # 在信息流内容部署区域，点新增"按钮
                logger.info("点击新增按钮")
                await self.service.page.click('.ant-card:has-text("信息流内容部") button:has-text("新 增")')

                # 等待模态框出现
                logger.info("等待栏目表单模态框出现")
                await self.service.page.wait_for_selector('.ant-modal-content', state='visible', timeout=5000)
                await asyncio.sleep(1)  
                # 等待模态框完全展开
                
                # 操作模态框内的表单元素
                # 填写标题
                if title:
                    logger.info(f"填写栏目标题: {title}")
                    await self.service.page.fill('.ant-modal-content #title', title)
                
                # 填写描述
                if description:
                    logger.info(f"填写栏目描述: {description}")
                    await self.service.page.fill('.ant-modal-content #desc', description)
                
                # 设置栏目序号
                if sort_number:
                    logger.info(f"设置栏目序号: {sort_number}")
                    await self.service.page.fill('.ant-modal-content #sort', sort_number)
                
                
                # 设置模板
                if template_names and len(template_names) > 0:
                    for template_name in template_names:
                        logger.info(f"选择模板: {template_name}")
                        # 点击模板选择
                        await self.service.page.click('.ant-modal-content #templateIds')
                        # 等待下拉列表
                        await self.service.page.wait_for_selector('.ant-select-dropdown', state='visible', timeout=3000)
                        # 选择模板
                        template_option = f'.ant-select-dropdown .ant-select-item-option:has-text("{template_name}")'
                        template_exists = await self.service.page.wait_for_selector(template_option, state='visible', timeout=3000)
                        if template_exists:
                            await self.service.page.click(template_option)
                            logger.info(f"已选择模板: {template_name}")
                        else:
                            logger.warning(f"未找到模板 {template_name}")
                
                # 等待短暂时间，确保模板选择操作完成
                await asyncio.sleep(0.5)

                # 如果模板下拉列表仍然可见，点击空白处关闭
                if self.service.page.query_selector('.ant-select-selector'):
                    logger.info("点击空白处关闭模板下拉列表")
                    await self.service.page.click('body')

                 # 若未设置发布时间，则设置为当前时间
                if not publish_start_time:
                    publish_start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                if not publish_end_time:
                    publish_end_time = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d %H:%M:%S")

                # 设置发布时间
                if publish_start_time and publish_end_time:
                    logger.info(f"设置发布时间: {publish_start_time} - {publish_end_time}")
                    # 使用专用的日期范围设置方法
                    await self._set_date_range('.ant-modal-content #publishTime', publish_start_time, publish_end_time)

                # 设置隐藏标题 - 恢复表单设置
                if hide_title:
                    logger.info("设置隐藏标题")
                    await self.service.page.click('.ant-modal-content #titleVisible')
                
                # 设置二级栏目
                if enable_sub:
                    logger.info("设置二级栏目")
                    await self.service.page.click('.ant-modal-content #enableSub')
                
                # 设置图片标题
                if img_title:
                    logger.info("设置图片标题")
                    await self.service.page.click('.ant-modal-content #imgTitle')
                
                # 设置使用推荐算法
                if is_recommend:
                    logger.info("设置使用推荐算法")
                    await self.service.page.click('.ant-modal-content #isRecommend')
                
                # 设置置顶
                if is_top:
                    logger.info("设置置顶")
                    await self.service.page.click('.ant-modal-content #isTop')
                
                # 构建并返回结果，并提示下一步调用select_column_resource工具选择资源
                result = {
                    "success": True,
                    "message": "信息流栏目配置填写完成，接下来请选择栏目资源",
                    "next_tool": "select_column_resource",
                    "data": {
                        "page_id": page_id,
                        "title": title,
                        "description": description,
                        "sort_number": sort_number,
                        "publish_start_time": publish_start_time,
                        "publish_end_time": publish_end_time,
                        "template_names": template_names,
                        "hide_title": hide_title,
                        "enable_sub": enable_sub,
                        "img_title": img_title,
                        "is_recommend": is_recommend,
                        "is_top": is_top
                    }
                }
                
                return result
                
            except Exception as e:
                logger.error(f"填写信息流栏目表单失败 {e}")
                traceback.print_exc()
                return {
                    "status": "error", 
                    "message": f"填写信息流栏目表单失败: {str(e)}",
                    "error": traceback.format_exc()
                }
           
    @tool_method(description="保存栏目")
    async def confirm_column_submission(
        self,
        save_type: Annotated[str, Field(description="保存类型")]
    ) -> Dict[str, Any]:
        """保存栏目
        Args:
            save_type: 保存类型，保存
            
        Returns:
            提交结果
        """
        with RequestTimer("confirm_column_submission"):
            try:
                if not self.service:
                    raise RuntimeError("浏览器自动化服务未初始化")
                
                # 确保浏览器已启动
                if not await self.service.ensure_browser():
                    return {
                        "success": False,
                        "message": "浏览器启动失败，无法确认提交栏目",
                        "data": {}
                    }
                
                # 根据用户选择的保存类型点击对应按钮
                button_text = "保 存"
                save_button_selector = f'.ant-modal-footer button.ant-btn-primary:has-text("{button_text}")'
                
                await self.service.click_element(save_button_selector)

                # 等待3秒
                await asyncio.sleep(3)

                # 页面url包含addPage，即认为成功
                # 获取当前页面url
                current_url = self.service.page.url
                if "addPage" in current_url:
                    save_success = True
                else:
                    save_success = False
                
                if save_success:
                    column_data = self.pending_column_submission
                    # 清空待提交状态
                    self.pending_column_submission = None
                    
                    return {
                        "success": True,
                        "message": f"栏目 '{column_data['title']}' {save_type}成功",
                        "data": column_data
                    }
                else:
                    return {
                        "success": False,
                        "message": f"{save_type}栏目后未收到成功提示",
                        "data": {}
                    }
                
            except Exception as e:
                logger.error(f"确认提交栏目失败: {str(e)}", exc_info=True)
                return {
                    "success": False,
                    "message": f"确认提交栏目失败: {str(e)}",
                }
      
    async def _set_date_range(self, selector: str, start_datetime: str, end_datetime: str) -> None:
        """设置日期范围选择器的值
        
        Args:
            selector: 日期范围选择器
            start_datetime: 开始日期时间值，格式：YYYY-MM-DD HH:mm:ss
            end_datetime: 结束日期时间值，格式：YYYY-MM-DD HH:mm:ss
        """
        try:
            logger.info(f"设置日期范围: {start_datetime} - {end_datetime}")
            
            # 点击日期范围选择器，打开日期选择面板
            await self.service.page.click(selector)
            await asyncio.sleep(0.5)  # 等待日期选择面板显示
            
            # 设置开始时间
            await self.service.page.fill('.ant-picker-input-active input', start_datetime)
            await asyncio.sleep(0.5)
            
            # 点击确定按钮完成开始时间选择
            confirm_button = '.ant-btn-primary:has-text("确 定")'
            await self.service.page.click(confirm_button)
            logger.info("已点击日期选择器的确定按钮，完成开始时间选择")
            await asyncio.sleep(0.5)
            
            # 此时会自动跳转到结束时间选择
            # 设置结束时间
            await self.service.page.fill('.ant-picker-input-active input', end_datetime)
            await asyncio.sleep(0.5)
            
            # 再次点击确定按钮完成整个日期范围选择
            await self.service.page.click(confirm_button)
            logger.info("已点击日期选择器的确定按钮，完成结束时间选择")
            await asyncio.sleep(0.5)
            
            # 如果日期选择器仍然可见，点击空白处关闭
            try:
                date_picker_visible = await self.service.page.query_selector('.ant-picker-dropdown:visible')
                if date_picker_visible:
                    await self.service.page.click('body', position={"x": 10, "y": 10})
            except Exception as e:
                logger.warning(f"尝试关闭日期选择器时出错: {str(e)}")
                
            logger.info(f"已设置日期范围 {selector}: {start_datetime} - {end_datetime}")
        except Exception as e:
            logger.error(f"设置日期范围失败 {selector}: {e}")
            # 尝试点击页面其他位置关闭日期选择面板
            try:
                await self.service.page.click("body", position={"x": 0, "y": 0})
            except:
                pass
            
    @tool_method(description="登录到系统")
    async def login_to_system(
        self
    ) -> Dict[str, Any]:
        """执行单独的登录操作，登录到系统        
        Returns:
            登录结果
        """
        try:
            # 检查是否已初始化            
            if not hasattr(self, 'service') or not self.service:
                logger.error("服务未初始化，请先调用initialize方法")
                await self.initialize()

            # 检查是否已登录
            if self.service.is_logged_in:
                logger.info("已登录，跳过登录操作")
                return {
                    "success": True,
                    "message": "已登录，跳过登录操作",
                }
            
            # 检查用户名和密码            
            if not self.username or not self.password:
                return {
                    "success": False,
                    "message": "未配置用户名或密码，请在环境变量中设置DEPLOY_USERNAME和DEPLOY_PASSWORD",
                    "data": {
                        "username": bool(self.username),
                        "password": bool(self.password)
                    }
                }
            
            logger.info("开始启动浏览器...")
            # 设置浏览器为可见模式
            self.service.headless = False
            
            # 确保浏览器已启动
            browser_started = False
            max_browser_retries = 3
            
            for attempt in range(max_browser_retries):
                try:
                    logger.info(f"{attempt + 1} 次尝试启动浏览器")
                    browser_started = await self.service.ensure_browser()
                    if browser_started:
                        logger.info("浏览器启动成功")
                        break
                    else:
                        logger.warning(f"{attempt + 1} 次启动浏览器失败，准备重试")
                        await asyncio.sleep(2)
                except Exception as e:
                    logger.error(f"{attempt + 1} 次启动浏览器出错: {str(e)}")
                    if attempt < max_browser_retries - 1:
                        await asyncio.sleep(2)
                    else:
                        return {
                            "success": False,
                            "message": f"多次尝试启动浏览器均失败: {str(e)}",
                            "data": {"error": str(e)}
                        }
            
            if not browser_started:
                return {
                    "success": False,
                    "message": "浏览器启动失败，请检查系统环境",
                    "data": {}
                }
            
            # 直接导航到登录页            
            login_url = "https://sso.tclking.com/cas/login"
            logger.info(f"导航到登录页 {login_url}")
            
            # 尝试导航到登录页            
            max_retries = 3
            success = False
            
            for attempt in range(1, max_retries + 1):
                try:
                    logger.info(f"导航到登录页面尝试 {attempt}/{max_retries}")
                    await self.service.page.goto(login_url, wait_until='networkidle')
                    success = True
                    break
                except Exception as e:
                    logger.error(f"导航到登录页面尝试 {attempt} 失败: {e}")
                    
                    if attempt < max_retries:
                        logger.info("等待2秒后重试")
                        await asyncio.sleep(2)
                        # 如果浏览器可能已关闭，尝试重新启动
                        await self.service.ensure_browser()
            
            if not success:
                return {
                    "success": False,
                    "message": "无法导航到登录页面，请检查网络连接",
                    "data": {}
                }
            
            # 执行登录
            login_success = await self.service.login()
            
            if login_success:
                # 检查当前URL，确认登录是否成功
                current_url = self.service.page.url
                page_content = await self.service.extract_text_content()
                page_title = await self.service.page.title()
                
                # 登录成功的文本指示器
                success_indicators = ["登录成功", "登陆成功", "login success", "登录中央认证系统", "您已经成功登录"]
                has_success_text = any(indicator in page_content for indicator in success_indicators)
                
                # 即使URL仍包含login，但如果页面内容包含成功提示，也认为登录成功
                if "login" in current_url.lower() and not has_success_text:
                    # 如果还在登录页面，且没有成功提示，可能登录失败
                    return {
                        "success": False,
                        "message": f"登录可能失败，仍然位于登录相关页面且没有成功提示: {current_url}",
                        "data": {"current_url": current_url}
                    }
                
                # 记录登录状态
                self.service.is_logged_in = True
                
                # 记录成功指示
                success_message = "登录成功"
                if has_success_text:
                    success_message = f"登录成功，页面显示成功提示: {page_title}"
                
                return {
                    "success": True,
                    "message": success_message,
                    "data": {
                        "current_url": current_url,
                        "page_title": page_title,
                        "has_success_text": has_success_text
                    }
                }
            else:
                return {
                    "success": False,
                    "message": "登录失败，请检查用户名和密码",
                    "data": {
                        "username_provided": bool(self.username),
                        "password_provided": bool(self.password)
                    }
                }
        except Exception as e:
            logger.error(f"登录过程出错: {str(e)}", exc_info=True)
            return {
                "success": False,
                "message": f"登录过程出错: {str(e)}",
                "data": {
                    "error": str(e),
                    "traceback": traceback.format_exc()
                }
            }

    #@tool_method(description="登录后导航到指定页面")
    async def navigate_after_login(
        self,
        module: Annotated[str, Field(description="模块名称，例如新增信息流 新增栏目 查询信息流列表")] = "新增信息流"
    ) -> Dict[str, Any]:
        """登录成功后导航到指定页面
        
        Args:
            target_url: 目标URL，默认为信息流页面地址
            
        Returns:
            导航结果
        """
        
        # 新增/添加信息流模式
        if re.search(r'(新增|添加).*?(信息流|页面)', module):
            target_url = "https://idsaas-qcl.test.leiniao.com/page/cms-lite-launcher/#/page/addPage"
        # 新增/添加栏目模式
        elif re.search(r'(新增|添加).*?(栏目)', module):
            target_url = "https://idsaas-qcl.test.leiniao.com/page/cms-lite-launcher/#/column/addColumn"
        # 查询/查看信息流列表
        elif re.search(r'(查询|查看|浏览).*?(信息流|列表)', module):
            target_url = "https://idsaas-qcl.test.leiniao.com/page/cms-lite-launcher/#/page/list"
        else:
            logger.warning(f"未能识别的模块名 {module}，默认导航到新增信息流页面")
            target_url = "https://idsaas-qcl.test.leiniao.com/page/cms-lite-launcher/#/page/addPage"
        
        try:
            if not self.service:
                raise RuntimeError("浏览器自动化服务未初始化")
        
            # 确保浏览器已启动
            if not await self.service.ensure_browser():
                return {
                    "success": False,
                    "message": "浏览器启动失败，无法执行导航",
                    "data": {}
                }
            
            # 检查是否已登录
            if not self.service.is_logged_in:
                return {
                    "success": False,
                    "message": "您尚未登录，请先调用login_to_system方法进行登录",
                    "data": {
                        "hint": "在继续操作前，请先执行login_to_system方法完成登录"
                    }
                }
            
            # 尝试导航到目标页面            logger.info(f"登录后导航到目标页面: {target_url}")
            
            # 尝试导航，最多重            success = False
            max_retries = 3
            
            for attempt in range(1, max_retries + 1):
                try:
                    logger.info(f"导航尝试 {attempt}/{max_retries}")
                    # 记录当前URL
                    pre_nav_url = self.service.page.url
                    # 执行导航
                    await self.service.page.goto(target_url, wait_until='domcontentloaded')
                    
                    # 等待网络空闲
                    try:
                        await self.service.page.wait_for_load_state("networkidle", timeout=10000)
                        logger.info("页面加载状态变为networkidle")
                    except Exception as e:
                        logger.warning(f"等待页面加载状态变化超时: {e}")
                    
                    # 等待一小段时间，确保页面响应
                    await asyncio.sleep(2)
                    
                    # 获取当前URL
                    current_url = self.service.page.url
                    logger.info(f"导航后的页面URL: {current_url}")
                    
                    # 检查导航是否成功（URL变化或包含目标路径部分）
                    if pre_nav_url != current_url or any(path_part in current_url for path_part in ['/page/addPage', '/columnDetail']):
                        page_title = await self.service.page.title()
                        success = True
                        logger.info(f"导航成功，当前页面标题: {page_title}")
                        break
                    
                    # 检查是否又回到了登录页                    if "login" in current_url.lower() or "sso" in current_url.lower():
                        # 重置登录状态                        self.service.is_logged_in = False
                        logger.warning("导航过程中检测到登录状态失效")
                        return {
                            "success": False,
                            "message": "导航过程中登录状态失效，请重新登录",
                            "data": {
                                "current_url": current_url
                            }
                        }
                    
                    # 如果没有明显失败但URL没有预期变化，再等待一下，可能是单页应用正在加载
                    await asyncio.sleep(3)
                    
                    # 检查页面上是否有预期的元素
                    expected_selectors = ['form', '.ant-card', '.ant-table', '#title']
                    for selector in expected_selectors:
                        element = await self.service.page.query_selector(selector)
                        if element:
                            logger.info(f"找到目标页面元素: {selector}")
                            success = True
                            break
                    
                    if success:
                        break
                    
                    # 如果失败且不是最后一次尝试，等待一下再重试
                    if attempt < max_retries:
                        logger.warning(f"导航尝试{attempt}未得到预期结果，等待2秒后重试")
                        await asyncio.sleep(2)
                except Exception as e:
                    logger.error(f"导航尝试{attempt}出错: {str(e)}")
                    if attempt < max_retries:
                        await asyncio.sleep(2)
            
            # 导航结果
            if success:
                # 获取页面信息
                page_title = await self.service.page.title()
                current_url = self.service.page.url
                
                return {
                    "success": True,
                    "message": "导航成功",
                    "data": {
                        "page_title": page_title,
                        "current_url": current_url
                    }
                }
            else:
                # 获取当前状态                current_url = self.service.page.url
                
                return {
                    "success": False,
                    "message": "导航未获得预期结果，请检查页面状态",
                    "data": {
                        "current_url": current_url
                    }
                }
        except Exception as e:
            logger.error(f"导航过程出错: {str(e)}", exc_info=True)
            return {
                "success": False,
                "message": f"导航过程出错: {str(e)}",
                "data": {}
            }

    @tool_method(description="创建信息流")
    async def create_information_flow(
        self, 
        title: Annotated[str, Field(description="信息流标题")],
        channel_id: Annotated[str, Field(description="频道, 必须 可选值有 少儿 教育 健身 电影 广场")],
        terminal_type: Annotated[str, Field(description="下发渠道, 必须 可选值有 TCL 三星 绘本APK 少儿小程序")] = "TCL",
        description: Annotated[str, Field(description="页面描述")] = "",
        fee_type: Annotated[str, Field(description="付费类型")] = "",
        height: Annotated[str, Field(description="配置栏目高度")] = "100%",
        preview_style: Annotated[str, Field(description="预览样式")] = "无预览"
    ) -> Dict[str, Any]:
        """创建一个新的信息流表单，填写完成后返回预览信息
        
        Args:
            title: 信息流标题
            channel_id: 频道, 必须 可选值有 少儿 教育 健身 电影 广场
            terminal_type: 下发渠道, 必须 可选值有 TCL 三星 绘本APK 少儿小程序
            description: 页面描述
            fee_type: 付费类型
            height: 配置栏目高度
            preview_style: 预览样式
        Returns:
            Dict: 包含表单填写结果和预览信息
        """
        try:
            logger.info(f"开始创建信息流: 标题={title}, 频道={channel_id}, 下发渠道={terminal_type}")
            
            # 确保浏览器已启动
            if not self.service:
                return {
                    "success": False,
                    "message": "浏览器自动化服务未初始化，请先调用initialize方法",
                    "data": {}
                }
            
            # 确保浏览器已启动
            await self.service.ensure_browser()
            
            
            # 检查页面标题并验证是否为添加页面
            page_title = await self.service.page.title()
            current_url = self.service.page.url
            
            if "addPage" not in current_url and "page/add" not in current_url:
                logger.warning(f"当前页面可能不是添加页面: {current_url}, 标题: {page_title}")
                
                # 如果不在添加页面，尝试导航到添加页面
                add_page_url = "https://idsaas-qcl.test.leiniao.com/page/cms-lite-launcher/#/page/addPage"
                await self.service.navigate_to(add_page_url)
                await asyncio.sleep(2)  # 等待页面加载
            
            # 如果页面提示需要登录，则先登录
            if "登录" in await self.service.page.content():
                logger.info("页面提示需要登录，先登录")
                result = await self.login_to_system()
                if not result["success"]:
                    return {
                        "success": False,
                        "message": "登录失败，无法填写表",
                        "data": {}
                    }
                        
            # 再尝试一次
            success = await self.service.navigate_to(add_page_url)
            
            # 等待表单元素加载
            await self.service.wait_for_selector("#title", timeout=10000)
            
            # 填写表单
            form_data = {}
            
            # 填写标题
            await self.service.fill_form("#title", title)
            form_data["title"] = title
            
            # 填写描述
            if description:
                await self.service.fill_form("#desc", description)
                form_data["description"] = description
            
            # 填写下拉选择            
            select_fields = [
                {"id": "channelId", "value": channel_id},
                {"id": "height", "value": height},
                {"id": "terminalType", "value": terminal_type},
                {"id": "previewStyle", "value": preview_style}
            ]
            
            # 只有在提供了付费类型时才填写
            if fee_type:
                select_fields.append({"id": "feeType", "value": fee_type})
            
            # 使用改进的下拉选择方法填写表单
            for field in select_fields:
                if field["value"]:  # 只处理有值的字段
                    success = await self._fill_select(field["id"], field["value"])
                    if success:
                        form_data[field["id"]] = field["value"]
                        logger.info(f"成功设置 {field['id']} = {field['value']}")
                    else:
                        logger.error(f"设置 {field['id']} = {field['value']} 失败")
            
            # 保存待提交的表单数据
            self.pending_submission = form_data
            
           
            # 构建确认信息
            confirmation_message = f"信息流表单已创建成功，表单内容如下：\n" \
                      f"- 标题: {title}\n" \
                      f"- 频道: {channel_id}\n" \
                      f"- 下发渠道: {terminal_type}\n" \
                      f"- 页面描述: {description}\n" \
                      f"- 付费类型: {fee_type}\n" \
                      f"- 栏目高度: {height}\n" \
                      f"- 预览样式: {preview_style}\n"
                      
            if description:
                confirmation_message += f"\n- 描述: {description}"
            if fee_type:
                confirmation_message += f"\n- 付费类型: {fee_type}"
                
            confirmation_message += "\n\n请确认需要新增信息流的内容，如果您不满足当前内容可以选择继续修改。如果你觉得不需要修改，可以回复 保存或保存并发布 来操作保存这个信息流表单"
            
            return {
                "success": True,
                "message": confirmation_message,
                "data": {
                    "form_data": form_data
                }
            }
        except Exception as e:
            logger.error(f"创建信息流表单失败 {str(e)}", exc_info=True)
            return {
                "success": False,
                "message": f"创建信息流表单失败: {str(e)}",
            }

    async def _fill_select(self, select_id: str, option_text: str) -> bool:
        """填写下拉选择        
        Args:
            select_id: 下拉框的ID
            option_text: 要选择的选项文本
            
        Returns:
            bool: 操作是否成功
        """
        try:
            # 构建选择器，使用更精确的选择            
            selector = f"#{select_id} + .ant-select-selection-search-input, #{select_id}"
            
            # 首先尝试确保元素可见并滚动到视图
            await self.service.page.wait_for_selector(selector, state='visible', timeout=5000)
            try:
                element = await self.service.page.query_selector(selector)
                if element:
                    # 先滚动到元素位置，减少页面跳动
                    await element.scroll_into_view_if_needed()
                    await asyncio.sleep(0.5)
            except Exception as e:
                logger.warning(f"滚动到元素位置失败: {e}")
            
            # 等待一下，确保页面稳定
            await asyncio.sleep(0.5)
            
            # 使用强制点击策略，避免被其他元素遮挡
            try:
                # 查找下拉框所在的父元素，使用更可靠的方式点击
                container_selector = f".ant-select:has(#{select_id})"
                await self.service.page.click(container_selector, force=True)
            except Exception as e:
                logger.warning(f"使用选择{container_selector} 点击失败: {e}")
                # 回退到直接点击原始元素
                await self.service.page.click(selector, force=True)
            
            # 等待下拉选项出现
            dropdown_selector = ".ant-select-dropdown:not(.ant-select-dropdown-hidden)"
            await self.service.page.wait_for_selector(dropdown_selector, state='visible', timeout=5000)
            
            # 给足够时间让下拉菜单完全展开
            await asyncio.sleep(1)
            
            # 查找并点击指定选项（使用更精确的匹配方式）
            option_selector = f'.ant-select-item-option-content:text-is("{option_text}")'
            try:
                await self.service.page.click(option_selector, timeout=5000)
            except Exception as e:
                logger.warning(f"精确匹配选项失败: {e}, 尝试模糊匹配")
                # 使用模糊匹配
                option_selector = f'.ant-select-item-option-content:has-text("{option_text}")'
                await self.service.page.click(option_selector, timeout=5000)
            
            # 等待下拉菜单关闭
            await asyncio.sleep(0.5)
            
            logger.info(f"已选择 {select_id}: {option_text}")
            return True
        except Exception as e:
            logger.error(f"选择下拉选项失败 {select_id}: {e}")
            # 尝试关闭可能仍打开的下拉菜单
            try:
                await self.service.page.keyboard.press("Escape")
            except:
                pass
            return False

    @tool_method(description="保存信息流")
    async def submit_information_flow(
        self, 
        action: Annotated[str, Field(description="提交动作")]
    ) -> Dict[str, Any]:
        """提交已经填写完成的信息流表单，可以选择 保存
        Args:
            action: 提交动作
            
        Returns:
            Dict: 提交结果，包含是否成功、信息流ID等信        """
        try:

            # 如果页面有新增栏目 字样，表示当前页面是新增栏目页面，需要先保存栏目
            if "新增栏目" in await self.service.page.content():
                logger.info("当前页面是新增栏目页面，需要先保存栏目")
                return {
                    "status": "failed",
                    "message": "当前页面是新增栏目页面，需要先保存栏目",
                    "data": None
                }
            # 验证action参数
            valid_actions = ["保存", "保存并发"]
            if action not in valid_actions:
                return {
                    "status": "failed",
                    "message": f"无效的动作 {action}，可选 {', '.join(valid_actions)}",
                    "data": None
                }
            
            # 根据操作类型选择对应的按钮文本
            button_text = "保存并发布" if action == "保存并发布" else "保 存"
            
            # 使用精确的选择器，优先在卡片额外区域查找按钮
            success = False
            
            # 1. 尝试通过文本内容直接找到按钮
            selector = f"button:has-text(\"{button_text}\")"
            if await self.service.page.query_selector(selector):
                await self.service.page.click(selector)
                success = True
                logger.info(f"已点击{button_text}按钮")
            
            # 2. 如果上面失败，尝试在卡片额外区域中查找按钮
            if not success:
                selector = f".ant-card-extra button:has-text(\"{button_text}\")"
                if await self.service.page.query_selector(selector):
                    await self.service.page.click(selector)
                    success = True
                    logger.info(f"已在卡片额外区域点击'{button_text}'按钮")
            
            # 3. 如果前两种方法都失败，根据位置查找按钮
            if not success:
                if action == "保存":
                    selector = ".ant-card-extra button.ant-btn-primary:nth-child(2)"
                else:
                    selector = ".ant-card-extra button.ant-btn-primary:nth-child(3)"
                
                if await self.service.page.query_selector(selector):
                    await self.service.page.click(selector)
                    success = True
                    logger.info(f"已通过位置点击'{action}'按钮")
            
            if not success:
                logger.warning(f"所有方法都未能找到'{action}'按钮")
            
            # 等待结果提示出现
            success_message_selector = ".ant-message-success, .ant-message-notice"
            error_message_selector = ".ant-message-error"
            
            # 等待操作结果
            try:
                # 尝试等待成功消息
                await self.service.wait_for_selector(success_message_selector, timeout=10000)
                logger.info("检测到成功提示")
                success = True
                result_message = "操作成功完成"
            except Exception as wait_error:
                # 检查是否有错误消息
                try:
                    await self.service.wait_for_selector(error_message_selector, visible=True, timeout=2000)
                    error_text = await self.service.get_text(error_message_selector)
                    logger.error(f"检测到错误提示: {error_text}")
                    return {
                        "status": "failed",
                        "message": f"提交失败: {error_text}",
                        "data": None
                    }
                except:
                    # 如果两种消息都没有，可能是其他问题
                    logger.error(f"等待操作结果超时: {str(wait_error)}")
                    return {
                        "status": "failed",
                        "message": "提交后等待结果超时，无法确定是否成功",
                        "data": None
                    }
            
            

            
            
            return {
                "status": "success",
                "message": f"表单已成功{action}",
                "data": {
                    "action": action
                }
            }
        except Exception as e:
            logger.error(f"提交表单失败: {str(e)}", exc_info=True)
            return {
                "status": "failed",
                "message": f"提交表单失败: {str(e)}",
            }

    @tool_method(description="选择栏目资源 填充完栏目配置后，调用此工具选择栏目资源，调用此工具时，必须由用户提供频道类型、资源类型、搜索关键字、搜索关键字信息和需要的资源数量")
    async def select_column_resource(
        self,
        resource_channel: Annotated[str, Field(description="频道类型 由用户输入提供 可选值:少儿 教育 健身 老年 戏曲 广场舞")],
        resource_media_type: Annotated[str, Field(description="媒资形式，可选值:视频 音频 爱奇艺SDK 优酷SDK")],
        keyword: Annotated[str, Field(description="搜索关键字可选条件 片名 导演 演员 视频ID")],
        keyword_info: Annotated[str, Field(description="对应具体的片名、导演、演员或视频ID值")],
        resource_module: Annotated[str, Field(description="资源类型，可选值:媒资专辑 专题 频道页")] = "媒资专辑",
        resource_number: Annotated[int, Field(description="需要的资源数量")] = 10
    ) -> Dict[str, Any]:
        """选择栏目资源
        
        Args:
            resource_channel: 频道类型 可选值:少儿 教育 健身 老年 戏曲 广场舞
            resource_media_type: 媒资形式，可选值:视频 音频 爱奇艺SDK 优酷SDK
            keyword: 搜索关键字可选条件 片名 导演 演员 视频ID
            keyword_info: 对应具体的片名、导演、演员或视频ID值
            resource_module: 资源类型，可选值:媒资专辑 专题 频道页
            resource_number: 需要的资源数量
            
        Returns:
            资源选择结果
        """
        try:
            # 参数打印
            logger.info(f"频道类型: {resource_channel}, 资源类型: {resource_module}, 媒资形式: {resource_media_type}, 关键字: {keyword}, 关键字信息: {keyword_info}")

            # 资源选择部分处理
            logger.info("准备处理资源选择")
            
            # 1. 检查是否已经出现资源选择模态框
            resource_modal_selector = '.ant-modal-title:has-text("添加资源")'
            resource_modal_exists = await self.service.page.query_selector(resource_modal_selector)
            
            # 如果模态框还没有出现，需要双击合适的资源格
            if not resource_modal_exists:
                # 获取所有模板格子及其状态
                template_cells_info = await self.service.page.evaluate('''
                () => {
                    const cells = document.querySelectorAll('.templateCol___');
                    return Array.from(cells).map((cell, index) => {
                        // 多种判断方法组合使用
                        const hasFilled = 
                            // 1. 检查是否有filled类或包含bgImg类的元素
                            cell.className.includes('filled') ||
                            cell.querySelector('.bgImg___11RLL') !== null ||
                            // 2. 检查是否有内容元素
                            cell.querySelector('.itemContent___-:not(:empty)') !== null ||
                            // 3. 检查是否有img标签
                            cell.querySelector('img') !== null;
                        
                        return {
                            index: index,
                            hasFilled: hasFilled
                        };
                    });
                }
                ''')
                
                logger.info(f"模板格子状态: {template_cells_info}")
                
                # 找到第一个未填充的资源格
                empty_cell_index = -1
                for cell in template_cells_info:
                    if not cell.get('hasFilled', True):
                        empty_cell_index = cell.get('index')
                        break
                
                if empty_cell_index >= 0:
                    logger.info(f"找到未填充的资源格，索引: {empty_cell_index}")
                    
                    # 直接使用Playwright API双击
                    cells = await self.service.page.query_selector_all('.templateCol___2qDPl')
                    if empty_cell_index < len(cells):
                        cell = cells[empty_cell_index]
                        # 再次确认没有img元素
                        has_image = await cell.query_selector('img')
                        if not has_image:
                            # 确保元素可见
                            await cell.scroll_into_view_if_needed()
                            # 双击元素
                            await cell.dblclick()
                            logger.info(f"已使用Playwright API双击索引为 {empty_cell_index} 的未填充资源格")
                            await asyncio.sleep(1)
                else:
                    logger.warning("未找到未填充的资源格，尝试从左往右依次检查和双击")
                    
                    # 从左到右尝试双击每个资源格，通过检查是否有img元素来判断
                    cells = await self.service.page.query_selector_all('.templateCol___2qDPl')
                    for i, cell in enumerate(cells):
                        try:
                            # 检查是否已有资源填充
                            has_image = await cell.query_selector('img')
                            has_bg_img = await cell.query_selector('.bgImg___11RLL')
                            
                            if not has_image and not has_bg_img:
                                logger.info(f"尝试双击第 {i+1} 个未填充的资源格")
                                await cell.scroll_into_view_if_needed()
                                await cell.dblclick()
                                await asyncio.sleep(0.5)
                                
                                # 检查是否出现添加资源模态框
                                resource_modal = await self.service.page.query_selector('.ant-modal-title:has-text("添加资源")')
                                if resource_modal:
                                    logger.info(f"双击第 {i+1} 个资源格成功，已出现添加资源模态框")
                                    break
                        except Exception as e:
                            logger.warning(f"检查或双击第 {i+1} 个资源格失败: {str(e)}")
            
            # 再次检查是否已经出现资源选择模态框
            resource_modal_exists = await self.service.page.query_selector(resource_modal_selector)
            if not resource_modal_exists:
                logger.warning("尝试多种方式后仍未能打开资源选择模态框")
                return {
                    "success": False,
                    "message": "模板框已填满，可以进行保存栏目",
                    "data": {}
                }
            
            logger.info("资源选择模态框已打开，开始设置搜索条件")
            
            # 2. 设置资源类型 (媒资专辑/专题/频道页)
            if resource_module:
                logger.info(f"设置资源类型: {resource_module}")
                if resource_module == "视频" or resource_module == "媒资专辑" or resource_module == "video":
                    await self.service.page.click('.ant-modal-content:has(.ant-modal-title:has-text("添加资源")) label:has-text("媒资专辑")')
                elif resource_module == "topic" or resource_module == "专题":
                    await self.service.page.click('.ant-modal-content:has(.ant-modal-title:has-text("添加资源")) label:has-text("专题")')
                elif resource_module == "channel_page" or resource_module == "频道页":
                    await self.service.page.click('.ant-modal-content:has(.ant-modal-title:has-text("添加资源")) label:has-text("频道页")')
            
            # 3. 设置频道类型
            if resource_channel:
                try:
                    logger.info(f"设置频道类型: {resource_channel}")
                    # 在资源模态框内点击频道类型下拉
                    await self.service.page.click('.ant-modal-content:has(.ant-modal-title:has-text("添加资源")) #channelId, .ant-modal-content:has(.ant-modal-title:has-text("添加资源")) .ant-select:has(#channelId)')
                    await asyncio.sleep(0.5)
                    
                    # 选择下拉选项 (直接点击资源类型的选项)
                    channel_option = f'.ant-select-dropdown .ant-select-item-option-content:has-text("{resource_channel}")'
                    await self.service.page.click(channel_option, timeout=3000)
                    logger.info(f"已选择频道类型: {resource_channel}")
                except Exception as e:
                    logger.warning(f"设置频道类型失败: {str(e)}")
            
            # 4. 如果需要设置媒资形式
            if resource_media_type and resource_media_type != "视频":  # 默认已经是"视频"
                try:
                    logger.info(f"设置媒资形式: {resource_media_type}")
                    # 在资源模态框内点击媒资形式下拉
                    await self.service.page.click('.ant-modal-content:has(.ant-modal-title:has-text("添加资源")) #mediaType, .ant-modal-content:has(.ant-modal-title:has-text("添加资源")) .ant-select:has(#mediaType)')
                    await asyncio.sleep(0.5)
                    
                    # 选择下拉选项
                    media_option = f'.ant-select-dropdown .ant-select-item-option-content:has-text("{resource_media_type}")'
                    await self.service.page.click(media_option, timeout=3000)
                    logger.info(f"已选择媒资形式: {resource_media_type}")
                except Exception as e:
                    logger.warning(f"设置媒资形式失败: {str(e)}")
            
            # 5. 设置关键字搜索
            if keyword and keyword_info:
                try:
                    logger.info(f"设置关键字搜索类型: {keyword}, 关键字内容: {keyword_info}")
                    
                    # 5.1 点击关键字类型下拉框
                    keyword_type_selector = '.ant-modal-content:has(.ant-modal-title:has-text("添加资源")) .ant-input-group-addon .ant-select-selector'
                    await self.service.page.click(keyword_type_selector)
                    await asyncio.sleep(0.5)
                    
                    # 5.2 选择关键字类型选项(片名/导演/演员/视频ID)
                    keyword_type_option = f'.ant-select-dropdown .ant-select-item-option-content:has-text("{keyword}")'
                    await self.service.page.click(keyword_type_option, timeout=3000)
                    await asyncio.sleep(0.5)
                    
                    # 5.3 在"请输入"框中填写关键字内容
                    keyword_input = '.ant-modal-content:has(.ant-modal-title:has-text("添加资源")) .ant-input-group input[placeholder="请输入"]'
                    await self.service.page.fill(keyword_input, keyword_info)
                    
                    # 5.4 点击查询按钮
                    await self.service.page.click('.ant-modal-content:has(.ant-modal-title:has-text("添加资源")) button:has-text("查 询")')
                    logger.info("已点击查询按钮")
                    await asyncio.sleep(1)  # 等待搜索结果
                except Exception as e:
                    logger.warning(f"设置关键字搜索失败: {str(e)}")
            
            # 6. 选择搜索结果
            try:
                # 等待2秒确保查询完成
                await asyncio.sleep(2)
                
                # 检查是否有搜索结果
                result_table = '.ant-modal-content:has(.ant-modal-title:has-text("添加资源")) .ant-table-tbody tr'
                has_results = await self.service.page.query_selector(result_table)
                
                if has_results:
                    logger.info("检测到搜索结果，选择资源")
                    
                    # 使用表格头部的全选框（如果需要全选）
                    if resource_number > 3:
                        # 点击表头的全选框
                        select_all_checkbox = '.ant-modal-content:has(.ant-modal-title:has-text("添加资源")) .ant-table-thead .ant-checkbox-wrapper input'
                        select_all_exists = await self.service.page.query_selector(select_all_checkbox)
                        
                        if select_all_exists:
                            logger.info("使用全选框选择所有资源")
                            await self.service.page.click(select_all_checkbox)
                            # 等待1秒确保全选完成
                            await asyncio.sleep(1)
                        else:
                            logger.warning("未找到全选框，将使用单个选择方式")
                            # 如果没有全选框，则逐个选择
                            for i in range(min(resource_number, 10)):  # 限制最大选择数量为10
                                checkbox = f'.ant-modal-content:has(.ant-modal-title:has-text("添加资源")) .ant-table-tbody tr:nth-child({i+1}) .ant-checkbox-input'
                                await self.service.page.click(checkbox)
                                logger.info(f"已选择第{i+1}个资源结果")
                    else:
                        # 如果只需要选择少量资源，直接逐个选择
                        for i in range(min(resource_number, 10)):  # 限制最大选择数量为10
                            checkbox = f'.ant-modal-content:has(.ant-modal-title:has-text("添加资源")) .ant-table-tbody tr:nth-child({i+1}) .ant-checkbox-input'
                            await self.service.page.click(checkbox)
                            logger.info(f"已选择第{i+1}个资源结果")
                    
                    # 点击确定按钮
                    await self.service.page.click('.ant-modal-content:has(.ant-modal-title:has-text("添加资源")) .ant-modal-footer button.ant-btn-primary:has-text("确 定")')
                    logger.info("已点击确定按钮")
                    
                    # 等待对话框关闭
                    await self.service.page.wait_for_selector('.ant-modal-title:has-text("添加资源")', state='hidden', timeout=5000)
                    
                    return {
                        "success": True,
                        "message": "资源选择成功，接下来请确认是否需要继续添加栏目",
                        "next_tool": "select_column_resource",
                        "data": {
                            "module": resource_module,
                            "channel": resource_channel,
                            "media_type": resource_media_type,
                            "selected": True
                        }
                    }
                else:
                    logger.warning("未找到搜索结果")
                    
                    # 点击取消按钮
                    await self.service.page.click('.ant-modal-content:has(.ant-modal-title:has-text("添加资源")) .ant-modal-footer button:has-text("取 消")')
                    
                    return {
                        "success": False,
                        "message": "未找到可选择的资源结果，请尝试修改搜索条件",
                        "data": {
                            "selected": False
                        }
                    }
            except Exception as e:
                logger.error(f"选择资源结果失败: {str(e)}")
                # 尝试点击取消按钮
                try:
                    await self.service.page.click('.ant-modal-content:has(.ant-modal-title:has-text("添加资源")) .ant-modal-footer button:has-text("取 消")')
                except:
                    pass
                    
                return {
                    "success": False,
                    "message": f"选择资源结果失败: {str(e)}",
                    "data": {
                        "error": str(e)
                    }
                }
                
        except Exception as e:
            logger.error(f"选择资源失败: {str(e)}")
            return {
                "success": False,
                "message": f"选择资源失败: {str(e)}",
                "data": {
                    "error": str(e)
                }
            }

