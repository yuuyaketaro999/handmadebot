import os
import random
import csv
import tweepy

# 時間帯ごとのカテゴリ範囲（tweets.csvの行インデックス）
# 朝: ①No.001-017 + ②No.018-034 → 行0-33
# 昼: ③No.035-051 + ④No.052-068 → 行34-67
# 夜: ⑤No.069-084 + ⑥No.085-100 → 行68-99
SLOTS = {
    "morning": (0, 34),
    "noon":    (34, 68),
    "night":   (68, 100),
}


def post_tweet():
    client = tweepy.Client(
        consumer_key=os.environ["X_API_KEY"],
        consumer_secret=os.environ["X_API_KEY_SECRET"],
        access_token=os.environ["X_ACCESS_TOKEN"],
        access_token_secret=os.environ["X_ACCESS_TOKEN_SECRET"],
    )

    tweets = []
    with open("tweets.csv", "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            if row and row[0].strip():
                tweets.append(row[0].strip())

    slot = os.environ.get("TIME_SLOT", "morning")
    start, end = SLOTS.get(slot, (0, len(tweets)))
    candidates = tweets[start:end]

    if not candidates:
        print("ツイートが見つかりません")
        return

    tweet = random.choice(candidates)
    response = client.create_tweet(text=tweet)
    print(f"[{slot}] 投稿成功 ID: {response.data['id']}")
    print(f"内容: {tweet[:80]}...")


if __name__ == "__main__":
    post_tweet()
