"""Process build data.

Build data contains the latest build for each repository.
"""

from collections import deque
from typing import Deque, List

from app.models import Build, Pipeline


def get_latest_builds(pipelines: List[Pipeline]) -> List[Build]:
    """Get the latest builds for each pipelines."""
    builds_queue: Deque[Build] = deque([])

    def get_latest_build(builds: List[Build]) -> Build:
        """
        Get the latest build from a list of builds.

        constraint: len(builds) > 0.
        """
        latest = builds[0]
        for build in builds:
            if build.end_time > latest.end_time:
                latest = build
        return latest

    for pipe in pipelines:
        if len(pipe.builds) > 0:
            builds_queue.append(get_latest_build(pipe.builds))
    return list(builds_queue)
