# Stormworkspy

This repository contains the Stormworkspy library and workflow files for building
and publishing the package using Docker.

## Publishing

The workflow `publish.yml` builds the package entirely inside a Docker container
defined by `Dockerfile`. When manually triggered from the Actions tab it:

1. Builds the Docker image.
2. Runs the container to build the package and upload it to GitHub Packages.
3. Creates a GitHub release that includes the built distribution files.

### Security and secrets

The container authenticates to GitHub Packages using the built‑in
`GITHUB_TOKEN`. No personal tokens are stored in the repository.
Ensure `GITHUB_TOKEN` has `packages: write` permission (enabled by default).

To trigger the workflow, navigate to **Actions > Build and publish** and click
**Run workflow**. The package artifacts can be found in the created release.
