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
@pytest.mark.parametrize("length, expected_ok", [
    (50, True),     # 邊界：剛好 50 字
    (51, False),    # 邊界：多 1 字
    (55, False),
])
def test_description_length(db, length, expected_ok):
    assert service.report_found(db, "水壺", "教室", "藍" * length)["ok"] is expected_ok


def test_claim_limit_per_person(sample_db):
    assert service.claim(sample_db, 1, "王小明")["ok"] is True
    assert service.claim(sample_db, 2, "王小明")["ok"] is True
    assert service.claim(sample_db, 3, "王小明")["ok"] is False


@pytest.mark.parametrize("claimer", ["", "   ", None])
def test_claim_requires_name(sample_db, claimer):
    assert service.claim(sample_db, 1, claimer)["ok"] is False


def test_search_requires_condition(sample_db):
    assert service.search(sample_db)["ok"] is False


def test_handle_message_search_by_location_only(sample_db, fake_ai):
    ask = fake_ai({"有人在餐廳撿到東西嗎": "查詢|未知|餐廳"})
    result = service.handle_message(sample_db, "有人在餐廳撿到東西嗎", "", ask)
    assert result["ok"] is True
    assert [it["id"] for it in result["data"]["items"]] == [2]
