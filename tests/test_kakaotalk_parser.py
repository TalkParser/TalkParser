from time import time
from unittest import TestCase

from talkparser.kakaotalk_parser import KakaoTalkChatData


class KakaoTalkParserTest(TestCase):
    def test_large_process_time(self):
        start = time()
        KakaoTalkChatData(
            path="tests/data/KakaoTalkChatsLarge.txt",
            bot_used=True,
            not_user=["", "방장봇", "채팅방 관리자"],
        )
        print(time() - start)

    def test_middle_process_time(self):
        start = time()
        KakaoTalkChatData(
            path="tests/data/KakaoTalkChatsMiddle.txt",
            bot_used=True,
            not_user=["", "방장봇", "채팅방 관리자"],
        )
        print(time() - start)

    def test_small_process_time(self):
        start = time()
        KakaoTalkChatData(
            path="tests/data/KakaoTalkChatsSmall.txt",
            bot_used=True,
            not_user=["", "방장봇", "채팅방 관리자"],
        )
        print(time() - start)
