"""Test feature translation."""
import textwrap

import pytest
from pytest_bdd import translation


def test_invalid_lang():
    """Test loading an invalid language."""
    with pytest.raises(Exception) as exc:
        translation.get_language("spam")
    assert str(exc.value) == "no translation for language code 'spam'"


def test_translated_feature(testdir):
    """Test translated feature with explicit language line."""
    testdir.makefile(".feature", test=textwrap.dedent("""
    # language: en-lol
    OH HAI: lolcat language

        MISHUN: haz cheezburger
            I CAN HAZ ingredients
            WEN I make cheezburger
            DEN I haz cheezburger
    """))
    testdir.makepyfile(textwrap.dedent("""
    import pytest
    from pytest_bdd import given, scenario, then, when

    @given("ingredients")
    def ingredients():
        return "pass"

    @when("I make cheezburger")
    def make_cheez():
        return "pass"

    @then("I haz cheezburger")
    def haz_cheez():
        return "pass"

    @scenario("test.feature", "haz cheezburger")
    def test_scenario():
        pass
    """))

    result = testdir.runpytest()
    result.assert_outcomes(passed=1)


def test_set_language_outside_header(testdir):
    """Check setting language only works in first line."""
    testdir.makefile(".feature", test=textwrap.dedent("""
    Feature: random lang declaration

        # language: en-lol
        Scenario: lang setting outside header
            Given I set language outside header
            Then lang should fallback to default english
    """))
    testdir.makepyfile(textwrap.dedent("""
    import pytest
    from pytest_bdd import given, scenario, then, when

    @given("I set language outside header")
    def given_step():
        return "pass"

    @then("lang should fallback to default english")
    def then_step():
        return "pass"

    @scenario("test.feature", "lang setting outside header")
    def test_scenario():
        pass
    """))

    result = testdir.runpytest()
    result.assert_outcomes(passed=1)


def test_translated_with_spaces(testdir):
    """Test language line with variable spacing."""
    testdir.makefile(".feature", test=textwrap.dedent("""
    #   language:en-lol
    OH HAI: lol spaces

        MISHUN: haz cheezburger
            I CAN HAZ cheezburger
            DEN I eat cheezburger
    """))
    testdir.makepyfile(textwrap.dedent("""
    import pytest
    from pytest_bdd import given, scenario, then, when

    @given("cheezburger")
    def haz_cheez():
        return "pass"

    @then("I eat cheezburger")
    def eat_cheez():
        return "pass"

    @scenario("test.feature", "haz cheezburger")
    def test_scenario():
        pass
    """))

    result = testdir.runpytest()
    result.assert_outcomes(passed=1)
