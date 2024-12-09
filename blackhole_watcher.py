import asyncio
from watchfiles import awatch
from blackhole import on_created, getPath

class BlackholeHandler:
    def __init__(self, is_radarr):
        self.is_radarr = is_radarr
        self.path_name = getPath(is_radarr, create=True)

    async def watch(self):
        await on_created(self.is_radarr)
        async for changes in awatch(self.path_name):
            for change in changes:
                if change[0] in [1,2] and (change[1].lower().endswith((".torrent", ".magnet"))):
                    await on_created(self.is_radarr)

async def main():
    print("Watching blackhole")
    
    radarr_handler = BlackholeHandler(is_radarr=True)
    sonarr_handler = BlackholeHandler(is_radarr=False)

    await asyncio.gather(
        radarr_handler.watch(),
        sonarr_handler.watch()
    )

if __name__ == "__main__":
    asyncio.run(main())