import codecs
import orjson
from notify.models import TeamsCard, TeamsChannel
from notify.providers.teams import Teams
from notify.conf import MS_TEAMS_DEFAULT_TEAMS_ID, MS_TEAMS_DEFAULT_CHANNEL_ID
from ...utils.json import json_encoder
from ...interfaces.env import EnvSupport
from .abstract import AbstractEvent


class TeamsMessage(AbstractEvent):
    def __init__(self, *args, **kwargs):
        super(TeamsMessage, self).__init__(*args, **kwargs)
        self.channel = kwargs.get('channel', MS_TEAMS_DEFAULT_CHANNEL_ID)
        self.team_id = kwargs.get('team_id', MS_TEAMS_DEFAULT_TEAMS_ID)
        self.channel_name = kwargs.get('channel_name', 'General')

    async def __call__(self, *args, **kwargs):
        tm = Teams(
            as_user=True,
            team_id=self.team_id,
        )
        channel = TeamsChannel(
            name=self.channel_name,
            team_id=self.team_id,
            channel_id=self.channel,
        )
        status = kwargs.pop("status", "done")
        task = kwargs.pop("task", None)
        program = task.getProgram()
        task_name = f"{program}.{task.taskname}"
        task_id = task.task_id
        message = kwargs.pop("message", f"Task Completed {task_name}, {task_id}")
        try:
            stat = task.stats  # getting the stat object:
            stats = stat.to_json()
        except AttributeError:
            stats = []
        if status == "done":
            icon = "✅"
        elif status in ("error", "failed", "exception", "task error"):
            icon = "🛑"
        elif status in (
            "warning",
            "file_not_found",
            "not_found",
            "data_not_found",
            "done_warning",
        ):
            icon = "⚠️"
        elif status in ("empty_file"):
            icon = "📄"
        else:
            icon = "✅"
        txt = f"{icon} {message}"
        if self.type == "card":
            msg = TeamsCard(
                title=f"Task {task_name} uid:{task_id}",
                text=txt,
                summary=f"Task Summary: {task_name}",
            )
            if hasattr(self, "with_stats"):
                # iterate over task stats:
                for stat, value in stats["steps"].items():
                    section = msg.addSection(activityTitle=stat, text=stat)
                    stats_json = orjson.dumps(value, option=orjson.OPT_INDENT_2 | orjson.OPT_APPEND_NEWLINE).decode()
                    section.addFacts(
                        facts=[{"name": stat, "value": stats_json}]
                    )
            if hasattr(self, 'with_codereview'):
                # Add Code Review
                section = msg.addSection(activityTitle="Code Review", text="Code Review")
                codereview = codecs.decode(json_encoder(stats['Review']), 'unicode_escape')
                section.addFacts(
                    facts=[{"name": "Code Review", "value": codereview}]
                )
        async with tm as conn:
            return await conn.send(
                recipient=channel,
                message=msg
            )
