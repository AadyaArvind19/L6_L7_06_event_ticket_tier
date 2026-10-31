
import pytest
from event_ticket_tier import process_ticket_manifest, monitor_gate_flow


# 1. Input validation: valid and invalid inputs
def test_invalid_manifest_type():
    with pytest.raises(ValueError):
        process_ticket_manifest("invalid", 0.1)


def test_negative_tax_rate():
    with pytest.raises(ValueError):
        process_ticket_manifest([], -0.1)


def test_valid_empty_manifest_list():
    assert process_ticket_manifest([], 0.1)["status"] == "ZERO_SALES"


# 2. Confirmation: confirmed and unconfirmed
def test_unconfirmed_order():
    result = process_ticket_manifest(
        [{"is_confirmed": False}], 0.1
    )
    assert result["status"] == "ZERO_SALES"


def test_confirmed_order():
    result = process_ticket_manifest(
        [{"is_confirmed": True, "tier": "general",
          "orders": [{"qty": 2}]}], 0.1
    )
    assert result["status"] == "COMPLETED"


# 3. All ticket tiers and invalid tier
def test_vip_tier():
    result = process_ticket_manifest(
        [{"is_confirmed": True, "tier": "vip",
          "orders": [{"qty": 2}]}], 0
    )
    assert result["total_revenue"] == 300.0


def test_premium_tier():
    result = process_ticket_manifest(
        [{"is_confirmed": True, "tier": "premium",
          "orders": [{"qty": 2}]}], 0
    )
    assert result["total_revenue"] == 180.0


def test_general_tier():
    result = process_ticket_manifest(
        [{"is_confirmed": True, "tier": "general",
          "orders": [{"qty": 2}]}], 0
    )
    assert result["total_revenue"] == 90.0


def test_invalid_tier():
    result = process_ticket_manifest(
        [{"is_confirmed": True, "tier": "unknown",
          "orders": []}], 0
    )
    assert result["status"] == "ZERO_SALES"


# 4. Quantity: zero, negative and positive
def test_zero_quantity():
    result = process_ticket_manifest(
        [{"is_confirmed": True, "tier": "general",
          "orders": [{"qty": 0}]}], 0
    )
    assert result["status"] == "ZERO_SALES"


def test_negative_quantity():
    result = process_ticket_manifest(
        [{"is_confirmed": True, "tier": "general",
          "orders": [{"qty": -2}]}], 0
    )
    assert result["status"] == "ZERO_SALES"


def test_positive_quantity():
    result = process_ticket_manifest(
        [{"is_confirmed": True, "tier": "general",
          "orders": [{"qty": 2}]}], 0
    )
    assert result["total_revenue"] == 90.0


# 5. Promotional code branches
def test_earlybird_promotion():
    result = process_ticket_manifest(
        [{"is_confirmed": True, "tier": "general",
          "orders": [{"qty": 2, "promo": "EARLYBIRD"}]}], 0
    )
    assert result["total_revenue"] == 72.0


def test_normal_promotion():
    result = process_ticket_manifest(
        [{"is_confirmed": True, "tier": "general",
          "orders": [{"qty": 2, "promo": ""}]}], 0
    )
    assert result["total_revenue"] == 90.0


def test_bulk_order_discount():
    result = process_ticket_manifest(
        [{"is_confirmed": True, "tier": "general",
          "orders": [{"qty": 5, "promo": ""}]}], 0
    )
    assert result["total_revenue"] == 205.0


def test_fraud_risk_general_tier():
    result = process_ticket_manifest(
        [{"is_confirmed": True, "tier": "general",
          "orders": [{"qty": 2, "promo": "FRAUD_RISK"},
                     {"qty": 2, "promo": ""}]}], 0
    )
    assert result["total_revenue"] == 180.0


def test_fraud_risk_vip_tier():
    result = process_ticket_manifest(
        [{"is_confirmed": True, "tier": "vip",
          "orders": [{"qty": 2, "promo": "FRAUD_RISK"}]}], 0
    )
    assert result["status"] == "ZERO_SALES"


# 6. Exclusive lounge: enabled and disabled
def test_lounge_enabled():
    result = process_ticket_manifest(
        [{"is_confirmed": True, "tier": "general",
          "exclusive_lounge": True,
          "orders": [{"qty": 2}]}], 0
    )
    assert result["total_revenue"] == 165.0


def test_lounge_disabled():
    result = process_ticket_manifest(
        [{"is_confirmed": True, "tier": "general",
          "exclusive_lounge": False,
          "orders": [{"qty": 2}]}], 0
    )
    assert result["total_revenue"] == 90.0


# 7. Audit rejection and completion
def test_audit_rejected():
    result = process_ticket_manifest(
        [{"is_confirmed": True, "tier": "general",
          "orders": [{"qty": 0} for _ in range(5)]}], 0
    )
    assert result["status"] == "AUDIT_REJECTED"


def test_completed_status():
    result = process_ticket_manifest(
        [{"is_confirmed": True, "tier": "general",
          "orders": [{"qty": 2}]}], 0
    )
    assert result["status"] == "COMPLETED"


# 8. Gate monitoring: no data and normal flow
def test_no_gate_data():
    assert monitor_gate_flow([]) == "NO_DATA"


def test_normal_gate_flow():
    assert monitor_gate_flow([[20, 30, 40]]) == "FLOW_NORMAL"


# 9. Congestion: threshold and streak conditions
def test_single_high_rate():
    assert monitor_gate_flow([[60]]) == "FLOW_NORMAL"


def test_two_consecutive_high_rates():
    assert monitor_gate_flow([[60, 70]]) == "OVERFLOW"


def test_high_rates_with_reset():
    assert monitor_gate_flow([[60, 30, 70]]) == "FLOW_NORMAL"


def test_overflow_after_reset():
    assert monitor_gate_flow([[60, 30, 70, 80]]) == "OVERFLOW"


def test_multiple_gate_streams():
    assert monitor_gate_flow([[60], [70, 80]]) == "OVERFLOW"
