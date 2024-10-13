from dataclasses import dataclass

@dataclass
class User:
    chat_id: int
    first_name: str
    username: str
    isSubscribed: bool
    isActive: bool

    @classmethod
    def from_chat_info(cls, chat):
        return cls(
            chat_id=chat.id,
            first_name=chat.first_name,
            username=chat.username,
            isSubscribed=False,
            isActive=False 
        )
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            chat_id=data['chat_id'],
            first_name=data['first_name'],
            username=data['username'],
            isSubscribed=data['isSubscribed'],
            isActive=data['isActive']
        )