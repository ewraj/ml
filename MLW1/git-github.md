# Git & GitHub — everything you need, in the order you need it

Written for this repo and this plan: solo work, one machine (Windows), a commit
every Sunday, and a GitHub profile that someone hiring you will actually open.

**The one book worth downloading:** *Pro Git* by Scott Chacon and Ben Straub — free,
official, and the whole PDF/EPUB is at **git-scm.com/book**. Chapters 1–3 and 7
cover everything below in more depth. Read Ch.10 ("Git Internals") once you are
comfortable; it makes the rest stop feeling arbitrary.

---

## 1. The mental model (read this once, properly)

Almost every confusing thing about git dissolves once these four ideas land.

**A commit is a full snapshot, not a diff.** Git stores the complete state of
every file at each commit (deduplicated by content, so this is cheaper than it
sounds). The diffs you see are *computed* on demand by comparing two snapshots.

**Every commit points at its parent.** That chain of parents is your history. A
commit's ID is a hash of its content *and* its parent, so a commit ID pins the
entire history behind it. Change anything in the past and every ID after it
changes — that is why rewriting history is disruptive.

**A branch is just a movable pointer to one commit.** Not a copy, not a folder
— a 41-byte file containing a hash. This is why branching is instant and why
you should branch freely. `HEAD` is a pointer to *which branch you are on*.

**There are three places a file lives:**

```
working tree  ──git add──>  staging area (index)  ──git commit──>  repository
 (your edits)                (what will go in)                      (history)
```

`git status` tells you which of the three each file disagrees with. Read its
output — it literally suggests the command you want.

---

## 2. One-time setup

```bash
git config --global user.name  "Raj"
git config --global user.email "rajrxo@gmail.com"

git config --global init.defaultBranch main
git config --global pull.rebase true        # linear history on pull
git config --global core.autocrlf true      # Windows: CRLF locally, LF in repo
git config --global core.editor "code --wait"   # or "notepad", or your editor
git config --global push.autoSetupRemote true   # first push needs no -u
```

Check anything with `git config --list --show-origin`.

**Authentication to GitHub.** Two options, pick one:

- **GitHub CLI (easiest).** Install `gh`, then `gh auth login` — it handles
  browser login and credential storage for you.
- **SSH keys.** `ssh-keygen -t ed25519 -C "rajrxo@gmail.com"`, then paste
  `~/.ssh/id_ed25519.pub` into GitHub -> Settings -> SSH and GPG keys. Test with
  `ssh -T git@github.com`.

Never type a password into a `git push` prompt — GitHub removed password auth
years ago. It wants a token, which is why you use `gh` or SSH instead.

---

## 3. The daily loop

This is 90% of your git usage. The other sections are for when something
unusual happens.

```bash
git status                  # what changed, what is staged
git diff                    # unstaged changes (working tree vs index)
git diff --staged           # staged changes (index vs last commit)
git add exercises/          # stage a path
git add -p                  # stage hunk by hunk — use this, it makes you re-read your diff
git commit -m "message"
git log --oneline --graph --decorate -10
git push
```

**`git add -p` is the habit worth building.** It walks you through your own
changes one hunk at a time (`y` stage, `n` skip, `s` split, `q` quit). You will
catch debug prints and commented-out code before they reach history.

### Committing at the right size
One commit = one coherent change you could describe in one line. For this plan,
that is roughly: one session's work, or one exercise function if it was a
struggle worth recording. Do not let a week pile into one commit called
"updates" — the Sunday commit should be the *last* of several, not the only one.

---

## 4. Commit messages

```
Vectorize pairwise_sq_dists with the expansion trick

Used ||x-y||^2 = ||x||^2 + ||y||^2 - 2x.y so the whole thing is one
matmul plus two broadcasts. The naive (n,m,d) version blew past 4GB on
the MNIST subset; this one allocates only the (n,m) result.
```

The rules that matter:
- **Subject line: imperative mood, under ~50 chars, no full stop.** "Add X",
  not "Added X" or "Adding X". It reads as an instruction to the codebase —
  "apply this commit and it will *add X*."
- Blank line, then the body wrapped at ~72 chars.
- **The body explains WHY, not what.** The diff already says what. Six months
  from now you will want the reasoning, and so will anyone reading the repo to
  decide whether to interview you.
- `git commit` with no `-m` opens the editor, which is how you write a real
  body. Get used to it.

---

## 5. `.gitignore`

Lives at the repo root; already set up in this repo. It matches paths, and it
only affects **untracked** files.

```
.venv/
__pycache__/
*.pyc
.pytest_cache/
.idea/
```

Patterns: `*.ext` any such file, `dir/` a directory, `/file` only at the root,
`!keep.txt` an exception, `**/x` at any depth.

**The trap:** adding a file to `.gitignore` does nothing if it is already
tracked. To stop tracking but keep it on disk:

```bash
git rm --cached -r .venv    # --cached = untrack only, do not delete
```

