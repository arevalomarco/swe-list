# mock-iv-questions

Public question bank for [Mock IV](https://github.com/arevalomarco54/mock-iv) — timed quant LLD mocks in VS Code.

This repo is **questions, not answers.** There is no `reference/` here. Manifests still include interviewer hints and probes (the extension needs them); treat those as spoilers if you are sitting the question yourself.

## Sit a pad (no extension)

Each folder has `QUESTION.py` or `QUESTION.cpp` — one file, three parts, starter stubs. Same shape as the old comment-driven pads.

1. Open `order-book/QUESTION.py` (or whichever id).
2. Read only the top docstring (**Part 1**) and fill in the stubs. Do not scroll yet: PART 2 and PART 3 are below in the same file and will spoil the follow-up.
3. When Part 1 works (or you are stuck the way a real round would move on), read the `PART 2` docstring. There are no extra stubs — add methods to the same class.
4. Same again for `PART 3`.

Python pads are ordinary files; they are not wired to `tests/`. To actually run the suites, use Mock IV (below) or `pytest` against that question's `tests/` with your implementation in `starter/solution/`.

C++ pads are the same idea in a `/* */` comment wrap around the header stubs. They are not a CMake target.

## Pull this into Mock IV

The extension does not talk to GitHub. It only reads folders on disk at `~/.interview-vs/questions/` (or `<interviewVs.dataDir>/questions`). The root of this repo *is* that folder: one directory per question id. It uses `prompts/`, `starter/`, and `tests/` — not `QUESTION.py`.

**Empty data dir (first time):**

```bash
git clone git@github.com:arevalomarco54/mock-iv.git
cd mock-iv
npm install
npm run build

git clone git@github.com:arevalomarco54/mock-iv-questions.git ~/.interview-vs/questions
```

Press **F5** in the `mock-iv` checkout to launch the Extension Development Host. The Questions view lists whatever is in `~/.interview-vs/questions`.

**You already have `~/.interview-vs/`** (attempts, progress). Only replace the questions folder, not the whole data dir:

```bash
# backup first if this folder has local edits
mv ~/.interview-vs/questions ~/.interview-vs/questions.bak
git clone git@github.com:arevalomarco54/mock-iv-questions.git ~/.interview-vs/questions
```

**Clone somewhere else** and point the setting at the parent of `questions/`:

```bash
git clone git@github.com:arevalomarco54/mock-iv-questions.git /path/to/questions
```

Then in VS Code: `interviewVs.dataDir` = `/path/to` (the directory that *contains* `questions/`, not `questions/` itself).

To refresh later: `git -C ~/.interview-vs/questions pull`.

## Layout

```
<id>/
  QUESTION.py or QUESTION.cpp   # practice pad: all three parts + starter stubs
  question.json                 # title, tags, companies, timing, hints, probes
  prompts/                      # part 1–3 problem statements (what the extension shows)
  starter/                      # materialized after the design gate
  tests/part1|2|3               # the spec; later parts run earlier suites too
```

A `-cpp` suffix is a C++ translation of the same family (`event-log` / `event-log-cpp`). Progress (`done` marks, attempts) is *not* in this repo — that stays in `~/.interview-vs/` next to the clone.

`question.json` already has a `companies` field (Jane Street, Citadel, Jump, …) separate from skill `tags`. The public bank table below lists both. Mock IV's Questions view currently filters on tags only; company is data waiting on a filter.

## Bank

| id | title | difficulty | language | companies |
|---|---|---|---|---|
| `event-log` | Event Log | warmup | python | |
| `kv-store-ttl` | KV Store + TTL | easy | python | |
| `bbo-nbbo` | BBO / NBBO | medium | python | Citadel |
| `circuit-breaker` | Circuit Breaker | medium | python | |
| `in-memory-fs` | In-Memory FS | medium | python | |
| `pubsub` | Pub / Sub | medium | python | |
| `token-manager` | Token Manager | medium | python | |
| `user-api` | User API | medium | python | |
| `abr-player` | ABR Player | hard | python | Jane Street |
| `arithmetic-encode` | Arithmetic Encode | hard | python | Jane Street |
| `diff-merge` | Diff / Merge | hard | python | Jane Street |
| `feed-sync` | Feed Sync | hard | python | Jane Street |
| `item-exchange` | Item Exchange | hard | python | Jane Street |
| `lru-lfu-cache` | LRU / LFU Cache | hard | python | Citadel |
| `order-book` | Order Book | hard | python | Jane Street, Jump Trading |
| `order-pool` | Order Pool | hard | python | Jump Trading |
| `rate-limiter` | Rate Limiter | hard | python | |
| `ring-buffer-spmc` | SPMC Ring Buffer | hard | python | Citadel |
| `symbol-tracker` | Symbol Tracker | hard | python | Jump Trading |
| `circuit-breaker-cpp` | Circuit Breaker | medium | cpp | |
| `event-log-cpp` | Event Log | warmup | cpp | |
| `kv-store-ttl-cpp` | KV Store + TTL | easy | cpp | |
| `lru-lfu-cache-cpp` | LRU / LFU Cache | hard | cpp | Citadel |
| `rate-limiter-cpp` | Rate Limiter | hard | cpp | |
