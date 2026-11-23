"""0D（加分題 A）：整合測試。從「一句話」經過假 AI，一路測到資料庫。

上面是老師的範例；請加上你的測試。
"""
import service


# ---------------- 範例（老師提供）----------------
def test_register_by_sentence(db, fake_ai):
    ask = fake_ai({"我在餐廳撿到一張學生證": "登記|學生證|餐廳"})
    result = service.handle_message(db, "我在餐廳撿到一張學生證", "", ask)
    assert result["ok"] is True


# ---------------- 請從這裡開始加 ----------------
def test_search_after_register(db, fake_ai):
    ask = fake_ai({"我在餐廳撿到一張學生證": "登記|學生證|餐廳",
                   "有人撿到學生證嗎": "查詢|學生證|未知"})
    service.handle_message(db, "我在餐廳撿到一張學生證", "", ask)
    result = service.handle_message(db, "有人撿到學生證嗎", "", ask)
    assert len(result["data"]["items"]) == 1


def test_claim_by_sentence(sample_db, fake_ai):
    ask = fake_ai({"我要認領 2 號": "認領|未知|未知"})
    assert service.handle_message(sample_db, "我要認領 2 號", "王小明", ask)["ok"] is True
    assert service.handle_message(sample_db, "我要認領 2 號", "李小華", ask)["ok"] is False


def test_unrelated_sentence(db, fake_ai):
    ask = fake_ai({"幫我推薦晚餐": "未知|未知|未知"})
    assert service.handle_message(db, "幫我推薦晚餐", "", ask)["ok"] is False


def test_ai_no_reply(db, fake_ai):
    ask = fake_ai({})
    assert service.handle_message(db, "表上沒有的句子", "", ask)["ok"] is False


def test_empty_input(db, fake_ai):
    assert service.handle_message(db, "   ", "", fake_ai({}))["ok"] is False
