# Refactoring & Technical Debt

Aturan refactoring dan pencatatan technical debt. Berlaku saat melakukan refactor atau menemukan debt baru.

---

## Refactoring
Pertahankan behavior existing kecuali perubahan behavior memang disengaja.
```
Understand -> Test -> Refactor -> Run Test -> Review
```
Jangan melakukan large-scale refactoring tanpa memahami dependency dan impact. Prefer incremental refactoring.

## Technical Debt
Catat, jangan disembunyikan. Setiap technical debt yang signifikan punya: Problem, Impact, Priority, Proposed Solution.

```
TD-001
Problem: Recommendation logic terlalu tightly coupled.
Impact: Sulit melakukan testing dan perubahan algorithm.
Priority: Medium
Solution: Extract scoring engine dari RecommendationService.
```

Gunakan skill `refactor-code`.
