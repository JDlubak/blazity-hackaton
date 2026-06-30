# Lessons

Proven, non-obvious pitfalls. Append only when something has actually bitten us.

## Atlas skill symlinks need elevation on Windows

The `.claude/skills`, `.agents/skills`, and `.cursor/skills` entries are meant to
be symlinks pointing at `.ai/skills`. On Windows, creating a symlink requires
Administrator rights or Developer Mode; without either, `doctor --fix` fails with
`EPERM`, and a non-elevated shell can only create a junction — which `doctor`
does not accept as a valid skill link.

Fix: enable Developer Mode (Settings → For developers) or open an elevated
terminal, then run `npx --yes @blazity-atlas/core@latest doctor --fix`.

Never remove a leftover junction with `Remove-Item -Recurse`: it can follow the
link and delete the real `.ai/skills` contents. Use `cmd /c rmdir <path>` to
remove just the link.
