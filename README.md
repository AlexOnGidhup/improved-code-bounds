# improved-code-bounds

Explicit error-correcting codes and covering codes that improve entries in the published tables
of bounds, found on 25 November 2026 by a swarm of AI research agents in one overnight run.

Every code is a plain text file, and one short script checks all of them exhaustively:

```bash
pip install numpy
python verify.py
```

The script takes about a minute and ends with `24 of 24 codes verified`.

## Status

- **The codes are valid.** Each was checked three times: by the agent that found it, by an
  independent reviewing agent, and by `verify.py`, which shares no code with the searches.
- **Novelty is checked against the tables and a literature search, not confirmed by the table
  maintainers.** No result has been submitted or peer-reviewed yet. The search found no earlier
  value that matches or beats any entry below; what it could not read is listed in
  [documents/LITERATURE.md](documents/LITERATURE.md).
- **Everything here was produced by language-model agents** (see [How this was found](#how-this-was-found)).
  A human commissioned the run and has not checked the mathematics by hand.

## Results

### Packings: more codewords at the same minimum distance

`N(m,n,d)` is the largest code with `m` binary and `n` ternary coordinates and minimum Hamming
distance `d`. `A_3(n,d)` is the largest ternary code of length `n` and distance `d`.

| Parameter | Previous lower bound | New | File |
|---|---|---|---|
| N(2,12,7) | 162 (Brouwer's table, derived from a ternary code) | **171** | [N_2_12_7__171.txt](codes/packing/N_2_12_7__171.txt) |
| N(3,11,7) | 108 (Brouwer's table, derived) | **116** | [N_3_11_7__116.txt](codes/packing/N_3_11_7__116.txt) |
| A_3(15,5) | 7929 (O. Sanchez, October 2026) | **8748** | [A3_15_5__8748.txt](codes/packing/A3_15_5__8748.txt) |

### Coverings: fewer codewords at the same radius

`K_q(n,R)` is the smallest code over `q` symbols of length `n` such that every word is within
Hamming distance `R` of a codeword.

| Parameter | Previous upper bound | New | File |
|---|---|---|---|
| K_5(7,3) | 100 (Kéri's table) | **85** | [K5_7_3__85.txt](codes/covering/K5_7_3__85.txt) |
| K_5(9,3) | 1275 (Kéri's table) | **1250** | [K5_9_3__1250.txt](codes/covering/K5_9_3__1250.txt) |
| K_5(9,4) | 255 (Kéri's table) | **250** | [K5_9_4__250.txt](codes/covering/K5_9_4__250.txt) |
| K_5(9,5) | 55 (Kéri's table) | **50** | [K5_9_5__50.txt](codes/covering/K5_9_5__50.txt) |
| K_6(6,2) | 274 (Rivas Soriano, via Kéri's table) | **216** | [K6_6_2__216.txt](codes/covering/K6_6_2__216.txt) |
| K_7(5,1) | 769 (Kéri's table) | **766** | [K7_5_1__766.txt](codes/covering/K7_5_1__766.txt) |
| K_7(9,4) | 1475 (Marosi 2026) | **1372** | [K7_9_4__1372.txt](codes/covering/K7_9_4__1372.txt) |

Three more entries follow from K_6(6,2) ≤ 216 by standard rules (append a coordinate; direct sum
with K_6(3,1) = 18 and K_6(4,1) ≤ 72). They are consequences, not separate discoveries:

| Parameter | Previous upper bound | New | File |
|---|---|---|---|
| K_6(7,3) | 227 (Marosi 2026) | **216** | [K6_7_3__216.txt](codes/covering/K6_7_3__216.txt) |
| K_6(9,3) | 4752 (Kéri's table) | **3888** | [K6_9_3__3888.txt](codes/covering/K6_9_3__3888.txt) |
| K_6(10,3) | 19347 (Kéri's table) | **15552** | [K6_10_3__15552.txt](codes/covering/K6_10_3__15552.txt) |

### Unconfirmed

These codes are valid, but the comparison is weaker. They are kept apart on purpose.

**Ternary constant-weight codes.** `A_3(n,d,w)`: ternary words of length `n` with exactly `w`
nonzero coordinates and distance `d`. The only table found is Table 5 of Östergård and Svanström
(2002). Later papers cover other parameter ranges; a 1999 thesis and two papers from 2000 and
2002 could not be read. Files are in
[codes/unconfirmed/ternary-constant-weight](codes/unconfirmed/ternary-constant-weight).

| A_3(n,d,w) | 2002 table | New |
|---|---|---|
| (7,3,4) | 60 | 62 |
| (7,3,5) | 72 | 82 |
| (8,3,5) | 161 | 173 |
| (8,3,6) | 168 | 184 |
| (9,3,6) | 411 | 483 |
| (9,3,7) | 405 | 426 |
| (10,4,5) | 204 | 221 |
| (10,3,6) | 876 | 878 |
| (10,3,7) | 960 | 1194 |
| (10,3,9) | 325 | 326 |

**DNA code with constant GC content.** `A_4^GC(12,7,6) ≥ 236`: length 12 over {A,T,G,C}, six
symbols from {G,C} in every word, distance 7, no reverse-complement constraint. The King/Gaborit
table (2010) lists 183. The paper most likely to hold a later value (Aboluion, Smith, Perkins and
Montemanni, Discrete Mathematics 311, 2011) could not be read, so this stays open. File:
[A4GC_12_7_6__236.txt](codes/unconfirmed/dna-gc-content/A4GC_12_7_6__236.txt).

## Caveats

- **A_3(15,5).** The previous record came from an active project that improved it three times
  within two days in October 2026. A better value may exist there and not yet be in the table.
- **K_7(5,1).** The margin is three codewords, the narrowest of the confirmed results.
- **Old tables.** Kéri's covering tables were last revised in 2011, and Brouwer's pages accept
  submissions by email, so unpublished improvements cannot be ruled out.
- **Second-hand reading.** The literature check was done by agents whose web tool returns page
  summaries. Table values quoted here were read that way, not from the original pages by a person.

## File format

One codeword per line, digits `0..q-1`, no separators, Unix line endings. For mixed codes the
binary coordinates come first. For the DNA code `0=A, 1=T, 2=G, 3=C`. File names are
`<parameters>__<size>.txt`. [SHA256SUMS](SHA256SUMS) lists the checksums.

## How the codes were built

| Result | Construction |
|---|---|
| N(2,12,7), N(3,11,7) | Start from the code that the table derives from a ternary code, add the words that still fit, then local search with swaps |
| A_3(15,5) | Union of 12 cosets of a linear [15,6,≥5] ternary code; the 12 syndromes are a clique found by local search (8 minutes, one core) |
| K_5(9,5), K_5(9,4), K_5(9,3), K_6(6,2), K_7(9,4) | Matrix method: the code is {x : Hx ∈ S} for a check matrix H and a small syndrome set S, with H and S found by simulated annealing or best-response iteration |
| K_5(7,3) | Orbits of a random group of coordinate permutations and affine symbol maps, then weighted set cover over the orbits |
| K_7(5,1) | Tabu search on the full space, 820 → 769 → 766 |
| Ternary constant weight | Tabu and swap search on the conflict graph of all words of weight w |
| DNA code | Orbits of a group of order 48 that preserves distance and GC content, then weighted clique search |

## How this was found

The run used [wwresearch](https://github.com/Siekwie/wwresearch), a shared board that keeps
parallel agents on different ideas and sends every claimed result to a fresh agent for review.

- **Goal:** improve any published bound for packing or covering codes with an explicit,
  checkable code. The full brief is in
  [documents/goal-given-to-agents.de.md](documents/goal-given-to-agents.de.md).
- **Agents:** Claude Code with Claude Sonnet 5.5, two to four at a time, for about nine hours on
  one desktop PC (CPU only, Python with numpy and numba). The first 20 minutes used Claude
  Mythos 5.2. An orchestrating Claude session set the run up, re-verified each claim with its own
  script and wrote this repository.
- **Volume:** 85 agents, 44 distinct approaches, 10 reviewed submissions accepted, 1 left
  inconclusive, 27 partial results, 29 dead ends.
- **Where it worked:** only in tables that had seen little computer search (mixed alphabets,
  alphabets of size 5 to 7, ternary codes). On heavily studied entries (binary codes, binary
  constant weight, the ternary football pool problem, quaternary codes) the agents only tied
  known records or failed. Details are in [documents/METHOD.md](documents/METHOD.md).

## Repository layout

| Path | Content |
|---|---|
| `codes/` | The codes: `packing/`, `covering/`, `unconfirmed/` |
| `verify.py` | Exhaustive verifier for all codes |
| `search/` | The agents' search scripts and source notes per result, archived as written (notes in German) |
| `reviews/` | Reports of the independent reviewing agents (German) |
| `documents/LITERATURE.md` | Novelty check: sources read, sources not reachable, verdict per result |
| `documents/METHOD.md` | How the run was set up, what failed, how to reproduce |
| `documents/run-log.de.md` | Orchestrator's log of the night (German) |
| `documents/board-export.md` | Full export of the research board: all cards and findings |

The scripts in `search/` are a record of what the agents ran. They were not cleaned up, some
need intermediate files that are not included, and they are not needed to check the results.

## Comparison tables

- A. E. Brouwer, tables of bounds for codes: <https://aeb.win.tue.nl/codes/>
  (`23codes.html`, `ternary-1.html`, `quaternary-1.html`)
- G. Kéri, tables for bounds on covering codes: <http://old.sztaki.hu/~keri/codes/>
- M. Marosi, "New upper and lower bounds on covering codes K_q(n,R) for alphabets of size
  5 ≤ q ≤ 21", arXiv:2608.19872 (2026)
- P. R. J. Östergård and M. Svanström, "Ternary constant weight codes", Electronic Journal of
  Combinatorics 9 (2002), R41
- O. D. King and P. Gaborit, table of DNA codes with constant GC content:
  <https://rambutan.umassmed.edu/king/dnacodes.html>
