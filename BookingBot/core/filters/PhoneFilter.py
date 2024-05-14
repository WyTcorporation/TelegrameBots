from aiogram.filters import BaseFilter
from aiogram.types import Message


# Дивись нову документацію
class IsTrueContact(BaseFilter):
    is_contact: bool

    async def __call__(self, message: Message):
        try:
            self.is_contact = message.contact.user_id == message.from_user.id
        except:
            self.is_contact = False
        return self.is_contact
