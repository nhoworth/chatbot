### `main.py`
```python
import os
from aiohttp import web
from botbuilder.core import BotFrameworkAdapterSettings, BotFrameworkAdapter, TurnContext
from botbuilder.schema import Activity
from bot import TeamsStandupBot
from dotenv import load_dotenv

load_dotenv()

APP_ID = os.getenv("MICROSOFT_APP_ID")
APP_PASSWORD = os.getenv("MICROSOFT_APP_PASSWORD")

adapter_settings = BotFrameworkAdapterSettings(APP_ID, APP_PASSWORD)
adapter = BotFrameworkAdapter(adapter_settings)
bot = TeamsStandupBot()

async def messages(req):
    body = await req.json()
    activity = Activity().deserialize(body)
    auth_header = req.headers.get("Authorization", "")

    async def aux_func(turn_context: TurnContext):
        await bot.on_turn(turn_context)

    await adapter.process_activity(activity, auth_header, aux_func)
    return web.Response(status=200)

app = web.Application()
app.router.add_post("/api/messages", messages)

if __name__ == "__main__":
    web.run_app(app, port=3978)
```