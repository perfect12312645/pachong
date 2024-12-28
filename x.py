import requests
import json
from tqdm import tqdm

# x_url=input("请输入想爬取的视屏url：")

url_list = []


def get_video_message(txt):
    start_index = len('https://x.com/')
    with open(txt, 'r', encoding='utf-8') as f:
        for x_url in f.readlines():
            result = x_url[start_index:].strip()
            title = result.rsplit('/', 1)[1].strip()
            url = "https://download-x-video.com/api/parse"
            headers = {
                'Content-Type': 'application/json',
                "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0"
            }
            data = {
                "url": result
            }
            json_data = json.dumps(data)
            response = requests.post(url, data=json_data, headers=headers)
            if response.status_code == 200:
                # 如果请求成功，解析并打印响应内容
                url_list.append({"name": title, "url": response.json().get("videoInfos")[2].get("url")})
            else:
                # 如果请求失败，打印错误信息
                print('Failed to send POST request. Status code:', response.status_code)
                print('Response content:', response.content)


get_video_message("x.txt")


def download_video(name, url):
    res = requests.get(url, stream=True)
    total_size_in_bytes = int(res.headers.get('content-length', None))
    block_size = 1024
    with open(f"file/{name}.mp4", "wb") as f:
        with tqdm(total=total_size_in_bytes, unit='B', unit_scale=True, unit_divisor=1024, ncols=100,
                  desc=f"{name} 下载") as pbar:
            for data in res.iter_content(block_size):
                if data:  # 确保data不是空的（可能是最后一个块）
                    f.write(data)  # 写入数据块到文件
                    pbar.update(len(data))  # 更新进度条
    print(f"{name}下载成功！")


if __name__ == '__main__':
    for item in url_list:
        download_video(item["name"], item["url"])
