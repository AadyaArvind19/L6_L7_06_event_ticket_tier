
import pytest
from event_ticket_tier import process_ticket_manifest, monitor_gate_flow


def test_general_ticket():
    manifests = [{
        "is_confirmed": True,
        "tier": "general",
        "orders": [{"qty": 2, "promo": ""}]
    }]
    result = process_ticket_manifest(manifests, 0.1)
    assert result == {"total_revenue": 99.0, "status": "COMPLETED"}


def test_vip_ticket():
    manifests = [{
        "is_confirmed": True,
        "tier": "vip",
        "orders": [{"qty": 2, "promo": ""}]
    }]
    result = process_ticket_manifest(manifests, 0.1)
    assert result["total_revenue"] == 330.0


def test_premium_ticket():
    manifests = [{
        "is_confirmed": True,
        "tier": "premium",
        "orders": [{"qty": 2, "promo": ""}]
    }]
    result = process_ticket_manifest(manifests, 0.1)
    assert result["total_revenue"] == 198.0


def test_unconfirmed_manifest():
    result = process_ticket_manifest(
        [{"is_confirmed": False, "tier": "general"}], 0.1
    )
    assert result["status"] == "ZERO_SALES"


def test_invalid_tier():
    result = process_ticket_manifest(
        [{"is_confirmed": True, "tier": "invalid", "orders": []}], 0.1
    )
    assert result["status"] == "ZERO_SALES"


def test_invalid_quantity():
    result = process_ticket_manifest(
        [{"is_confirmed": True, "tier": "general",
          "orders": [{"qty": 0}]}], 0.1
    )
    assert result["status"] == "ZERO_SALES"


def test_earlybird_discount():
    result = process_ticket_manifest(
        [{"is_confirmed": True, "tier": "general",
          "orders": [{"qty": 2, "promo": "EARLYBIRD"}]}], 0.1
    )
    assert result["total_revenue"] == 79.2


def test_bulk_discount():
    result = process_ticket_manifest(
        [{"is_confirmed": True, "tier": "general",
          "orders": [{"qty": 5, "promo": ""}]}], 0.1
    )
    assert result["total_revenue"] == 225.5


def test_fraud_risk_non_vip():
    result = process_ticket_manifest(
        [{"is_confirmed": True, "tier": "general",
          "orders": [{"qty": 2, "promo": "FRAUD_RISK"},
                     {"qty": 2, "promo": ""}]}], 0.1
    )
    assert result["total_revenue"] == 198.0


def test_fraud_risk_vip():
    result = process_ticket_manifest(
        [{"is_confirmed": True, "tier": "vip",
          "orders": [{"qty": 1, "promo": ""},
                     {"qty": 2, "promo": "FRAUD_RISK"}]}], 0.1
    )
    assert result["status"] == "ZERO_SALES"


def test_exclusive_lounge():
    result = process_ticket_manifest(
        [{"is_confirmed": True, "tier": "general",
          "exclusive_lounge": True,
          "orders": [{"qty": 2, "promo": ""}]}], 0.1
    )
    assert result["total_revenue"] == 181.5


def test_audit_rejected():
    orders = [{"qty": 0} for _ in range(5)]
    orders.append({"qty": 2, "promo": ""})
    result = process_ticket_manifest(
        [{"is_confirmed": True, "tier": "general", "orders": orders}], 0.1
    )
    assert result["status"] == "AUDIT_REJECTED"


def test_invalid_input():
    with pytest.raises(ValueError):
        process_ticket_manifest("invalid", 0.1)

    with pytest.raises(ValueError):
        process_ticket_manifest([], -0.1)


def test_gate_no_data():
    assert monitor_gate_flow([]) == "NO_DATA"


def test_gate_normal_flow():
    assert monitor_gate_flow([[20, 30, 40]]) == "FLOW_NORMAL"


def test_gate_overflow():
    assert monitor_gate_flow([[55, 60]]) == "OVERFLOW"