**Never commit:** virtualenvs, `__pycache__`, datasets, model weights, `.env`
files, API keys, anything over ~50 MB. MNIST goes in `.gitignore` and gets
downloaded by a script — the repo holds code, not data.

---

## 6. Branches

```bash
git switch -c knn-cosine       # create and move to a branch
git switch main                # go back
git branch                     # list
git branch -d knn-cosine       # delete (safe — refuses if unmerged)
git branch -D knn-cosine       # delete (force)
```

`switch` and `restore` are the modern, unambiguous replacements for the
overloaded `git checkout`. `checkout` still works everywhere and you will see it
in every tutorial; it does both jobs, which is exactly why it confuses people.

### Merging
```bash
git switch main
git merge knn-cosine
```
If the branches have not diverged, git **fast-forwards** — just slides the
pointer, no merge commit. If they have, you get a merge commit with two parents.

### Rebase
```bash
git switch knn-cosine
git rebase main        # replay my commits on top of main's tip
```
Rebase *rewrites* your commits (new IDs) so history stays linear. Merge
preserves what actually happened; rebase makes it read as if you worked in
order.

**The golden rule: never rebase commits you have already pushed somewhere
others pull from.** Working solo, rebase freely. It is your own history.

### Merge conflicts
Git marks the file and stops:
```
<<<<<<< HEAD
your version
=======
their version
>>>>>>> knn-cosine
```
Edit the file into what you actually want — **delete all three marker lines** —
then `git add <file>` and `git commit` (or `git rebase --continue`). Bail out
any time with `git merge --abort` / `git rebase --abort`. Nothing is lost; an
abort is always safe.

---

## 7. Remotes and GitHub

A **remote** is a named URL for another copy of the repo. `origin` is the
conventional name for "the one I cloned from / pushed to".

```bash
git remote -v                                   # list remotes
git remote add origin git@github.com:USER/ml.git
git push -u origin main                         # -u links the branches, once
git push
git pull                                        # = fetch + merge (or rebase, per your config)
git fetch                                       # download, change nothing locally — always safe
```

**`fetch` vs `pull`.** `fetch` updates your knowledge of the remote
(`origin/main` moves) and leaves your files alone. `pull` does that *and*
integrates it into your branch. When you are unsure what upstream did, `fetch`
then `git log HEAD..origin/main` to look before you leap.

`origin/main` is a **remote-tracking branch**: your local cache of where `main`
was on the server as of your last fetch. It only moves when you fetch, which is
why it can be stale.

### Starting this repo on GitHub

```bash
gh repo create ml --public --source=. --remote=origin --push
```

Or make an empty repo on github.com and `git remote add` it as above. **Do not**
let GitHub add a README or .gitignore at creation time when you already have
commits locally — you get two unrelated histories and an awkward first merge.
(If it happens: `git pull --allow-unrelated-histories`.)

---

## 8. Undo — the table you will actually come back to

Find your situation on the left.

| Situation | Command | Destroys work? |
|---|---|---|
| Edited a file, want the last committed version back | `git restore <file>` | **Yes**, that edit |
| Staged something by mistake | `git restore --staged <file>` | No |
| Last commit message is wrong | `git commit --amend` | No (rewrites the commit) |
| Forgot a file in the last commit | `git add <f>` then `git commit --amend --no-edit` | No |
| Undo the last commit, keep changes staged | `git reset --soft HEAD~1` | No |
| Undo the last commit, keep changes unstaged | `git reset HEAD~1` | No |
| Last commit gone entirely | `git reset --hard HEAD~1` | **Yes** |
| Undo a commit that is already pushed | `git revert <sha>` | No — adds an inverse commit |
| Need a file as it was 3 commits ago | `git restore --source=HEAD~3 <file>` | Overwrites current copy |
| "I have destroyed everything" | `git reflog` | No — this is the undo button |

**`--soft` / `--mixed` / `--hard`** map exactly onto the three trees from §1:
`--soft` moves only the branch pointer, `--mixed` (the default) also resets the
index, `--hard` also overwrites your working tree. Only `--hard` can lose work.

**`git reflog` is the safety net nobody mentions to beginners.** Git records
every position `HEAD` has held — including commits you "deleted" with a bad
reset or rebase. They survive for around 90 days:

```bash
git reflog                    # find the sha you want, e.g. abc1234
git reset --hard abc1234      # you are back
```

Anything **committed** is nearly impossible to truly lose. Anything **never
committed** is gone the moment you `--hard` or `restore` it. That asymmetry is
the whole argument for committing early and often.

### Pushed a secret

Rotate the key first — assume it is compromised the second it lands on GitHub,
because bots scrape public commits within minutes. Then scrub history with
`git filter-repo` (or the BFG), force-push, and treat the old key as dead.
Deleting the file in a *new* commit does nothing; it is still in history.

---

## 9. Stash — "I need to switch tasks right now"

