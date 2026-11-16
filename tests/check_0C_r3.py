"""0C 第三輪（加分）的檢查：地點清單要有「系館」，而且可以在那裡登記。"""
import service
from config import LOCATIONS
from checklib import check, new_db, read_source

db = new_db()
check("0C-r3 地點清單有系館", "系館" in LOCATIONS, True)
check("0C-r3 可以在系館登記", service.report_found(db, "雨傘", "系館")["ok"], True)
check("0C-r3 LOCATIONS 只寫一次", read_source("config.py").count("LOCATIONS ="), 1)