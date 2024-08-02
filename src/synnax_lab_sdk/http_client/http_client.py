from abc import ABC, abstractmethod
from typing import Dict


class HttpClient(ABC):

    @abstractmethod
    def post(self, endpoint: str, body: Dict, headers: Dict) -> Dict: ...
