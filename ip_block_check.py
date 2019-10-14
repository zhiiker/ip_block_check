# -*- encoding: utf-8 -*-

import requests
import time
import db
import result
import post2tg


def run():
    # 从tg机器人获得信息
    html = r"https://api.telegram.org/bot983128077:AAHYi5ouhw_pMnQe9**********4/getUpdates"
    info1 = requests.get(html)
    info1.encoding = 'utf-8'
    info = info1.json()
    update_id = 184912313

    # 温馨欢迎语
    # 解决因tg编译已发送信息造成错误
    try:
        text0 = "请务必阅读关于后输出正确指令，否则可能报错" + "\n"
        # text1 = "%23+%e5%9f%9f%e5%90%8d%e6%88%96%e8%80%85ip%e6%a0%bc%e5%bc%8f%e5%bf%85%e9%a1%bb%e6%98%afIP%2fPort" + "\n"
        # text2 = "%23+%e9%bb%98%e8%ae%a4%e6%9c%ba%e5%99%a8%e4%ba%ba%e4%bc%9a%e6%af%8f%e5%a4%a912%3a00%3a00%e6%8e%a8%e9%80%81%e5%b7%b2%e4%bf%9d%e5%ad%98ip%e7%9a%84%e6%9f%a5%e8%af%a2%e7%bb%93%e6%9e%9c" + "\n"
        text3 = "%23+%e6%9f%a5%e8%af%a2%e5%9f%9f%e5%90%8dwww.google.com" + "\n"
        text4 = "%26ip_check+www.google.com%2f80" + "\n"
        text5 = "%23+%e6%9f%a5%e8%af%a2140.238.33.201%2f22" + "\n"
        text6 = "%26ip_check+140.238.33.201%2f22" + "\n"
        text7 = "%23+%e6%9f%a5%e8%af%a2%e5%b7%b2%e4%bf%9d%e5%ad%98%e5%9f%9f%e5%90%8d" + "\n"
        text8 = "%26ip_saved" + "\n"
        text9 = "%23+%e5%88%a0%e9%99%a4%e5%9f%9f%e5%90%8d%e8%ae%b0%e5%bd%95140.238.33.201%2f22" + "\n"
        text10 = "%26ip_delete+140.238.33.201%2f22" + "\n"
        text11 = '%23 %e6%9f%a5%e8%af%a2%e6%89%80%e6%9c%89%e5%b7%b2%e4%bf%9d%e5%ad%98%e7%9a%84%e5%9f%9f%e5%90%8d' + "\n"
        text12 = "%2fip_check"
        text = text0 + text3 + text4 + text5 + text6 + text7 + text8 + text9 + text10 + text11 + text12
        post2tg.post(info["result"][-1]["message"]["from"]["id"], text)
    except KeyError:
        pass

    # 主程序
    while True:

        # 新数据入库
        for i in range(len(info["result"])):
            try:
                if "&ip_check" in info["result"][i]["message"]["text"]:
                    db.ip_saved(info, i)
                else:
                    pass

            # 解决发送后如果编辑信息造成的bug,懒得再判断了，直接默认忽视编辑过得信息
            except KeyError:
                pass

        # 查看已保存或者删除
        info1 = requests.get(html)
        info1.encoding = 'utf-8'
        info = info1.json()
        # 解决由于getupdate失败的问题
        try:
            if info["result"][-1]["update_id"] != update_id:
                update_id = info["result"][-1]["update_id"]

                # 查看保存的ip/port
                try:
                    if ("&ip_saved" or "/ip_saved") in info["result"][-1]["message"]["text"]:
                        text = "你保存的ip记录为："
                        post2tg.post(info["result"][-1]["message"]["from"]["id"], text)
                        for x in db.IP_Port.find({"username": info["result"][-1]["message"]["from"]["username"]}):
                            if x["ip_port"] != "-1":
                                post2tg.post(info["result"][-1]["message"]["from"]["id"],
                                             x["ip_port"].replace("&ip_check ", ""))

                    # 查看保存的ip/port
                    if "&ip_delete" in info["result"][-1]["message"]["text"]:
                        ip_delete = info["result"][-1]["message"]["text"].replace("&ip_delete ", "")
                        for y in db.IP_Port.find({"ip_port": ip_delete}):
                            text = "已从数据库删除IP: " + "\n" + ip_delete
                            post2tg.post(info["result"][-1]["message"]["from"]["id"], text)
                            y_delete = {"ip_port": "-1"}
                            # 删除数据库保存的ip(将其值重置为-1)
                            db.IP_Port.update_one(y, {"$set": y_delete})

                    # 快速查询已保存ip状态
                    if "/ip_check" in info["result"][-1]["message"]["text"]:
                        for x in db.IP_Port.find({"chat_id": info["result"][-1]["message"]["from"]["id"]}):
                            try:
                                result.check_result(x['chat_id'], x['ip_port'])
                            except IndexError:
                                pass

                    # 查看保存的ip/port
                    if "/ip_saved" in info["result"][-1]["message"]["text"]:
                        text = "服务器保存记录的ip记录为："
                        post2tg.post(info["result"][-1]["message"]["from"]["id"], text)
                        for x in db.IP_Port.find({"username": info["result"][-1]["message"]["from"]["username"]}):
                            if x["ip_port"] != "-1":
                                post2tg.post(info["result"][-1]["message"]["from"]["id"],
                                             x["ip_port"].replace("&ip_check ", ""))

                    # 快速删除所有保存ip
                    if "/ip_delete" in info["result"][-1]["message"]["text"]:
                        for y in db.IP_Port.find({"chat_id": info["result"][-1]["message"]["from"]["id"]}):
                            y_delete = {"ip_port": "-1"}
                            db.IP_Port.update_one(y, {"$set": y_delete})
                        post2tg.post(info["result"][-1]["message"]["from"]["id"], "已删除服务器保存IP/Port")
                except KeyError:
                    pass
        except IndexError:
            pass

        time.sleep(5)


run()
