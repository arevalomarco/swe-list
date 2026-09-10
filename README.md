# mock-iv-questions

Practice pads for [Mock IV](https://github.com/arevalomarco54/mock-iv) questions. One file per question, three parts, starter stubs. No tests, no manifests, no reference solutions.

Want the same questions inside the VS Code extension (prompts, starter, accumulating tests)? That is a different repo: [mock-iv-extension](https://github.com/arevalomarco54/mock-iv-extension).

## Sit a pad

```bash
git clone git@github.com:arevalomarco54/mock-iv-questions.git
```

1. Open `order-book/QUESTION.py` (or `event-log-cpp/QUESTION.cpp`).
2. Read only the top docstring (**Part 1**) and fill in the stubs. Do not scroll yet: PART 2 and PART 3 are below in the same file and will spoil the follow-up.
3. When Part 1 works (or you are stuck the way a real round would move on), read the `PART 2` docstring. There are no extra stubs — add methods to the same class.
4. Same again for `PART 3`.

Python pads are ordinary files; they are not wired to a test suite. C++ pads wrap the same idea in `/* */` around the header stubs — they are not a CMake target.

## Layout

```
<id>/
  QUESTION.py or QUESTION.cpp
```

A `-cpp` suffix is a C++ translation of the same family (`event-log` / `event-log-cpp`).

## Ones I sat

Questions from interviews I actually took. The rest of the bank is practice; company tags there are “this shop asks things like this,” not “I got this prompt.”

| Company | Pad | What it was |
|---|---|---|
| Jane Street | [`code-folding/QUESTION.py`](code-folding/QUESTION.py) | Code editor / folding — match braces, then fold/render `(..)`, then nested folds swallow inner ones |
| Jane Street | [`arithmetic-encode/QUESTION.py`](arithmetic-encode/QUESTION.py) | Arithmetic encode/decode — uniform `[0,1)` split, then frequency-weighted, then adaptive |
| Jump Trading | [`order-book/QUESTION.py`](order-book/QUESTION.py) | Order book — limit/market + price-time, then cancel by id, then amend |

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
| `code-folding` | Code Folding | medium | python | Jane Street |
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
