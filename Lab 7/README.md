# L6_L7_06 — Event Ticket Tier

## Lab 7: Fuzz Testing with Hypothesis

### About

This lab explores property-based fuzz testing using the Hypothesis library to identify and fix input validation bugs in a Python application.

The application contains three functions tested against unexpected and malformed inputs:

- `decode_promo_voucher()` – Validates promotional voucher codes.
- `calculate_seat_tier_price()` – Calculates seat prices based on tier and row.
- `parse_attendee_badge()` – Processes attendee badge CSV strings.

Hypothesis automatically generates edge-case inputs to identify crashes and unhandled exceptions. The application was hardened using defensive input validation to handle unexpected inputs safely.

### Files

| File | Description |
|---|---|
| `processor.py` | Corrected application containing the three functions with input validation. |
| `test_processor.py` | Hypothesis-based fuzz tests for all three functions. |
| `Lab_7_Fuzz_Testing_Screenshots.pdf` | Report containing screenshots of the original application, failing tests, fixed application, and passing tests. |

### Dependencies

Install the required libraries:

```bash
pip install hypothesis pytest
```

### Running the Application

```bash
python processor.py
```

### Running the Tests

```bash
python -m pytest test_processor.py -v
```

### Test Results

- Initial implementation: 3 tests failed due to unexpected inputs.
- Fixed implementation: All 3 tests passed.

Refer to the PDF report for execution screenshots and testing evidence.