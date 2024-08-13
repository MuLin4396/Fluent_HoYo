import json  # 用于处理JSON数据
from datetime import datetime  # 用于处理日期和时间
import re  # 用于正则表达式操作
import openpyxl  # 用于处理Excel文件
from aiohttp import ClientSession, ClientTimeout, ClientError  # 用于异步HTTP请求
import asyncio  # 用于异步编程

# 设置HTTP请求的头部信息
headers = {
    'Referer': 'https://www.miyoushe.com/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0'
}

# 创建正则表达式用于去除控制字符
_RE = re.compile(r'[\000-\010]|[\013-\014]|[\016-\037]')

# 定义记录消息的函数，将信息保存到Excel文件中
def record_message(sheet, uid, ip, nickname, floor_id, time, content):
    row = [f'{nickname}', f'{uid}', f'{ip}', f'{floor_id}', f'{time}', f'{content}']
    sheet.append(row)  # 将这一行数据添加到工作表中

# 异步HTTP GET请求，增加重试机制
async def fetch(session, url):
    retries = 3  # 定义重试次数
    for i in range(retries):
        try:
            async with session.get(url) as response:
                return await response.json()  # 返回JSON响应
        except (ClientError, asyncio.TimeoutError) as e:
            if i < retries - 1:
                print(f"请求失败，正在重试...（{i + 1}/{retries}）")
                await asyncio.sleep(2)  # 等待2秒后重试
            else:
                print(f"请求失败，重试次数已用完：{e}")
                raise

# 异步主函数
async def main():
    last_id = '0'
    timeout = ClientTimeout(total=120)  # 设置超时时间为120秒
    count = 0  # 初始化计数器
    c=0

    # 打开现有的Excel文件（如果没有则创建）
    try:
        workbook = openpyxl.load_workbook('spider_data.xlsx')
        sheet = workbook.active
    except FileNotFoundError:
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        # 添加表头（如果文件不存在）
        header = ['名称', 'UID', 'IP', '楼层', '时间', '内容']
        sheet.append(header)

    # 创建异步HTTP会话
    async with ClientSession(headers=headers, timeout=timeout) as session:
        while True:
            # 构建请求URL，增加size参数以获取更多数据
            url = f'https://bbs-api.miyoushe.com/post/wapi/getPostReplies?gids=2&is_hot=false&last_id={last_id}&order_type=1&post_id=55221094&size=50'
            response = await fetch(session, url)  # 发送异步请求获取响应
            list = response['data']['list']  # 获取回复列表数据

            # 如果列表为空，则程序结束
            if not list:
                print('程序结束时间：', datetime.now())
                break

            # 遍历列表中的每个回复对象
            for obj in list:
                # 如果当前对象是列表中的最后一个
                if obj == list[-1]:
                    last_id = obj['reply']['floor_id']  # 获取最后一个回复的楼层ID
                    print('进入下一阶段', last_id)  # 输出日志信息

                # 去除文本中的控制字符
                obj = json.loads(json.dumps(obj, ensure_ascii=False))
                floor_id = obj['reply']['floor_id']  # 获取楼层ID
                content = _RE.sub(r'', obj['reply']['content'])  # 去除控制字符
                date_time = obj['reply']['updated_at']  # 获取回复更新时间的时间戳
                time = datetime.fromtimestamp(date_time)  # 将时间戳转换为datetime对象
                uid = obj['reply']['uid']  # 获取用户ID
                nickname = obj['user']['nickname']  # 获取用户昵称
                ip = obj['user']['ip_region']  # 获取用户IP地址

                # 记录消息到工作表中
                record_message(sheet, uid, ip, nickname, floor_id, time, content)
                count += 1  # 更新计数器
                c+=1

                # 每处理一万条数据，保存一次工作簿
                if count >= 100000:
                    workbook.save('spider_data.xlsx')
                    count = 0  # 重置计数器
                    print('保存了一次工作簿')

                # 输出日志信息
                print(time,floor_id)
                print(c)
                # print(time, floor_id, uid, nickname, ip, content)

        # 所有数据处理完毕后保存工作簿
        workbook.save('spider_data.xlsx')

# 运行异步主函数
asyncio.run(main())