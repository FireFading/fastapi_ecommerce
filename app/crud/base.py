from abc import abstractmethod


class CRUD:
    @abstractmethod
    async def get(self, *args):
        pass

    @abstractmethod
    async def create(self, *args):
        pass

    @abstractmethod
    async def update(self, *args):
        pass

    @abstractmethod
    async def delete(self, *args):
        pass
