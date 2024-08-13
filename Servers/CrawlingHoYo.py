import asyncio
import openpyxl
from aiohttp import ClientSession, ClientTimeout, ClientError
import json
import re
from datetime import datetime

headers = {
	'Referer'   : 'https://www.miyoushe.com/',
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0'
}

_RE = re.compile(r'[\000-\010]|[\013-\014]|[\016-\037]')

def record_message(sheet, uid, ip, nickname, floor_id, time, content):
	row = [f'{nickname}', f'{uid}', f'{ip}', f'{floor_id}', f'{time}', f'{content}']
	sheet.append(row)

async def fetch(session, url):
	retries = 3
	for i in range(retries):
		try:
			async with session.get(url) as response:
				return await response.json()
		except (ClientError, asyncio.TimeoutError) as e:
			if i < retries - 1:
				print(f"请求失败，正在重试...（{i + 1}/{retries}）")
				await asyncio.sleep(2)
			else:
				print(f"请求失败，重试次数已用完：{e}")
				raise

async def spider_main(dynamic_id, file_path):
	last_id = '0'
	timeout = ClientTimeout(total=120)
	count = 0
	c = 0

	try:
		workbook = openpyxl.load_workbook(file_path)
		sheet = workbook.active
	except FileNotFoundError:
		workbook = openpyxl.Workbook()
		sheet = workbook.active
		header = ['名称', 'UID', 'IP', '楼层', '时间', '内容']
		sheet.append(header)

	async with ClientSession(headers=headers, timeout=timeout) as session:
		while True:
			url = f'https://bbs-api.miyoushe.com/post/wapi/getPostReplies?gids=2&is_hot=false&last_id={last_id}&order_type=1&post_id={dynamic_id}&size=50'
			response = await fetch(session, url)
			list = response['data']['list']

			if not list:
				print('程序结束时间：', datetime.now())
				break

			for obj in list:
				if obj == list[-1]:
					last_id = obj['reply']['floor_id']
					print('进入下一阶段', last_id)

				obj = json.loads(json.dumps(obj, ensure_ascii=False))
				floor_id = obj['reply']['floor_id']
				content = _RE.sub(r'', obj['reply']['content'])
				date_time = obj['reply']['updated_at']
				time = datetime.fromtimestamp(date_time)
				uid = obj['reply']['uid']
				nickname = obj['user']['nickname']
				ip = obj['user']['ip_region']

				record_message(sheet, uid, ip, nickname, floor_id, time, content)
				count += 1
				c += 1

				if count >= 100000:
					workbook.save(file_path)
					count = 0
					print('保存了一次工作簿')

				print(time, floor_id)
				print(c)

		workbook.save(file_path)
