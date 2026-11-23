"""0B 負責：商業規則層（service.py）的測試。

上面兩個是老師的範例；請在「第一輪」「第二輪」下面加上你的測試。
提示：service 的每個函式都回傳 {"ok": ..., "message": ..., "data": ...}，大多只要檢查 ["ok"]。
"""
import pytest

import service


# ---------------- 範例（老師提供）----------------
def test_report_found_normal(db):
    assert service.report_found(db, "雨傘", "圖書館")["ok"] is True


@pytest.mark.parametrize("item_id, claimer, expected_ok", [
    (1, "王小明", True),      # 正常：認領 1 號
    (99, "王小明", False),    # 錯誤：沒有 99 號
])
def test_claim(sample_db, item_id, claimer, expected_ok):
    assert service.claim(sample_db, item_id, claimer)["ok"] is expected_ok


# ---------------- 第一輪：請從這裡開始加 ----------------
@pytest.mark.parametrize("category, location, description, expected_ok", [
    ("雨傘", "圖書館", "", True),      # 正常
    ("飛機", "圖書館", "", False),     # 錯誤：類別不在清單
    ("水壺", None, "", False),         # 錯誤：沒說地點
    ("水壺", "月球", "", False),       # 錯誤：地點不在清單
])
def test_report_found(db, category, location, description, expected_ok):
    assert service.report_found(db, category, location, description)["ok"] is expected_ok


def test_claim_without_id(sample_db):
    assert service.claim(sample_db, None, "王小明")["ok"] is False


def test_search_by_category(sample_db):
    result = service.search(sample_db, "雨傘", None)
    assert len(result["data"]["items"]) == 2



# ---------------- 第二輪：邊界與錯誤情況 ----------------
