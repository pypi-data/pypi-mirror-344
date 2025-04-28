import re
from typing import List

from duowen_agent.llm import tokenizer
from duowen_agent.rag.models import Document
from .base import BaseChunk

BULLET_PATTERN = {
    # 中文法律条款结构（编/章/节/条 + 括号条款）
    "chinese_legal": [
        r"\*{0,2}?第[零一二三四五六七八九十百0-9]+(分?编|部分)",
        r"\*{0,2}?第[零一二三四五六七八九十百0-9]+章",
        r"\*{0,2}?第[零一二三四五六七八九十百0-9]+节",
        r"\*{0,2}?第[零一二三四五六七八九十百0-9]+条",
        r"\*{0,2}?[$（][零一二三四五六七八九十百]+[$）]",
    ],
    # 数字多级编号体系（数字章节/多级标号）
    "numeric_outline": [
        r"\*{0,2}?第[0-9]+章",
        r"\*{0,2}?第[0-9]+节",
        r"\*{0,2}?[0-9]{,2}[\. 、]",
        r"\*{0,2}?[0-9]{,2}\.[0-9]{,2}[^a-zA-Z/%~-]",
        r"\*{0,2}?[0-9]{,2}\.[0-9]{,2}\.[0-9]{,2}",
        r"\*{0,2}?[0-9]{,2}\.[0-9]{,2}\.[0-9]{,2}\.[0-9]{,2}",
    ],
    # 中文混合型条款（含中文数字的嵌套结构）
    "chinese_mixed": [
        r"\*{0,2}?第[零一二三四五六七八九十百0-9]+章",
        r"\*{0,2}?第[零一二三四五六七八九十百0-9]+节",
        r"\*{0,2}?[零一二三四五六七八九十百]+[ 、]",
        r"\*{0,2}?[$（][零一二三四五六七八九十百]+[$）]",
        r"\*{0,2}?[$（][0-9]{,2}[$）]",
    ],
    # 英文法律条款（PART/Chapter/Section等）
    "english_legal": [
        r"\*{0,2}?PART (ONE|TWO|THREE|FOUR|FIVE|SIX|SEVEN|EIGHT|NINE|TEN)",
        r"\*{0,2}?Chapter (I+V?|VI*|XI|IX|X)",
        r"\*{0,2}?Section [0-9]+",
        r"\*{0,2}?Article [0-9]+",
    ],
}


def is_bullet_document(text, threshold=0.1):
    """
    判断文档是否属于条款类结构
    :param text: 输入文本
    :param threshold: 匹配比例阈值（默认5%）
    :return: True/False 及匹配详情
    """
    total_lines = len(text.split("\n"))

    def _structured(bullet_type, text):
        match_count = 0

        # 合并所有正则模式
        all_patterns = [re.compile(p) for p in BULLET_PATTERN[bullet_type]]

        # 逐行检测
        for line in text.split("\n"):
            line = line.strip()
            if not line:
                continue

            # 判断是否匹配条款模式
            for pattern in all_patterns:
                if pattern.search(line):
                    match_count += 1
                    break  # 避免重复计数

        # 计算匹配比例
        match_ratio = match_count / total_lines if total_lines > 0 else 0
        return {
            "bullet_type": bullet_type,
            "match_ratio": match_ratio,
            "matched_lines": match_count,
            "total_lines": total_lines,
        }

    data_list = []
    for i in BULLET_PATTERN:
        data_list.append(_structured(i, text))

    data = {}
    for x in data_list:
        if x["match_ratio"] > threshold:
            data = x
            break

    if not data:
        data = max(data_list, key=lambda x: x["match_ratio"])

    data["is_structured"] = data["match_ratio"] > threshold

    return data


class BulletChunker(BaseChunk):
    def __init__(self, chunk_size: int = 512):
        self.chunk_size = chunk_size

    def chunk(self, text: str) -> List[Document]:

        _chk = is_bullet_document(text)
        if _chk["is_structured"] is False:
            return [
                Document(
                    page_content=text,
                    metadata=dict(
                        token_count=tokenizer.emb_len(text),
                        chunk_index=0,
                        is_structured=False,
                    ),
                )
            ]

        _doc = []

        rule_pattern = BULLET_PATTERN[_chk["bullet_type"]]

        def _split_by_chapters_verbose(text: str, pattern: str) -> list[str]:
            chapters = []

            # 获取所有章节位置
            matches = list(re.finditer(pattern, text))
            if not matches:
                return [text]

            # 处理每个章节块
            for i, match in enumerate(matches):
                start = match.start()
                end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
                content = text[start:end].strip()
                chapters.append(content)

            # 处理首段无标题内容
            if matches:
                first_start = matches[0].start()
                if first_start > 0:
                    chapters.insert(0, text[0:first_start])

            return chapters

        def _chunk(text, level):

            _data = _split_by_chapters_verbose(text, rule_pattern[level])

            _current_doc = []

            for i in _data:

                if tokenizer.emb_len(i) > self.chunk_size:

                    if _current_doc:
                        _doc.append("\n\n".join(_current_doc))
                        _current_doc = []

                    if (level + 1) < len(rule_pattern):
                        _chunk(i, level + 1)
                    else:
                        _current_doc.append(i)
                else:
                    _merge_str = "\n\n".join(_current_doc + [i])
                    if tokenizer.emb_len(_merge_str) <= self.chunk_size:
                        _current_doc.append(i)
                    else:
                        _doc.append("\n\n".join(_current_doc))
                        _current_doc = []
                        _current_doc.append(i)

            _doc.append("\n\n".join(_current_doc))
            _current_doc = []

        _chunk(text, 0)

        return [
            Document(
                page_content=i,
                metadata=dict(token_count=tokenizer.emb_len(i), chunk_index=idx),
            )
            for idx, i in enumerate(_doc)
            if len(i.strip()) > 0
        ]
