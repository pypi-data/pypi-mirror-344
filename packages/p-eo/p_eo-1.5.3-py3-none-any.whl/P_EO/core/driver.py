import time
from pathlib import Path
from urllib.parse import urlparse, parse_qsl, unquote

from selenium.webdriver import Chrome, ChromeOptions, ChromeService
from selenium.webdriver.remote.webdriver import WebDriver
from webdrivermanager_cn import ChromeDriverManager, GeckodriverManager

from P_EO.common.common import get_chrome_driver_by_port
from P_EO.common.config import Default
from P_EO.common.log import LogMixin
from P_EO.common.time_ import get_time
from P_EO.core.javascript import JavaScript
from P_EO.public_variables.public_variables import Public


class Driver(LogMixin):
    def __init__(self, driver: WebDriver):
        self.__d = driver

    @property
    def web_driver(self):
        """
        返回 WebDriver 对象
        :return:
        """
        return self.__d

    def set_implicitly_wait(self, timeout: float = Default.IMPLICITLY_WAIT):
        """
        设置隐式等待时间
        :param timeout:
        :return:
        """
        self.web_driver.implicitly_wait(time_to_wait=timeout)
        self.log.debug(f'隐式等待设定: {timeout} s')

    @property
    def get_implicitly_wait(self):
        """
        获取当前隐式等待设定时间
        """
        return self.web_driver.timeouts.implicit_wait

    @property
    def get_cur_window_size(self):
        """
        获取当前网页窗口大小
        :return:
        """
        return self.web_driver.get_window_size()

    def set_cur_window_size(self, width=0, height=0):
        """
        设定当前窗口大小，如果窗口大小为0，则默认最大化打开
        :param width:
        :param height:
        :return:
        """
        if width > 0 and height > 0:
            self.web_driver.set_window_size(width=width, height=height)
            self.log.debug(f'设定浏览器窗口: {width} {height}')
        else:
            self.web_driver.maximize_window()
            self.log.debug('浏览器窗口最大化')
        self.log.info(f'当前窗口大小: {self.get_cur_window_size}')

    @property
    def get_cur_url(self):
        """
        获取当前url
        :return:
        """
        return self.current_url

    @property
    def current_url(self):
        return self.web_driver.current_url

    @property
    def url_parser(self):
        """
        url解析器
        <scheme>://<netloc>/<path>;<params>?<query>#<fragment>
        :return:
        """
        return Url(self.get_cur_url)

    @property
    def get_cur_url_parser(self):
        return self.url_parser

    @property
    def url_query_dict(self):
        """
        url解析器
        <scheme>://<netloc>/<path>;<params>?<query>#<fragment>
        :return:
        """
        return self.url_parser.query_dict

    def get(self, url):
        """
        打开新url
        :param url:
        :return:
        """
        self.web_driver.get(url)
        self.log.info(f'访问url: {url}')

    def wait_url_changed(self, url, timeout=Default.TIMEOUT):
        """
        等待url跳转为指定的url
        :param url:
        :param timeout:
        :return:
        """
        trigger_time = time.time()
        while time.time() - trigger_time <= timeout:
            try:
                if url in self.current_url:
                    return True
            except:
                pass
        return False

    def switch_frame_to_default(self):
        """
        切换到最外层 frame
        :return:
        """
        self.web_driver.switch_to.default_content()

    @property
    def js(self):
        return JavaScript(driver=self.web_driver)

    def open_new_window(self, url=''):
        """
        打开一个新tab，如果url有值，则打开指定url
        :param url:
        :return:
        """
        self.js.open_new_tab(url)
        self.log.info(f'浏览器打开新tab: {url}')

    def goto_new_route(self, route=''):
        """
        切换到同host下新route
        :param route:
        :return:
        """
        self.js.goto_new_route(route)
        self.log.info(f'浏览器切换路由: {route}')

    @property
    def title(self):
        """
        获取title
        :return:
        """
        return self.web_driver.title

    def wait_title_changed(self, title, timeout=Default.TIMEOUT):
        """
        等待title跳转为指定的title
        :param title:
        :param timeout:
        :return:
        """
        trigger_time = time.time()
        while time.time() - trigger_time <= timeout:
            try:
                if title in self.title:
                    return True
            except:
                pass
        return False

    def back(self):
        """
        返回
        :return:
        """
        self.web_driver.back()
        self.log.info(f'浏览器返回上一级页面 - {self.current_url}')

    def forward(self):
        """
        前进
        :return:
        """
        self.web_driver.forward()
        self.log.info(f'浏览器前进下一级页面 - {self.current_url}')

    def refresh(self, wait=Default.REFRESH_WAIT):
        """
        刷新
        :param wait: 默认刷新后暂停1s
        :return:
        """
        self.web_driver.refresh()
        self.log.info(f'浏览器刷新页面，等待 {wait} s')
        time.sleep(wait)

    def screenshots(self, file_path=None):
        """
        截图
        :param file_path: 截图完整路径
        :return:
        """
        if not file_path:
            file_path = Default.WEB_PAGE_PATH
            file_path.mkdir(parents=True, exist_ok=True)
            img_name = f'{get_time()}_{self.title}.png'
            file_path = Path(file_path).joinpath(img_name)

        self.web_driver.save_screenshot(filename=file_path)
        self.log.info(f'浏览器截图: {file_path}')
        return file_path

    def quit(self):
        """
        退出浏览器
        :return:
        """
        self.web_driver.quit()
        self.log.info('关闭浏览器')

    @property
    def alert(self):
        """
        切换到 Alert 窗口
        :return:
        """
        return self.web_driver.switch_to.alert

    @property
    def error_img(self) -> str:
        return Public.last_error_image

    @property
    def cookies(self):
        """
        返回 Cookie 对象
        :return:
        """
        return Cookie(driver=self.web_driver)

    @property
    def cookies_dict(self):
        return self.cookies.cookie_dict

    @property
    def window(self):
        """
        返回 window 对象
        :return:
        """
        return Window(driver=self.web_driver)

    def maximize_window(self):
        self.window.maximize_window()

    def minimize_window(self):
        self.window.minimize_window()

    def switch_window_by_title(self, title):
        return self.window.switch_window_by_title(title)

    def switch_window_by_url(self, url):
        return self.window.switch_window_by_url(url)


