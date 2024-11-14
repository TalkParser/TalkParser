import re

PATTERN = re.compile(
    r"(?P<date>\d{4}년 \d{1,2}월 \d{1,2}일 오[전후] \d{1,2}:\d{1,2}), (?P<name>.+) : (?P<message>[\s\S]+?)(?=\n\d{4}년 \d{1,2}월 \d{1,2}일 오[전후] \d{1,2}:\d{1,2})"
)


def parse_kakaotalk(chat_text: str):
    messages = []
    for chat_match in PATTERN.finditer(chat_text):
        date = chat_match.group("date")
        name = chat_match.group("name")
        message = chat_match.group("message")
        messages.append({"date": date, "name": name, "message": message})
    return messages


if __name__ == "__main__":
    import time

    with open(
        "tests/data/KakaoTalkChatsMiddle.txt",
        "r",
        encoding="utf-8",
    ) as f:
        text = f.read()
    start_time = time.time()
    result = parse_kakaotalk(text)
    end_time = time.time()
    print(f"파싱 소요 시간: {end_time - start_time:.8f}초")
    print(len(result))
    print(result[-1])
