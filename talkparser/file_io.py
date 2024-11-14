def read_chat_file(file_path: str):
    """
    채팅 파일을 한 줄씩 읽어오는 제너레이터 함수

    Args:
        file_path: 읽어올 채팅 파일 경로

    Yields:
        str: 파일에서 읽어온 한 줄의 텍스트
    """
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:  # 빈 줄 제외
                yield line


if __name__ == "__main__":
    count = 0
    for line in read_chat_file("tests/data/KakaoTalkChatsLarge.txt"):
        print(line)
        count += 1
        if count >= 4:
            break
