# 开发人员： Xiaoqiang
# 微信公众号: xiaoqiangclub
# 开发时间： 2025/4/26 10:48
# 文件名称： set_publish_params.py
# 项目描述： 设置微信公众号文章群发参数
# 开发工具： PyCharm

from wechat_draft import SetPublishParams


async def set_publish_params():
    set_publish_params = SetPublishParams([ '表彰管理系统工具','微信聊天数据管理工具', ], set_original=True,
                                          author='XiaoqiangClub',
                                          quick_reprint=True, set_collect='游戏', open_comment=False,
                                          set_praise=False, original_link=None, hide_browser=True)
    return set_publish_params.run()


if __name__ == '__main__':
    import asyncio

    print(asyncio.run(set_publish_params()))
