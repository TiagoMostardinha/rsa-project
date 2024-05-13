from dataclasses import dataclass

@dataclass
class Message:
    content: str
    source: str

    def __str__(self):
        return f'{self.content}'


@dataclass
class ErrorMessage(Message):
    errorVar: str
    errorCode: int

    def __str__(self):
        return f'({self.errorVar} {self.errorCode}) {self.content}'
