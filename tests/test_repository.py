"""0A 負責：資料存取層（repository.py）的測試。

上面兩個是老師的範例；請在「第一輪」「第二輪」下面加上你的測試。
提示：sample_db 裡有 1 號雨傘（圖書館）、2 號水壺（餐廳）、3 號雨傘（教室）。
"""
import pytest

import repository


# ---------------- 範例（老師提供）----------------
def test_add_item_returns_new_id(db):
    assert repository.add_item(db, "雨傘", "圖書館", "黑傘") == 1


def test_get_item_not_found_returns_none(db):
    assert repository.get_item(db, 99) is None


# ---------------- 第一輪：請從這裡開始加 ----------------
def test_get_item_fields(sample_db):
    item = repository.get_item(sample_db, 2)
    assert item["category"] == "水壺"
    assert item["location"] == "餐廳"
    assert item["status"] == "待認領"
    assert item["claimer"] is None


def test_find_items_by_category(sample_db):
    ids = [it["id"] for it in repository.find_items(sample_db, category="雨傘")]
    assert ids == [1, 3]


def test_mark_claimed_once(sample_db):
    assert repository.mark_claimed(sample_db, 1, "王小明") is True
    assert repository.get_item(sample_db, 1)["status"] == "已認領"



# ---------------- 第二輪：邊界與錯誤情況 ----------------
def test_mark_claimed_twice_fails(sample_db):
    repository.mark_claimed(sample_db, 1, "王小明")
    assert repository.mark_claimed(sample_db, 1, "李小華") is False


def test_find_items_excludes_claimed(sample_db):
    repository.mark_claimed(sample_db, 1, "王小明")
    ids = [it["id"] for it in repository.find_items(sample_db, category="雨傘")]
    assert ids == [3]


def test_find_items_by_category_and_location(sample_db):
    ids = [it["id"] for it in repository.find_items(sample_db, "雨傘", "教室")]
    assert ids == [3]


def test_count_claimed_by(sample_db):
    repository.mark_claimed(sample_db, 1, "王小明")
    repository.mark_claimed(sample_db, 2, "李小華")
    assert repository.count_claimed_by(sample_db, "王小明") == 1
    assert repository.count_claimed_by(sample_db, "陳大文") == 0


def test_stats_lists_category_without_items(sample_db):
    rows = {r["類別"]: r for r in repository.category_stats(sample_db)}
    assert rows["鑰匙"]["總件數"] == 0


@pytest.mark.parametrize("column, expected", [
    ("總件數", 2),
    ("待認領", 2),
    ("已認領", 0),
])
def test_stats_umbrella(sample_db, column, expected):
    rows = {r["類別"]: r for r in repository.category_stats(sample_db)}
    assert rows["雨傘"][column] == expected
