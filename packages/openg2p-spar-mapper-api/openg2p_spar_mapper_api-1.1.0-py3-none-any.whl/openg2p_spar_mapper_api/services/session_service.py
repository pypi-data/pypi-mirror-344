from openg2p_fastapi_common.context import dbengine
from openg2p_fastapi_common.service import BaseService
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker


class SessionInitializer(BaseService):
    def __init__(self):
        super().__init__("SessionInitializer")
        self.session_maker = None

    async def get_session_from_pool(self) -> AsyncSession:
        if not self.session_maker:
            self.session_maker = async_sessionmaker(
                dbengine.get(), expire_on_commit=False
            )

        async with self.session_maker() as session:
            return session
