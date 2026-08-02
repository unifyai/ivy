#!/bin/bash -e
# Build the Ivy docs locally, mirroring what .github/workflows/publish-docs.yml does.
#
# This previously ran `docker run unifyai/doc-builder:latest`, but that image is
# no longer published, so the Docker path is gone. CI checks the doc-builder out
# and runs it directly instead, and so does this script.
#
# Any arguments are forwarded to make_docs_without_docker.sh (e.g. -s to skip
# reinstalling dependencies on repeat runs).

project_dir=$(cd "$(dirname "$0")/.." && pwd)
doc_builder_dir="$project_dir/.doc-builder"

if [ -d "$doc_builder_dir" ]; then
    git -C "$doc_builder_dir" pull --ff-only
else
    git clone --depth 1 https://github.com/unifyai/ivy-doc-builder.git "$doc_builder_dir"
fi

"$doc_builder_dir/make_docs_without_docker.sh" "$@" "$project_dir"
