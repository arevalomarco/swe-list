# mock-iv-questions

Public question bank for [Mock IV](https://github.com/arevalomarco54/mock-iv) — timed quant LLD mocks in VS Code.

This repo is **questions, not answers.** There is no `reference/` here. Manifests still include interviewer hints and probes (the extension needs them); treat those as spoilers if you are sitting the question yourself.

## Pull this into Mock IV

The extension does not talk to GitHub. It only reads folders on disk at `~/.interview-vs/questions/` (or `<interviewVs.dataDir>/questions`). The root of this repo *is* that folder: one directory per question id.

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
  question.json                 # title, tags, timing, design gate, hints, probes
  prompts/                      # part 1–3 problem statements (what the extension shows)
  starter/                      # materialized after the design gate
  tests/part1|2|3               # the spec; later parts run earlier suites too
```

`QUESTION.py` / `QUESTION.cpp` is the same shape as the old comment-driven pads: part 1 prompt + stubs, then trailing PART 2 / PART 3 prompts. The extension does not load that file; it uses `prompts/`, `starter/`, and `tests/`. The pad is there to sit the question in a single buffer.

A `-cpp` suffix is a C++ translation of the same family (`event-log` / `event-log-cpp`). Progress (`done` marks, attempts) is *not* in this repo — that stays in `~/.interview-vs/` next to the clone.

## Bank

| id | title | difficulty | language |
|---|---|---|---|
| `event-log` | Event Log | warmup | python |
| `kv-store-ttl` | KV Store + TTL | easy | python |
| `bbo-nbbo` | BBO / NBBO | medium | python |
| `circuit-breaker` | Circuit Breaker | medium | python |
| `in-memory-fs` | In-Memory FS | medium | python |
| `pubsub` | Pub / Sub | medium | python |
| `token-manager` | Token Manager | medium | python |
| `user-api` | User API | medium | python |
| `abr-player` | ABR Player | hard | python |
| `arithmetic-encode` | Arithmetic Encode | hard | python |
| `diff-merge` | Diff / Merge | hard | python |
| `feed-sync` | Feed Sync | hard | python |
| `item-exchange` | Item Exchange | hard | python |
| `lru-lfu-cache` | LRU / LFU Cache | hard | python |
| `order-book` | Order Book | hard | python |
| `order-pool` | Order Pool | hard | python |
| `rate-limiter` | Rate Limiter | hard | python |
| `ring-buffer-spmc` | SPMC Ring Buffer | hard | python |
| `symbol-tracker` | Symbol Tracker | hard | python |
| `circuit-breaker-cpp` | Circuit Breaker | medium | cpp |
| `event-log-cpp` | Event Log | warmup | cpp |
| `kv-store-ttl-cpp` | KV Store + TTL | easy | cpp |
| `lru-lfu-cache-cpp` | LRU / LFU Cache | hard | cpp |
| `rate-limiter-cpp` | Rate Limiter | hard | cpp |
