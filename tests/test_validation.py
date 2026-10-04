import pytest

from wol_bot.validation import normalize_ip, normalize_mac, validate_name


@pytest.mark.parametrize(
    "value",
    ["AA:BB:CC:DD:EE:FF", "aa-bb-cc-dd-ee-ff", "aabb.ccdd.eeff", "AABBCCDDEEFF", " aa:bb:cc:dd:ee:ff "],
)
def test_mac_formats_are_normalized(value):
    assert normalize_mac(value) == "aa:bb:cc:dd:ee:ff"


@pytest.mark.parametrize(
    "value",
    ["aa:bb:cc:dd:ee:ff;garbage", "aa:bb:cc:dd:ee", "aa:bb:cc:dd:ee:gg", "aa:bb-cc:dd:ee:ff", ""],
)
def test_invalid_mac_is_rejected(value):
    with pytest.raises(ValueError):
        normalize_mac(value)


@pytest.mark.parametrize(
    ("value", "expected"),
    [("192.168.1.20", "192.168.1.20"), ("FE80::0001", "fe80::1")],
)
def test_ip_is_normalized(value, expected):
    assert normalize_ip(value) == expected


@pytest.mark.parametrize("value", ["nope", "192.168.1.300", "10.0.0.0/24", ""])
def test_invalid_ip_is_rejected(value):
    with pytest.raises(ValueError):
        normalize_ip(value)


@pytest.mark.parametrize("value", ["desktop", "nas-01", "pc.office", "a"])
def test_valid_names(value):
    assert validate_name(value) == value


@pytest.mark.parametrize("value", ["all", "ALL", "-desktop", "has space", "x" * 33, "<b>", ""])
def test_invalid_names(value):
    with pytest.raises(ValueError):
        validate_name(value)
