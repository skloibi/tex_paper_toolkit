# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

from tex_paper_toolkit.stringify import make_tex_identifier


def test_make_tex_identifier_defaults():
    assert make_tex_identifier("validtexstring") == "validtexstring"
    assert make_tex_identifier("String With Spaces") == "StringWithSpaces"
    assert make_tex_identifier("$p3c14L.€hars") == "pcLhars"


def test_make_tex_identifier_spell_digits():
    assert make_tex_identifier("1", spell_digits=True) == "one"
    assert make_tex_identifier("1", spell_digits="c") == "One"
    assert (
        make_tex_identifier("$p3c14L.€hars", spell_digits=True) == "pthreeconefourLhars"
    )
    assert make_tex_identifier("const1", spell_digits="c") == "constOne"


def test_make_tex_identifier_upcase():
    assert (
        make_tex_identifier("string with spaces", upcase_after_separator=True)
        == "StringWithSpaces"
    )
    assert (
        make_tex_identifier(
            "String with 5p4ces, spe€ial chars aŋD numb3rs", upcase_after_separator=True
        )
        == "StringWithpcesSpeIalCharsADNumbrs"
    )


def test_make_tex_identifier_all_options():
    assert (
        make_tex_identifier(
            "String with 5p4ces, spe€ial chars aŋD numb3rs",
            spell_digits="c",
            upcase_after_separator=True,
        )
        == "StringWithFivepFourcesSpeIalCharsADNumbThreers"
    )
