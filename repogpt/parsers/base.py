from abc import ABC, abstractmethod
from typing import List


class Parser(ABC):

    @staticmethod
    @abstractmethod
    def get_file_summary(file_contents: str, file_name: str = None) -> List[str]:
        """Given some file contents"""
