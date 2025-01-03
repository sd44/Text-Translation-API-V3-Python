# -*- coding: utf-8 -*-

# This simple app uses the '/translate' resource to translate text from
# one language to another.

# This sample runs on Python 2.7.x and Python 3.x.
# You may need to install requests and uuid.
# Run: pip install requests uuid

import json
import os
import urllib.parse as urlparse
import uuid
from http.server import BaseHTTPRequestHandler, HTTPServer

import requests


def trans(text):
    key_var_name = 'TRANSLATOR_TEXT_SUBSCRIPTION_KEY'
    if key_var_name not in os.environ:
        raise Exception(
            'Please set/export the environment variable: {}'.format(
                key_var_name))
    subscription_key = os.environ[key_var_name]

    region_var_name = 'TRANSLATOR_TEXT_REGION'
    if region_var_name not in os.environ:
        raise Exception(
            'Please set/export the environment variable: {}'.format(
                region_var_name))
    region = os.environ[region_var_name]

    endpoint_var_name = 'TRANSLATOR_TEXT_ENDPOINT'
    if endpoint_var_name not in os.environ:
        raise Exception(
            'Please set/export the environment variable: {}'.format(
                endpoint_var_name))
    endpoint = os.environ[endpoint_var_name]

    # If you encounter any issues with the base_url or path, make sure that you
    # are using the latest endpoint:
    # https://docs.microsoft.com/azure/cognitive-services/translator/reference/v3-0-translate

    path = '/translate?api-version=3.0'
    params = '&from=en&from=zh-Hans&to=en&to=zh-Hans'
    constructed_url = endpoint + path + params

    headers = {
        'Ocp-Apim-Subscription-Key': subscription_key,
        'Ocp-Apim-Subscription-Region': region,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    # You can pass more than one object in body.
    body = [{'text': text}]
    request = requests.post(constructed_url, headers=headers, json=body)
    response = request.json()

    print(
        json.dumps(response,
                   sort_keys=True,
                   indent=4,
                   ensure_ascii=False,
                   separators=(',', ': ')))

    return response[0]['translations'][0]['text'] + '\n\n' + response[0][
        'translations'][1]['text']


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        # 解析查询参数
        query = urlparse.urlparse(self.path).query
        params = urlparse.parse_qs(query)
        command_str = params.get("command", [""])[0].strip()

        # 处理空格分隔的命令
        response = self.handle_command(command_str)

        # 设置响应头
        self.send_response(200)
        self.send_header("Content-type", "text/plain; charset=utf-8")
        self.end_headers()

        # 发送响应
        self.wfile.write(response.encode("utf-8"))

    def handle_command(self, command_str):
        # 拆分空格分隔的字符串为列表
        if not command_str:
            return {"message": "No command provided."}
        return trans(command_str)


def run(server_class=HTTPServer,
        handler_class=SimpleHTTPRequestHandler,
        port=8006):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting HTTP server on port {port}...")
    httpd.serve_forever()


if __name__ == "__main__":
    run()
