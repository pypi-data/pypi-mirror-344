from abc import ABC, abstractmethod
from typing import Any

from ..models import Document


class BaseVector(ABC):

    @abstractmethod
    def get_backend_type(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def semantic_search(self, query: str, **kwargs: Any) -> list[Document]:
        raise NotImplementedError

    @abstractmethod
    def full_text_search(self, query: str, **kwargs: Any) -> list[Document]:
        raise NotImplementedError

    @abstractmethod
    def hybrid_search(self, query: str, **kwargs: Any) -> list[Document]:
        raise NotImplementedError

    @abstractmethod
    def add_document(self, document: Document):
        raise NotImplementedError

    @abstractmethod
    def batch_add_document(self, documents: list[Document], batch_num: int):
        raise NotImplementedError

    @abstractmethod
    def get_documents_by_ids(self, ids: list[str], size=1000):
        raise NotImplementedError

    @abstractmethod
    def delete_collection(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def create_collection(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_collection_name(self):
        raise NotImplementedError
