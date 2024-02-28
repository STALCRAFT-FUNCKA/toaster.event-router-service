"""Service "toaster.event-routing-service".
About:
    A service that listening to VKontakte longpolling server,
    receives events from it, and then forms them
    custom events, sending json data through the client socket
    about the event to other processing services.
    
Author:
    Oidaho (Ruslan Bashinskii)
    oidahomain@gmail.com
"""
import asyncio
from fetcher import Fetcher


async def main():
    """Entry point.
    """
    fetcher = Fetcher()
    fetcher.run()



if __name__ == "__main__":
    asyncio.run(main())
