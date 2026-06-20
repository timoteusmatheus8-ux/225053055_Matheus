import asyncio
import os

import flet as ft

from main import main

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")


async def run():
    port = int(os.environ.get("PORT", 8080))

    # Use FLET_APP_WEB view so Flet starts a pure web server without
    # attempting to launch a local browser window (which would crash in a
    # headless container environment).
    await ft.app_async(
        target=main,
        view=ft.AppView.FLET_APP_WEB,
        port=port,
        host="0.0.0.0",
        assets_dir=ASSETS_DIR,
    )

    # Keep the event loop alive indefinitely so the process does not exit
    # after ft.app_async returns (e.g. when the last client disconnects).
    await asyncio.Event().wait()


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(run())
    except KeyboardInterrupt:
        pass
    finally:
        loop.close()