```bash
git stash push -m "half-done cosine metric"
git stash list
git stash pop          # reapply the most recent and drop it
git stash apply        # reapply but keep it in the list
git stash drop
git stash -u           # include untracked files — the flag people forget
```

Uncommitted work goes on a shelf; your tree returns to the last commit. Useful,
but a stash is easy to forget about — for anything longer than an hour, a
scratch branch with a WIP commit is the better tool.

---

## 10. Tags

```bash
git tag -a w1 -m "Week 1 complete: numpy from the metal"
git push origin w1
```

A tag is a permanent pointer to one commit (a branch moves, a tag does not).
Tagging each week of this plan gives you `w1`, `w2`, ... and makes "show me
where I was ten weeks in" a single command.

---

## 11. The GitHub flow, and pull requests

Even solo, PRs are worth using occasionally — they give you a reviewable diff
and a place to write down what you did, and they are how every team you join
will work.

```bash
git switch -c feature/knn-weighted
# ... commits ...
git push
gh pr create --fill          # open the PR from the CLI
gh pr view --web
gh pr merge --squash         # squash = one tidy commit on main
gh pr checks                 # CI status
```

**Merge strategies:** *merge commit* keeps every commit plus a join; *squash*
flattens the branch into one commit (tidiest for small features); *rebase*
replays each commit onto main with no merge commit. Solo, squash is usually
right.

Other `gh` commands worth knowing: `gh repo clone`, `gh issue create`,
`gh repo view --web`, `gh run watch`.

---

## 12. Making GitHub work for hiring

This is the part the Tuesday Apply hour exists for. An unexplained repo is
invisible.

**Per repo:**

- A README that opens with *what this is and what it demonstrates*, in two
  sentences. For this repo: implemented from scratch, no sklearn, here is the
  math.
- **Explain the math, not the API.** Nobody is impressed by `knn.fit(X, y)`.
  They are impressed by the paragraph on why the distance expansion turns an
  `(n,m,d)` allocation into a single matmul.
- Show the result: a table, a plot, a benchmark. README images can live in the
  repo.
- Say how to run it. Three lines, copy-pasteable.
- A commit history that looks like real work — many small commits with real
  messages beat one "initial commit" dump.

**On your profile:**

- **Pin the six repos you want judged.** Everything else is noise; pinning is
  how you choose what gets read.
- A profile README: create a repo named exactly after your username, add
  `README.md`, and it renders at the top of your profile.
- Add CI once you have tests: a workflow running `pytest` and `ruff` on push. A
  green badge signals "this person ships working code" faster than any
  paragraph.

```yaml
# .github/workflows/test.yml
name: tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install -e ".[dev]"
      - run: ruff check .
      - run: pytest
```

---

## 13. Rules that save you

1. **Commit before anything scary.** A commit makes the work recoverable; that
   is the entire safety model.
2. **`git status` before every commit, `git diff --staged` before you type -m.**
3. **Never force-push a shared branch.** Solo you can; the habit still matters.
   Prefer `--force-with-lease`, which refuses if the remote moved under you.
4. **Never commit secrets, venvs, or data.** Rotate immediately if you slip.
5. **Pull before you start, push when you stop.** Divergence is cheap to fix at
   one commit and painful at twenty.
6. **If you are lost: `git status`, then `git log --oneline --graph --all`, then
   `git reflog`** — in that order. Do not start typing `reset --hard` while
   confused. That is the one command that turns a mess into a loss.

---

## 14. Quick reference

```bash
# look
git status                              # where am I
git log --oneline --graph --decorate --all
git log -p <file>                       # history of one file, with diffs
git log -S argpartition                 # commits that added/removed that string
git blame <file>                        # who wrote each line, and when
git show <sha>                          # one commit in full
git diff main..feature                  # branch vs branch

# move
git switch <branch>  /  git switch -c <new>
git restore <file>   /  git restore --staged <file>
git reset --soft|--mixed|--hard <ref>
git revert <sha>
git cherry-pick <sha>                   # copy one commit to here

# share
git fetch / git pull / git push
git push --force-with-lease             # the only force worth using
git clone <url>

# refs — usable anywhere a sha goes
HEAD          # current commit
HEAD~3        # three commits back
main@{2}      # where main pointed two moves ago (reflog syntax)
abc1234       # any unambiguous prefix works
```

---

## 15. Where to go deeper

- **Pro Git**, Chacon & Straub — git-scm.com/book. Free, official, complete.
  Ch.1-3 is the working knowledge, Ch.7 is the power tools, Ch.10 (Git
  Internals) is why any of it works. This is the PDF to download.
- **`git help <command>`** — offline, authoritative, better than most blog
  posts. `git help revisions` documents the `HEAD~3` / `@{2}` syntax.
- **Oh Shit, Git!?!** (ohshitgit.com) — one page, organised by disaster.
- **Learn Git Branching** (learngitbranching.js.org) — visual and interactive,
  the fastest way to make branching and rebase click.
- **GitHub Docs** on Actions and profile READMEs, when you get to §12.
