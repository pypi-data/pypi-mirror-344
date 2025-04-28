# 开发人员： Xiaoqiang
# 微信公众号: xiaoqiangclub
# 开发时间： 2025/4/28 10:41
# 文件名称： dp_is_login_test.py
# 项目描述： 检测DrissionPage是否登录指定网站
# 开发工具： PyCharm

from wechat_draft import dp_is_login

if __name__ == '__main__':
    url = 'https://mp.weixin.qq.com/cgi-bin/home'
    # url = 'https://www.baidu.com'
    login_text = '首页'
    print(dp_is_login(url, login_text, timeout=20, close_browser=False, fuzzy_search=False))
