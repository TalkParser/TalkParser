import multiprocessing
import re
from time import time

# 정규표현식을 함수 외부에서 컴파일
pattern = re.compile(
    pattern=r"\n\d{4}년 \d{1,2}월 \d{1,2}일 오[전후] \d{1,2}:\d{1,2}\n"
)
date_pattern = re.compile(
    pattern=r"(\d{4}년 \d{1,2}월 \d{1,2}일 오[전후] \d{1,2}:\d{1,2}), "
)

event_pattern = re.compile(pattern=r"(.+?)이 .+?님에서 (.+?)님으로 (.|\n)+")
delete_pattern = re.compile("(채팅방 관리자)가 (메시지를 가렸습니다.)")


def test(data: str):
    data = pattern.split(data)
    data = event_pattern.sub(r"\2님이 \1이 되었습니다.", data)
    data = delete_pattern.sub(r"\1님이 \2 : ", data)

    return date_pattern.split(data)


if __name__ == "__main__":
    with open(
        "tests/data/KakaoTalkChatsLarge.txt", mode="r", encoding="utf-8"
    ) as f:
        text = f.read()

    # CPU 카운트 확인
    cpu_count = min(4, len(text))

    # 단일 for 루프 테스트
    start = time()
    output = [test(i) for i in text]
    end = time()
    print(f"for loop: {end - start}")

    # 멀티프로세싱 Pool 사용
    start = time()
    with multiprocessing.Pool(processes=cpu_count) as pool:
        output = pool.map(test, text)
    end = time()
    print(f"multiprocessing Pool: {end - start}")