class Cookie:
    def __init__(self, driver: WebDriver):
        self.__d = driver

    @property
    def cookies(self):
        return self.__d.get_cookies()

    def get_cookie(self, name):
        return self.__d.get_cookie(name)

    def add_cookie(self, **cookie_dict):
        self.__d.add_cookie(cookie_dict)

    def delete_cookie(self, name):
        self.__d.delete_cookie(name)

    def delete_all_cookies(self):
        self.__d.delete_all_cookies()

    @property
    def cookie_dict(self):
        return {i['name']: unquote(i['value']) for i in self.cookies}


class Window(LogMixin):
    def __init__(self, driver: WebDriver):
        self.__d = driver

    def maximize_window(self):
        self.__d.maximize_window()
        self.log.info('最大化浏览器窗口')

    def minimize_window(self):
        self.__d.minimize_window()
        self.log.info('最小化浏览器窗口')

    @property
    def window_size(self):
        return self.__d.get_window_size()

    def set_window_size(self, width, height):
        self.__d.set_window_size(width=width, height=height)
        self.log.info(f'设置浏览器窗口大小: {width} x {height}')

    @property
    def cur_window_handle(self):
        return self.__d.current_window_handle

    @property
    def window_handles(self):
        return self.__d.window_handles

    def switch_window(self, window_handle):
        self.__d.switch_to.window(window_handle)
        self.log.info(f'切换到指定handle: {window_handle}')

    def switch_window_by_title(self, title: str):
        """
        根据title切换windows handle
        :param title:
        :return:
        """
        _dict = {}
        for _handle in self.window_handles:
            self.__d.switch_to.window(_handle)
            _dict[_handle] = self.__d.title
            if title in self.__d.title:
                self.log.info(f'切换到指定title: {title} - {_handle}')
                return True

        self.log.warning(f'未找到指定title: {title} - {_dict}')
        return False

    def switch_window_by_url(self, url: str):
        """
        根据url切换windows handle
        :param url:
        :return:
        """
        _dict = {}
        for _handle in self.window_handles:
            self.__d.switch_to.window(_handle)
            _dict[_handle] = self.__d.current_url
            if url in self.__d.current_url:
                self.log.info(f'切换到指定url: {url} - {_handle}')
                return True

        self.log.warning(f'未找到指定url: {url} - {_dict}')
        return False

    def switch_window_by_index(self, index: int):
        """
        根据索引切换windows handle
        :param index: 0, 1, 2,...
        :return:
        """
        _handle = self.window_handles[index]
        self.switch_window(_handle)
        self.log.info(f'切换到指定索引handle: {index} - {_handle}')

    def switch_to_new_window(self):
        """
        切换到最后一个window handle
        :return:
        """
        self.switch_window_by_index(-1)
        self.log.info(f'切换到末尾handle - {self.cur_window_handle}')

    def close(self):
        """
        关闭window
        :return:
        """
        __cur_handle = self.cur_window_handle
        self.__d.close()
        self.log.info(f'关闭当前浏览器window - {__cur_handle}')

    def close_alone(self):
        """
        如果当前window list不唯一，则可以关闭
        :return:
        """
        __len = self.window_handles
        if len(__len) > 1:
            self.close()
            self.log.info(f'当前窗口数量：{__len}，可以关闭窗口')
            return
        self.log.warning(f'当前窗口数量：{__len}，无法关闭窗口')


    def close_other(self):
        """
        关闭除当前window外的所有window
        :return:
        """
        __cur_handle = self.cur_window_handle
        for _handle in self.window_handles:
            if _handle == __cur_handle:
                continue
            self.switch_window(_handle)
            self.close()
            self.log.debug(f'关闭 tab - {_handle}')
        self.switch_window(__cur_handle)
        self.log.info('关闭除当前window外的所有window')


