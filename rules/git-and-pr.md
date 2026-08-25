# Git & Pull Request

Aturan commit, branch, dan pull request. Berlaku setiap kali membuat commit, branch, atau PR.

---

## Branch
```
main
feature/*
fix/*
refactor/*
chore/*
```

## Commit
Prefer:
```
feat: add recommendation endpoint
fix: resolve duplicate ranking
refactor: extract scoring service
test: add recommendation service tests
docs: update API documentation
```
Hindari: `update`, `fix`, `final`, `final2`, `fix banget`.

## Pull Request
PR wajib menjelaskan: apa yang berubah, kenapa, bagaimana cara ditest, ada breaking change atau tidak, perlu migration atau tidak.

Code review wajib memeriksa: Correctness, Readability, Architecture, Security, Performance, Testing, Maintainability.
