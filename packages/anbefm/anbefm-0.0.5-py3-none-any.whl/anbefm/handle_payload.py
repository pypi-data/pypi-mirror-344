'''
Author: liubei
Date: 2021-04-08 17:21:53
LastEditTime: 2021-04-09 11:48:44
Description: 
'''
import asyncio
import os
import json
import uuid
import asyncio
import json
from tornado.web import RequestHandler


class PayloadParams():
    ...


class HandlePayload(RequestHandler):
    upload_dir = './'  # 子类需指定该属性
    payload: dict = {}

    async def prepare(self):
        fut = super().prepare()

        if asyncio.coroutines.iscoroutine(fut):
            await fut

        print(self.request.headers)

        if 'application/json' in self.request.headers.get('Content-type', '') and self.request.body:
            res = '{}'
            try:
                res = self.request.body.decode('utf-8')
            except:
                res = self.request.body.decode('gbk')
            self.payload = json.loads(res) or {}
            print('self.payload-->', self.payload)
        elif 'multipart/form-data' in self.request.headers.get('Content-type', ''):
            self.payload = {}
            for k in self.request.arguments.keys():
                self.payload[k] = self.request.arguments.get(k)[0].decode('utf-8')
            files = self.request.files or {}
            for k in files.keys():
                self.payload[k] = [self.save_file(f) for f in files[k]]
            print('self.payload-->', self.payload)

    def save_file(self, f):
        dirpath = self.upload_dir
        if not os.path.exists(dirpath):
            os.makedirs(dirpath)

        res = {}
        res['origin_file_name'] = f.get('filename')
        res['file_type'] = os.path.splitext(f.get('filename'))[-1]
        res['file_name'] = str(uuid.uuid1()) + res['file_type']
        res['file_size'] = len(f.get('body'))
        res['file_error_msg'] = None

        with open(dirpath + res['file_name'], mode='wb') as sf:
            try:
                sf.write(f.get('body'))
            except Exception as e:
                res['file_error_msg'] = '写入文件失败'
                raise e

        return res
