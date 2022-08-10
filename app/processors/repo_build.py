"""Process build data.

Build data contains the latest build for each repository.
"""
from typing import Dict, List

from app.models import Build


def process_repo_build(builds: List[Build]) -> List[Build]:
    """Process builds into build data."""
    repo_url_to_builds: Dict[str, List[Build]] = {}
    for build in builds:
        repo_url = build.build_url.split("/-/")[0]
        repo_url_to_builds.setdefault(repo_url, []).append(build)
    return [value[0] for value in repo_url_to_builds.values()]
