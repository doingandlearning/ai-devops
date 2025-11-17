#!/usr/bin/env bash
set -euo pipefail
: "${LOG:=build.log}"

LC_ALL=C grep -nE 'error|fatal|failed' "$LOG" | tee /tmp/errors.txt

echo -e "\n=== Error Count Summary ==="
awk -F: '
/error/ {comp++}
/ld: cannot find/ {link_missing++}
/undefined reference/ {link_undef++}
END {
  printf "Compilation errors: %d\n", comp+0
  printf "Linker errors - missing library: %d\n", link_missing+0
  printf "Linker errors - undefined reference: %d\n", link_undef+0
  printf "Total error lines: %d\n", NR+0
}' /tmp/errors.txt
