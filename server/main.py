import json
import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI, Header
from starlette.middleware.cors import CORSMiddleware
from operator import itemgetter

app = FastAPI()
rank = []

# CORSを回避するために追加（今回の肝）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,   # 追記により追加
    allow_methods=["*"],      # 追記により追加
    allow_headers=["*"]       # 追記により追加
)


with open("rank.json", "r") as f:
    rankjson = json.load(f)
    rank.append(rankjson["master"])
    rank.append(rankjson["hard"])
    rank.append(rankjson["normal"])

print("Load Successfully")

@app.get("/wikirunner/{difficult}")
def root(difficult: int, kyit_cache_allowed: str = Header("yes")):
    if kyit_cache_allowed == "yes" and difficult <= 2 and difficult >=0:
        return rank[difficult]
    else:
        return "fail: Use cache. or wrong difficultly"
    
@app.get("/wikirunner/write/{difficult}")
def read_item(name: str, score: int, time: str, difficult: int, kyit_cache_allowed: str = Header("yes")):
    if kyit_cache_allowed == "no" and difficult <= 2 and difficult >=0:
        dt_now = datetime.datetime.now()
        rank[difficult].append({"name": name, "score": score, "time":time , "date": dt_now.strftime("%Y/%m/%d/%H:%M")})
        rank[difficult].sort(key=itemgetter('score'), reverse=True)

        return "success"
    else:
        return "fail: Do not use cache. or wrong difficultly"

def backup():
    for a in range(3):
        max_ren = 100
        num = len(rank[a])
        print(num)
        if num > max_ren:
            del rank[a][max_ren - num:]

    with open("rank.json", "w") as f:
        dumprank = {
            "master": rank[0],
            "hard": rank[1], 
            "normal": rank[2]
        }
        json.dump(dumprank, f)
        print("buckup sucsess")

@app.on_event("startup")
def skd_process():
    # スケジューラのインスタンスを作成する
    scheduler = BackgroundScheduler()
    # スケジューラーにジョブを追加する
    scheduler.add_job(backup, "interval", seconds=30)
    # スケジューラを開始する
    scheduler.start()