"""NEIS에서 면목고 급식을 받아 meals.json으로 저장합니다 (앱의 백업 데이터).
지난 1주 ~ 앞으로 5주를 주 단위로 받아옵니다. NEIS_KEY 환경변수가 있으면 사용합니다."""
import json, os, urllib.parse, urllib.request
from datetime import datetime, timedelta, timezone

ATPT, SCHOOL = "B10", "7010077"
KEY = os.environ.get("NEIS_KEY", "")

today = datetime.now(timezone(timedelta(hours=9))).date()
monday = today - timedelta(days=today.weekday())
rows = []
for w in range(-1, 6):
    start = monday + timedelta(weeks=w)
    end = start + timedelta(days=6)
    q = {"Type": "json", "pSize": "20", "ATPT_OFCDC_SC_CODE": ATPT, "SD_SCHUL_CODE": SCHOOL,
         "MLSV_FROM_YMD": start.strftime("%Y%m%d"), "MLSV_TO_YMD": end.strftime("%Y%m%d")}
    if KEY:
        q["KEY"] = KEY
    url = "https://open.neis.go.kr/hub/mealServiceDietInfo?" + urllib.parse.urlencode(q)
    with urllib.request.urlopen(url, timeout=30) as r:
        data = json.load(r)
    rows += data.get("mealServiceDietInfo", [{}, {}])[1].get("row", [])

with open("meals.json", "w", encoding="utf-8") as f:
    json.dump({"updated": datetime.now(timezone.utc).isoformat(), "rows": rows}, f, ensure_ascii=False)
print(f"saved {len(rows)} meals")
