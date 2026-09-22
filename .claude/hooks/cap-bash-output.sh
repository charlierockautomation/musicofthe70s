#!/usr/bin/env bash
# PreToolUse hook (matcher: Bash). Rewrites known-noisy commands (git log/diff,
# verify_post.py, generate_blog_hub_cards.py, npm/pytest test-build runs) so only
# a capped tail lands in the model's context. Full output still goes to disk under
# .claude/bash-logs/, nothing is silently discarded. Uses python3, not jq (jq is
# not installed on this machine).
set -euo pipefail
exec python3 "$(dirname "${BASH_SOURCE[0]}")/cap-bash-output.py"
