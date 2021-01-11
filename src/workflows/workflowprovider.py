from __future__ import annotations

from dataclasses import dataclass

from src.workflows.load_atlas.workflow import LoadAtlasWorkflow
from src.workflows.load_section.workflow import LoadSectionWorkflow
from src.workflows.move_section.workflow import MoveSectionWorkflow
from src.workflows.select_channel.workflow import SelectChannelWorkflow


@dataclass
class WorkflowProvider:
    load_atlas: LoadAtlasWorkflow
    load_section: LoadSectionWorkflow
    select_channel: SelectChannelWorkflow
    move_section: MoveSectionWorkflow
