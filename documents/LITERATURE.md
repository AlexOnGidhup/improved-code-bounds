# Novelty check (25 November 2026)

Question: does each code beat the best value known today, or was it already known, already
beaten, or implied by a standard rule?

Six research agents (Claude Sonnet 5.5) fetched the comparison tables themselves, searched for
later papers and repositories, and tested the standard derivation rules against neighbouring table
cells. Their web tool returns summaries of pages, so numbers taken from web pages are second-hand.
No source was read in the original by a person.

## Verdicts

| Result | Best earlier value (source) | Verdict | Confidence |
|---|---|---|---|
| N(2,12,7) ≥ 171 | 162 (Brouwer; derived from a code by "spaik", 2011) | new | medium to high |
| N(3,11,7) ≥ 116 | 108 (Brouwer; derived) | new | medium to high |
| A_3(15,5) ≥ 8748 | 7929 (O. Sanchez, 17 Oct 2026) | new, with a caveat | medium |
| K_5(7,3) ≤ 85 | 100 (Kéri) | new | medium to high |
| K_5(9,3) ≤ 1250 | 1275 (Kéri) | new | medium to high |
| K_5(9,4) ≤ 250 | 255 (Kéri) | new | medium to high |
| K_5(9,5) ≤ 50 | 55 (Kéri) | new | medium to high |
| K_6(6,2) ≤ 216 | 274 (Rivas Soriano 2006, via Kéri) | new | high |
| K_6(7,3) ≤ 216 | 227 (Marosi 2026) | new; follows from K_6(6,2) | high |
| K_6(9,3) ≤ 3888 | 4752 (Kéri) | new; follows from K_6(6,2) | high |
| K_6(10,3) ≤ 15552 | 19347 (Kéri) | new; follows from K_6(6,2) | high |
| K_7(5,1) ≤ 766 | 769 (Kéri) | new, narrow margin | medium |
| K_7(9,4) ≤ 1372 | 1475 (Marosi 2026) | new | high |
| ten values A_3(n,d,w) | Östergård–Svanström 2002 | probably new | medium |
| A_4^GC(12,7,6) ≥ 236 | 183 (King/Gaborit table, 2010) | open | low to medium |

No result was found to be already known, already beaten, or implied by a standard rule.

## Evidence by group

### Mixed and ternary packings

- Brouwer, `23codes.html`, fetched 25 Nov 2026: N(2,12,7) = 162–432 and N(3,11,7) = 108–288. A
  footnote says both lower bounds follow from N(0,13,7) ≥ 162. The newest credits on the page are
  dated 22 Nov 2026.
- Brouwer, `ternary-1.html`, fetched 25 Nov 2026: A_3(15,5) = 7929–29213.
- codetables.de: the best linear ternary code of length 15 with distance 5 has 6561 words, so a
  linear code cannot give 8748.
- Caveat for A_3(15,5): the value 7929 comes from the repository `owhs/code-table-improvements`
  (October 2026), where it rose from 7847 to 7929 within two days. That project is active.

### Coverings over 5 symbols

- Kéri's table: K_5(7,3) ≤ 100, K_5(9,3) ≤ 1275, K_5(9,4) ≤ 255, K_5(9,5) ≤ 55. The newest note
  on the index page is dated 21 Nov 2011 and has no entries for q = 5.
- Marosi, arXiv:2608.19872 v3: the only row for q = 5 is K_5(11,5) ≤ 602.
- Standard rules applied to the neighbouring cells give 125, 1625, 325 and 65, all worse.
- Not read: the q = 5 cells of `Mapika/coldcase`, and the tables of Davydov et al. on linear
  covering codes.

### Coverings over 6 and 7 symbols

- Kéri's table (2009): K_6(6,2) ≤ 274, K_6(7,3) ≤ 246, K_6(9,3) ≤ 4752, K_6(10,3) ≤ 19347,
  K_7(5,1) ≤ 769, K_7(9,4) ≤ 1843.
- Marosi v3: K_6(7,3) ≤ 227 and K_7(9,4) ≤ 1475. The other four cells are absent.
- `Mapika/coldcase`, `cov/bounds.json`: K_6(6,2) = 133–274 and K_6(7,3) = 70–246, copied from Kéri.
- K_6(6,2) ≤ 216 is not implied by alphabet or direct-sum rules; the best derived values are 288,
  324 and 396.

### Ternary constant-weight codes

- Table 5 of Östergård–Svanström (2002) confirms the ten earlier lower bounds.
- Later work (Chee–Ling 2007, Zhang–Ge, Kharaghani–Suda–Zaitsev 2021, Polak) treats large
  distances, weight at most 4, upper bounds or families of large length, not these cells.
- Not readable: Svanström's thesis (1999), Bogdanova's paper (2000), the paper on
  constant-composition codes (2002), and citation lists.
- The narrow cases A_3(10,3,6) ≥ 878 (+2) and A_3(10,3,9) ≥ 326 (+1) are the most likely to have
  been matched somewhere. The large gains, such as 960 → 1194, are unlikely to be hidden.

### DNA code with constant GC content

- King/Gaborit table (last updated 23 June 2010): row n = 12, column d = 7 of the table without
  reverse-complement constraint gives 183. It is the right table and cell.
- Brouwer's quaternary table: 320 ≤ A_4(12,7) ≤ 1167, so 236 is plausible.
- `owhs/DNA_GC_codes_2026` has no entry for this cell, which means "not treated", not "183 confirmed".
- Not readable in two attempts: Aboluion, Smith, Perkins and Montemanni, Discrete Mathematics 311
  (2011) 1207–1219; Aboluion's thesis (2011); Montemanni, Smith and Koul (2014). A later value
  would be there. Without these tables the case stays open.

## Before claiming any record

1. Look up the (12,7,6) cell in Aboluion et al. 2011 with library access.
2. Ask O. Sanchez for the current state of A_3(15,5).
3. Ask P. Östergård about unpublished updates to the ternary constant-weight table.
4. Send the covering codes to G. Kéri and M. Marosi and the packings to A. E. Brouwer.
