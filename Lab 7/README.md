# L6_L7_51 — Self Storage

Lab 7: Fuzz Testing

## About

A small Python module that parses storage rentals, averages rental durations and works out the payable rent after a discount.

## Files

| File | Description |
|------|-------------|
| `self_storage.py` | The code under test |
| `test_self_storage.py` | Starter test file |

Refer to the lab handout for instructions.

## Submission — PES1UG24AM356

| File | Description |
|------|-------------|
| `self_storage.py` | Fixed module, hardened against invalid input |
| `test_self_storage.py` | Completed Hypothesis fuzz tests (13 property tests) |
| `Lab7_Report_PES1UG24AM356.pdf` | Report with screenshots for every step |
| `screenshots/` | Terminal screenshots used in the report |

Run the tests:

```
pip install hypothesis pytest
python -m pytest test_self_storage.py
```
