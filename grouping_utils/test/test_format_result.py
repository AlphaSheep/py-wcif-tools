from grouping_utils.results import format_result


def test_format_result():
    assert format_result(32, "333fm", "single") == "32"
    assert format_result(3233, "333fm", "average") == "32.33"
    assert format_result(3233, "333", "average") == "32.33"
    assert format_result(7234, "222", "single") == "1:12.34"
    assert format_result(940315501, "333mbf", "single") == "6/7 (52:35)"


