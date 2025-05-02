import os
from subprocess import CalledProcessError

import dony


@dony.command()
def release(
    # version: str = lambda: dony.select(
    #     "Choose version",
    #     choices=[
    #         "patch",
    #         "minor",
    #         "major",
    #         "none",
    #     ],
    #     fuzzy=True,
    # ),
    uv_publish_token: str = lambda: dony.input(
        "Enter UV publish token (usually a PyPI token)",
        default=os.getenv("UV_PUBLISH_TOKEN") or "",
    ),
):
    print(os.getenv("UV_PUBLISH_TOKEN"))

    # - Validate git status

    #     try:
    #         dony.shell("""
    #
    #             # - Exit if there are staged changes
    #
    #             git diff --cached --name-only | grep -q . && { echo "There are staged changes. Exiting"; exit 1; }
    #
    #             # - Exit if not on main branch
    #
    #             git branch --show-current | grep -q main || { echo "Not on main branch. Exiting"; exit 1; }
    #
    #             # - Exit if there are unpulled commits
    #
    #             git fetch origin && git diff --quiet HEAD origin/main ||  { echo "There are some unpulled commits. Exiting"; exit 1; }
    # """)
    #     except CalledProcessError:
    #         return

    # - Bump

    # if version != "none":
    #     dony.shell(
    #         f"""
    #
    #             # - Bump
    #
    #             VERSION=$(uv version --bump {version} --short)
    #             echo $VERSION
    #
    #             # - Commit, tag and push
    #
    #             git add pyproject.toml
    #             git commit --message "chore: release-$VERSION"
    #             git tag --annotate "release-$VERSION" --message "chore: release-$VERSION" HEAD
    #             git push
    #             git push origin "release-$VERSION" # push tag to origin,
    #             """
    #     )

    # - Build and publish

    dony.shell(
        f"""
        uv build
        UV_PUBLISH_TOKEN={uv_publish_token} uv publish
        """
    )


if __name__ == "__main__":
    release()