class Url:
    def __init__(self, url):
        """
        url解析器
        <scheme>://<netloc>/<path>;<params>?<query>#<fragment>
        :param url:
        """
        self.__url = url

    @property
    def url_parser(self):
        url = unquote(self.__url)
        return urlparse(url)

    @property
    def scheme(self):
        return self.url_parser.scheme

    @property
    def hostname(self):
        return self.url_parser.hostname

    @property
    def port(self):
        return self.url_parser.port

    @property
    def host(self):
        """
        <scheme>://<netloc>/<path>
        :return:
        """
        return f'{self.scheme}://{self.hostname}' + (f':{self.port}' if self.port else '')

    @property
    def path(self):
        return self.url_parser.path

    @property
    def params(self):
        return self.url_parser.params

    @property
    def query(self):
        return self.url_parser.query

    @property
    def query_dict(self):
        return {k: v for k, v in parse_qsl(self.query)}

    @property
    def fragment(self):
        return self.url_parser.fragment


class WebDriverManager:
    """
    下载浏览器驱动
    """

    @staticmethod
    def chrome(version='latest', path=None):
        return ChromeDriverManager(path=path, version=version)

    @staticmethod
    def firefox(version='latest', path=None):
        return GeckodriverManager(path=path, version=version)


class ChromeDriver:
    @staticmethod
    def web_driver(version='latest', port=0, detach=False, implicitly_wait=5):
        """
        实例化chrome对象
        :param version: 目标chrome浏览器版本
        :param port: 目标chrome debug 端口
        :param detach: 报错后，是否分离浏览器（即 自动化报错后，不关闭浏览器）
        :param implicitly_wait:
        :return:
        """
        options = ChromeOptions()
        if port:
            options.debugger_address = f'127.0.0.1:{port}'
        if detach:
            options.add_experimental_option('detach', True)
        if version == 'latest' and port:
            version = get_chrome_driver_by_port(port)
        driver_path = WebDriverManager().chrome(version=version).install()
        service = ChromeService(executable_path=driver_path)
        __driver = Chrome(options=options, service=service)
        __driver.implicitly_wait(implicitly_wait)
        return __driver

    def web_driver_new(self, version='latest', port=0, detach=False, implicitly_wait=5):
        return Driver(self.web_driver(version=version, port=port, detach=detach, implicitly_wait=implicitly_wait))

    def debug_driver(self, port=9222, implicitly_wait=5):
        return self.web_driver(port=port, implicitly_wait=implicitly_wait)

    def debug_driver_new(self, version='latest', port=9222, implicitly_wait=5):
        return self.web_driver_new(version=version, port=port, implicitly_wait=implicitly_wait)


def chrome_driver(version='latest', detach=False, implicitly_wait=5):
    return ChromeDriver().web_driver(version=version, detach=detach, implicitly_wait=implicitly_wait)


def chrome_driver_new(version='latest', detach=False, implicitly_wait=5):
    """
    P_EO 的 Driver 对象
    :param version:
    :param detach:
    :param implicitly_wait:
    :return:
    """
    return ChromeDriver().web_driver_new(version=version, detach=detach, implicitly_wait=implicitly_wait)


def debug_chrome_driver(port=9222, implicitly_wait=5):
    """
    接管调试开启调试端口的chrome浏览器
    参考：https://www.jianshu.com/p/962d223f4c5a
    :param port:
    :param implicitly_wait:
    :return:
    """
    return ChromeDriver().debug_driver(port=port, implicitly_wait=implicitly_wait)


def debug_chrome_driver_new(port=9222, implicitly_wait=5):
    """
    接管调试开启调试端口的chrome浏览器，P_EO 的 Driver 对象
    参考：https://www.jianshu.com/p/962d223f4c5a
    :param port:
    :param implicitly_wait:
    :return:
    """
    return ChromeDriver().debug_driver_new(port=port, implicitly_wait=implicitly_wait)
