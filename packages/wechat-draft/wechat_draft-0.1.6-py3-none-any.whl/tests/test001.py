from DrissionPage import Chromium, ChromiumOptions

# 先实例化一个非无头模式的浏览器
browser = Chromium()

# 打开一个页面测试
browser.latest_tab.get('https://www.baidu.com')
print(browser.latest_tab.title)
# 创建无头模式的配置
co = ChromiumOptions().headless()





# 再次打开页面测试
browser.latest_tab.set.window.hide()
browser.latest_tab.get('https://www.baidu.com')

print(browser.latest_tab.title)
# 关闭当前浏览器
browser.quit()