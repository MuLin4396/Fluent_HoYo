import asyncio
import json
import re
from datetime import datetime

import openpyxl
from aiohttp import ClientSession, ClientTimeout, ClientError

headers = {
	'Referer'   : 'https://www.miyoushe.com/',
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0'
}

_RE = re.compile(r'[\000-\010]|[\013-\014]|[\016-\037]')

def record_message(sheet, uid, ip, nickname, floor_id, time, content):
	row = [f'{nickname}', f'{uid}', f'{ip}', f'{floor_id}', f'{time}', f'{content}']
	sheet.append(row)

async def fetch(session, url, performAction):
	retries = 3
	for i in range(retries):
		try:
			async with session.get(url) as response:
				return await response.json()
		except (ClientError, asyncio.TimeoutError) as e:
			if i < retries - 1:
				performAction(f'请求失败，正在重试...（{i + 1}/{retries}）')
				await asyncio.sleep(2)
			else:
				performAction(f'请求失败，重试次数已用完：{e}')
				raise

async def spider_main(action_Controller, inputName, inputID, inputRequest, inputSave, performAction):
	last_id = '0'
	timeout = ClientTimeout(total=120)
	count = 0
	c = 0

	try:
		workbook = openpyxl.load_workbook(f'{inputName}.xlsx')
		sheet = workbook.active
	except FileNotFoundError:
		workbook = openpyxl.Workbook()
		sheet = workbook.active
		header = ['名称', 'UID', 'IP', '楼层', '时间', '内容']
		sheet.append(header)

	async with ClientSession(headers=headers, timeout=timeout) as session:
		while not action_Controller._is_stopped.is_set():
			url = f'https://bbs-api.miyoushe.com/post/wapi/getPostReplies?gids=2&is_hot=false&last_id={last_id}&order_type=1&post_id={inputID}&size={inputRequest}'
			response = await fetch(session, url, performAction)
			list = response['data']['list']

			if not list:
				performAction(f'程序结束时间：{datetime.now()}')
				break

			for obj in list:
				if action_Controller._is_stopped.is_set():
					break
				while action_Controller._is_paused.is_set():
					await asyncio.sleep(0.5)
				if action_Controller._is_stopped.is_set():
					break

				if obj == list[-1]:
					last_id = obj['reply']['floor_id']
					performAction(f'进入下一阶段{last_id}')

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

				if count >= int(inputSave):
					workbook.save(f'{inputName}.xlsx')
					count = 0
					performAction('保存了一次工作簿')

				performAction(f'{time}    {floor_id}\n{c}')

		workbook.save(f'{inputName}.xlsx')
