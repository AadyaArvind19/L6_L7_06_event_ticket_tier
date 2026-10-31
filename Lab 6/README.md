
# L6_L7_06 — Event Ticket Tier

## Lab 6: Code and Branch Coverage Analysis

### About

A Python application that manages event ticket pricing based on seating tiers, order quantities, promotional codes, and exclusive lounge access. It also handles fraudulent booking detection and monitors gate turnstile congestion.

### Files

| File | Description |
|---|---|
| `event_ticket_tier.py` | Application module under test |
| `test_event_ticket.py` | Original starter test file |
| `CodeCoverageTest_PES2UG24CS008_application.py` | Test cases for code coverage |
| `BranchCoverageTest_PES2UG24CS008_application.py` | Test cases for branch coverage |
| `code_coverage.png` | Code coverage terminal report screenshot |
| `branch_coverage.png` | Branch coverage terminal report screenshot |

### Coverage Results

| Coverage Type | Achieved Coverage |
|---|---:|
| Code Coverage | 100% |
| Branch Coverage | 100% |

### Tools Used

- Python 3.12
- pytest
- coverage.py

### How to Run

Install dependencies:

```bash
pip install pytest coverage
```

Run code coverage:

```bash
py -m coverage erase
py -m coverage run -m pytest CodeCoverageTest_PES2UG24CS008_application.py
py -m coverage report -m
```

Run branch coverage:

```bash
py -m coverage erase
py -m coverage run --branch -m pytest BranchCoverageTest_PES2UG24CS008_application.py
py -m coverage report -m
```

### Submission

All Lab 6 application files, test cases, and code and branch coverage screenshots are included in this folder.
