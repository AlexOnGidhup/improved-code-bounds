# Method

## Setup

- **Harness:** [wwresearch](https://github.com/Siekwie/wwresearch) 0.2.1. Each agent proposes one
  approach, reads the shared board once, and claims a card only if the approach is not there yet.
  A card ends as a submitted result, a partial result with a next step, or a dead end. A submitted
  result goes to a fresh agent that never sees the author's notes.
- **Agents:** Claude Code in headless mode, reasoning effort "high".
  - 01:35–01:58: three agents on Claude Mythos 5.2. Stopped because of the usage rate.
  - 02:00–10:41: Claude Sonnet 5.5, two agents at first, four from 03:45.
- **Machine:** one Windows desktop, 16 logical cores, 31 GB RAM, no GPU use. Python 3.12 with
  numpy, scipy, numba and networkx; no C compiler.
- **Rules given to the agents** (full text in `goal-given-to-agents.de.md`): check the current
  table first, save every code as a text file with a standalone exhaustive verifier, record the
  table entry and a search for newer work, stay under 3 GB RAM and four threads, post a note at
  least every 30 minutes.

## Verification chain

1. The author's `verify.py`, required to share no code with the search.
2. A reviewing agent that re-derives the check on its own and re-fetches the table.
3. The orchestrator's script, now `verify.py` in the repository root.
4. A separate literature search after the run (`LITERATURE.md`).

## What produced results

All accepted results are in tables that had seen little computer search.

| Approach | Outcome |
|---|---|
| Scan a table for cells whose bound is only derived from a neighbour, then search that cell directly | N(2,12,7), N(3,11,7) |
| Union of cosets of a linear code, clique search on syndromes | A_3(15,5) |
| Matrix method for covering codes over Z_q, q = 5, 6, 7 | K_5(9,3), K_5(9,4), K_5(9,5), K_6(6,2), K_7(9,4) |
| Group orbits plus weighted set cover | K_5(7,3) |
| Tabu search on the full space | K_7(5,1), ternary constant-weight codes |
| Closure of a covering table under the standard rules after a new entry | K_6(7,3), K_6(9,3), K_6(10,3) |

## What did not work

| Area | Outcome |
|---|---|
| Binary codes A(20,4), A(22,4) from Z4 cosets | Tied 24576 and 81920; an LP bound shows little room in these kernels |
| Binary A(17,6) with cyclic and affine groups | Record 258 not reached |
| Binary constant weight A(27,6,5), A(21,6,5) | 260 against 262; 110 tied, 111 not found |
| Ternary coverings K_3(7,2), K_3(9,2), K_3(n,1) | Tied K_3(7,2) = 34, nothing else |
| Mixed coverings K(2,7,1), K(3,5,1) | Tied 122 and 92; one kernel proved unable to go below 96 |
| Quaternary and quinary packings | Below the tables, for example 67 against 76 for A_4(8,5) |
| Linear codes over GF(8) and GF(9), saturating sets | 1 to 6 below the tables |
| Upper bounds by Delsarte LP, lower bounds for coverings by SDP | Tables are at least as good everywhere |
| Binary coverings K(n,R) | Records not reached |

The full list of cards and findings is in `board-export.md`.

## Incidents

- One search script grew to 13.7 GB and left the machine with no free memory. It was stopped by
  hand, and a watchdog then killed any Python process of the run above 4 GB. It fired twice more.

## Reproducing

Checking the results needs only `verify.py`. Re-running the searches is not packaged: the scripts
under `search/` are archived as the agents wrote them. To repeat the experiment, run wwresearch
with the goal file:

```bash
node bin/wwresearch.js run --goal-file goal-given-to-agents.de.md --agents 4 --max-ideas 0 --model claude-sonnet-5-5
```

A new run will explore different ideas and is not expected to find the same codes.
