# Turn A Bug Into A Reproducible Test

_When to use:_ When a bug is fixed and you want to prevent it returning.

```text
Convert this bug report into a reproducible automated test. Define preconditions, test data, steps, expected result and failure condition. First inspect existing test patterns. Create the smallest regression test that would have failed before the fix and passes after the fix. Run it and report actual evidence.
```
