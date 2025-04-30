from abc import ABC, abstractmethod
import tiktoken


class BaseTokenizer(ABC):
    @abstractmethod
    def count_tokens(self, text: str):
        pass


class OpenAiTokenizer(BaseTokenizer):
    def __init__(self, model_name):
        self.__tokenizer = tiktoken.encoding_for_model(model_name)

    def count_tokens(self, text: str):
        return len(self.__tokenizer.encode(text))
