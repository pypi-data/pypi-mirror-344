import enum
import os
import subprocess

import semver


def get_latest_tag():
    result = subprocess.run(
        ["git", "describe", "--tags", "--abbrev=0", "--match", "*-preview"],
        capture_output=True,
        check=True,
    )
    return result.stdout.decode().strip()


class BumpType(enum.Enum):
    MAJOR = enum.auto()
    MINOR = enum.auto()
    PATCH = enum.auto()


def detect_bump_type() -> BumpType:
    log = subprocess.check_output(
        ["git", "log", "--pretty=format:%s", "origin/main..HEAD"]
    ).decode()
    bump = BumpType.PATCH
    for line in log.splitlines():
        if line.upper().startswith("BREAKING CHANGE:") or line.lower().startswith("feat!:"):
            return BumpType.MAJOR
        elif line.lower().startswith("feat:"):
            return BumpType.MINOR
    return bump


def get_next_tag():
    current_version = get_latest_tag().lstrip('v').rstrip('-preview')
    bump_type = detect_bump_type()

    version = semver.Version.parse(current_version)

    match bump_type:
        case BumpType.PATCH:
            new_version = version.bump_patch()
        case BumpType.MINOR:
            new_version = version.bump_minor()
        case BumpType.MAJOR:
            new_version = version.bump_major()
        case _:
            raise Exception(f"Unexpected bump type: {bump_type}")
    result = f"v{new_version}"
    if os.getenv("CI_COMMIT_BRANCH") != "develop":
        result = f"{result}-preview"
    return result


if __name__ == "__main__":
    print(get_next_tag())
