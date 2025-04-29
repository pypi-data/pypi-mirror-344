import logging
from typing import Union, List

from duowen_agent.llm import tokenizer
from duowen_agent.rag.models import Document
from .base import BaseChunk
from .bullet import BulletChunker, is_bullet_document
from .markdown import MarkdownHeaderChunker
from .recursive import RecursiveChunker
from .regex import JinaTextChunker
from .separator import SeparatorChunker
from .word import WordChunker
from ..extractor.table import markdown_table_to_kv_list


class FastMixinChunker(BaseChunk):

    def __init__(
        self,
        chunk_size: int = 512,
        chunk_overlap: Union[int, float] = 80,
    ):
        self.chunk_size = chunk_size
        self.chunk_overlap = (
            chunk_overlap
            if isinstance(chunk_overlap, int)
            else int(chunk_overlap * chunk_size)
        )

    def chunk(self, text: str) -> List[Document]:
        """
        1. markdown切割
        2. regex切割(实验性质) 失败 降级 换行符切割
        3. 递归切割
        4. word切割（chunk_overlap 生效）
        """

        try:
            text = markdown_table_to_kv_list(text)
        except Exception as e:
            logging.warning(f"markdown_table_to_kv_list 识别异常: {text[:100]}...")

        slices = []
        data1 = MarkdownHeaderChunker(chunk_size=self.chunk_size).chunk(text)
        for _d1 in data1:
            if _d1.metadata.get("token_count") > self.chunk_size:

                if (
                    is_bullet_document(_d1.page_content) and len(data1) == 1
                ):  # 暂时不支持markdown文档混合切合
                    data2 = BulletChunker(chunk_size=self.chunk_size).chunk(
                        _d1.page_content
                    )
                else:
                    try:
                        data2 = JinaTextChunker(chunk_size=self.chunk_size).chunk(
                            _d1.page_content
                        )
                    except Exception as e:
                        data2 = SeparatorChunker(
                            chunk_size=self.chunk_size, chunk_overlap=0
                        ).chunk(_d1.page_content)

                for _d2 in data2:
                    if _d2.metadata.get("token_count") > self.chunk_size:
                        data3 = RecursiveChunker(chunk_size=self.chunk_size).chunk(
                            _d2.page_content
                        )
                        for _d3 in data3:
                            if _d3.metadata.get("token_count") > self.chunk_size:
                                data4 = WordChunker(
                                    chunk_size=self.chunk_size,
                                    chunk_overlap=self.chunk_overlap,
                                ).chunk(_d3.page_content)
                                for _d4 in data4:
                                    _d4.metadata = {**_d1.metadata, **_d4.metadata}
                                    slices.append(_d4)
                            else:
                                _d3.metadata = {**_d1.metadata, **_d3.metadata}
                                slices.append(_d3)
                    else:
                        _d2.metadata = {**_d1.metadata, **_d2.metadata}
                        slices.append(_d2)
            else:
                slices.append(_d1)

        _slices = []
        for idx, part in enumerate(slices):
            part.metadata["chunk_index"] = idx
            part.metadata["token_count"] = tokenizer.emb_len(
                part.page_content + part.metadata.get("header_str", "")
            )
            _slices.append(part)

        return _slices

    def __repr__(self) -> str:
        return (
            f"FastMixinChunker("
            f"chunk_size={self.chunk_size}, "
            f"chunk_overlap={self.chunk_overlap}"
        )
