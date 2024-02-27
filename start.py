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
from router import Fetcher

fetcher = Fetcher()

if __name__ == "__main__":
    fetcher.run()
