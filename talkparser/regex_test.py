import re
from typing import List, Dict, Optional
from multiprocessing import Pool
import os

# 날짜, 이름, 메시지를 하나의 패턴으로 통합
CHAT_PATTERN = re.compile(
    r"(\d{4}년 \d{1,2}월 \d{1,2}일 오[전후] \d{1,2}:\d{1,2}), "  # 날짜/시간 그룹
    r"(.+?)"  # 이름 그룹 (최소 매칭)
    r"(?:: (.+)|님이 들어왔습니다\.|님이 나갔습니다\.|님을 내보냈습니다\.|$)"  # 메시지 또는 시스템 메시지
)

# 이벤트 패턴들
EVENT_PATTERNS = [
    re.compile(r"방장이 .+님에서 .+님으로 변경되었습니다\."),
    re.compile(r"님이 들어왔습니다\.$"),
    re.compile(r"님이 나갔습니다\.$"),
    re.compile(r"님을 내보냈습니다\.$"),
]


def parse_line(line: str) -> Optional[Dict]:
    """
    채팅 라인을 파싱하여 구조화된 데이터로 반환

    Args:
        line: 파싱할 채팅 라인

    Returns:
        dict: 파싱된 결과를 담은 딕셔너리
        {
            'date': str,  # 날짜/시간
            'name': str,  # 발신자 이름
            'message': str,  # 메시지 내용
            'event': bool  # 이벤트 여부
        }
    """
    # CHAT_PATTERN으로 전체 매칭 시도
    chat_match = CHAT_PATTERN.match(line)
    if not chat_match:
        return None

    date, name, message = chat_match.groups()

    # 이벤트 여부 확인
    is_event = any(pattern.search(line) for pattern in EVENT_PATTERNS)

    # 메시지 처리
    if message is None:
        if is_event:
            # 부방장 이벤트 처리
            if "님이 부방장이 되었습니다" in line:
                name = name.replace("님이 부방장이 되었습니다", "")
                message = "부방장이 되었습니다."
            else:
                message = line.split(", ", 1)[1]  # 시스템 메시지 전체를 저장
        else:
            message = ""
    else:
        message = message.strip()

    return {
        "date": date.strip(),
        "name": name.strip(),
        "message": message,
        "event": is_event,
    }


def process_chunk(chunk: List[str]) -> List[Dict]:
    """
    청크 단위로 메시지를 처리하는 함수
    """
    chat_messages = []
    message_dict = {}
    message_lines = []

    for line in chunk:
        line = line.strip()
        if not line:
            continue

        parsed = parse_line(line)
        if parsed:
            if message_dict:
                message_dict["message"] = "\n".join(message_lines)
                chat_messages.append(message_dict.copy())

            message_dict = parsed
            message_lines = [parsed["message"]] if parsed["message"] else []
        else:
            if message_dict:
                message_lines.append(line)

    if message_dict:
        message_dict["message"] = "\n".join(message_lines)
        chat_messages.append(message_dict.copy())

    return chat_messages


def parse_chat_file(file_path: str) -> List[Dict]:
    """
    채팅 파일 전체를 병렬 처리하여 구조화된 데이터의 리스트로 반환

    Args:
        file_path: 파싱할 채팅 파일 경로

    Returns:
        List[Dict]: 파싱된 채팅 메시지들의 리스트
    """
    # 파일을 청크 단위로 나누기
    chunk_size = 5000  # 청크 크기 증가
    chunks = []
    current_chunk = []

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            current_chunk.append(line)
            if len(current_chunk) >= chunk_size:
                chunks.append(current_chunk)
                current_chunk = []
        if current_chunk:
            chunks.append(current_chunk)

    # 멀티프로세싱으로 청크 처리 (프로세스 수 증가)
    num_processes = min(16, os.cpu_count() or 1)  # 최대 16개 프로세스 사용
    with Pool(processes=num_processes) as pool:
        results = pool.map(process_chunk, chunks, chunksize=1)

    # 결과 합치기
    chat_messages = []
    for result in results:
        chat_messages.extend(result)

    return chat_messages


if __name__ == "__main__":
    import time

    start_time = time.time()
    chat_messages = parse_chat_file("tests/data/KakaoTalkChatsLarge.txt")
    end_time = time.time()

    print(f"파싱 소요 시간: {end_time - start_time:.2f}초")
    # 결과를 txt 파일로 저장
    output_file = "parsed_chat_results.txt"
    with open(output_file, "w", encoding="utf-8") as f:
        for message in chat_messages:
            # 각 메시지를 보기 좋게 포맷팅
            formatted_message = (
                f"날짜: {message['date']}\n"
                f"이름: {message['name']}\n"
                f"메시지: {message['message']}\n"
                f"이벤트 여부: {message['event']}\n"
                f"{'-'*50}\n"
            )
            f.write(formatted_message)
