### `bot.py`
```python
from botbuilder.core import ActivityHandler, TurnContext
from botbuilder.schema import ActivityTypes
from jira_integration import post_to_jira
from datetime import datetime

user_sessions = {}

class TeamsStandupBot(ActivityHandler):
    async def on_message_activity(self, turn_context: TurnContext):
        user_id = turn_context.activity.from_property.id
        user_name = turn_context.activity.from_property.name
        text = turn_context.activity.text.strip()

        if user_id not in user_sessions:
            user_sessions[user_id] = {"step": 0, "answers": {}}

        session = user_sessions[user_id]
        step = session["step"]

        if step == 0:
            session["answers"]["yesterday"] = text
            session["step"] += 1
            await turn_context.send_activity("What will you do today?")
        elif step == 1:
            session["answers"]["today"] = text
            session["step"] += 1
            await turn_context.send_activity("Are there any blockers?")
        elif step == 2:
            session["answers"]["blockers"] = text
            await turn_context.send_activity("Thanks! Updating JIRA...")
            await post_to_jira(user_name, session["answers"])
            del user_sessions[user_id]
```