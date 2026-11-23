"""0C 負責：AI 解讀層（ai_parser.py）的測試。

這一層不呼叫真的 AI：直接把「AI 可能的回覆」交給 parse_reply()，檢查整理出來的欄位。
上面兩個是老師的範例；請在「第一輪」「第二輪」下面加上你的測試。
"""
import pytest

import ai_parser


# ---------------- 範例（老師提供）----------------
def test_parse_standard_reply():
    result = ai_parser.parse_reply("登記|雨傘|圖書館", "我在圖書館撿到一把傘")
    assert result["action"] == "登記"
    assert result["category"] == "雨傘"


@pytest.mark.parametrize("reply, user_text, field, expected", [
    ("", "隨便說說", "action", "未知"),          # AI 沒回覆
])
def test_parse_reply_fields(reply, user_text, field, expected):
    assert ai_parser.parse_reply(reply, user_text)[field] == expected


# ---------------- 第一輪：請從這裡開始加 ----------------
@pytest.mark.parametrize("reply, user_text, field, expected", [
    ("【登記】|【雨傘】|圖書館。", "我在圖書館撿到傘", "action", "登記"),   # AI 多了符號
    ("認領|未知|未知", "我要認領 3 號", "item_id", 3),                   # 編號從原話抓
    ("查詢|耳機|教室", "我在教室掉了耳機", "category", "耳機"),
    ("查詢|耳機|月球", "我在月球掉了耳機", "location", "未知"),           # 地點不在清單
])
def test_parse_reply_round1(reply, user_text, field, expected):
    assert ai_parser.parse_reply(reply, user_text)[field] == expected



# ---------------- 第二輪：邊界與錯誤情況 ----------------
