import requests

URL = "https://www.dcard.tw/_api/forums"
response = requests.get(URL)
response.raise_for_status()

data = response.json()

# 設定 top 5 看板資料格式，存成json或list，維持最多只有5個欄位
# [{item1}, {item2}, {item3}, {item4}, {item5}]

top_5 = []
for kanban in data:
    if len(top_5) < 5:
        top_5.append(kanban)
    for item in top_5:
        # 每一筆資料，只要追蹤數有大於top_5 list裡面的其中之一，更新top_5 list:
        # 找出top_5裡面subscriptionCount最小的把他踢掉
        if kanban['subscriptionCount'] > item['subscriptionCount']:
            least_count = item['subscriptionCount']
            for item_ in top_5:
                if item_['subscriptionCount'] < least_count:
                    least_count = item['subscriptionCount']
            for item_ in top_5:
                if item_['subscriptionCount'] == least_count:
                    top_5.remove(item)
            # 把這筆資料加進top_5 list，break跳出迴圈
            top_5.append(kanban)
            break

# 依照訂閱數排序
top_5.sort(key=lambda item: item.get('subscriptionCount'), reverse=True)
# 依序列出看板名稱及訂閱數
i = 1
for item in top_5:
    print(f"{i}. {item['name']}/{item['alias']}： {item['subscriptionCount']}訂閱")
    i += 1
