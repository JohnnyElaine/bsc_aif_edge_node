from dataclasses import dataclass

from packages.enums import ComputeLoad
from packages.enums import ComputeType
from packages.enums import ComputeType
from worker.enums.work_source import WorkSource


@dataclass
class PullStreamConfig:
    fps: int
    resolution: tuple[int, int]
    compute_type: ComputeType
    compute_load: ComputeLoad
    stream_source: WorkSource

