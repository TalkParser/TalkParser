""" Process chunks of chat messages based on date/timestamp for efficient parsing """

import re

DATE_PATTERN = re.compile(
    r"\d{4}년 \d{1,2}월 \d{1,2}일 오[전후] \d{1,2}:\d{1,2}\n"
)


def process_chunk(chat_text: str):
    return DATE_PATTERN.split(chat_text)


if __name__ == "__main__":
    import time

    start_time = time.time()
    with open(
        "tests/data/KakaoTalkChatsLarge.txt", "r", encoding="utf-8"
    ) as f:
        chat_text = f.read()
    result = process_chunk(chat_text)
    end_time = time.time()

    print(f"처리 시간: {end_time - start_time:.2f}초")
    print(f"분할된 청크 수: {len(result)}")
