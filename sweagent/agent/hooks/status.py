from collections.abc import Callable

from sweagent.agent.hooks.abstract import AbstractAgentHook
from sweagent.types import AgentInfo, StepOutput


class SetStatusAgentHook(AbstractAgentHook):
    def __init__(self, id: str, callable: Callable[[str, str], None]):
        self._callable = callable
        self._id = id
        self._i_step = 0
        self._cost = 0.0

    def _update(self, message: str):
        self._callable(self._id, message)

    def on_step_start(self):
        self._i_step += 1
        self._update(f"Step {self._i_step:>3} (${self._cost:.2f})")

    def on_step_done(self, *, step: StepOutput, info: AgentInfo):
        self._cost = info["model_stats"]["instance_cost"]  # type: ignore

    def on_tools_installation_started(self):
        self._update("Installing tools")