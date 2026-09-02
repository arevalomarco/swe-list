# mock-iv-questions

Public question bank for [Mock IV](https://github.com/arevalomarco54/mock-iv) — timed quant LLD mocks in VS Code.

Each folder is one interview: a three-part prompt over one codebase, starter files, and accumulating tests. Clone this onto the path the extension already reads:

```bash
git clone git@github.com:arevalomarco54/mock-iv-questions.git ~/.interview-vs/questions
```

Then F5 on `mock-iv` and start an attempt.

This repo is **questions, not answers.** There is no `reference/` here. Manifests still include interviewer hints and probes (the extension needs them); treat those as spoilers if you are sitting the question yourself.

## Layout

```
<id>/
  question.json    # title, tags, timing, design gate, hints, probes
  prompts/         # part 1–3 problem statements
  starter/         # what you get after the design gate
  tests/part1|2|3  # the spec; later parts run earlier suites too
```

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
