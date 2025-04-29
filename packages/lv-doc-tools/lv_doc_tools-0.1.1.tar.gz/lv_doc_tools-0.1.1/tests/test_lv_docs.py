import pytest
from pathlib import Path
import json
import shutil
import os
from lv_doc_tools.generator import Doc_Generator


__author__ = "Mike Kidner"
__copyright__ = "Resonate Systems"
__license__ = "MIT"


@pytest.fixture
def config():
    return {
        "PATHS":{
            "ROOT": "~/lvproj",
            "LV_PROJ": "lv_proj_path",
            "OUTPUT": "~/docs_output",
            "TEST_XML": "test_outputs"
            },
        "TESTS": ["Test001.vi", "Test002.vi"],
    }


@pytest.fixture
def A_Generator():
    with open("base_config.json", "r") as fh:
        config = json.load(fh)
        print(config)
        yield Doc_Generator(config)


@pytest.fixture
def Tweak_Generator():
    with open("tweak_adocs.json", "r") as fh:
        config = json.load(fh)
        print(config)
        yield Doc_Generator(config)


def test_generator_init(config):
    DG = Doc_Generator(config)

    assert str(DG.root.stem) == "lvproj"
    assert str(DG.paths['lv_proj'].stem) == "lv_proj_path"
    assert str(DG.paths['test_xml'] == "~lvproj/lv_proj_out/test_outputs")
    assert DG.author == "Resonate Systems"
    assert DG.title == f"Documentation For {config['PATHS']['LV_PROJ']}"
    #assert Path("~/lvproj/Tests/Test001.vi") in DG.tests
    # with pytest.raises(AssertionError):
    #    fib(-10)


def test_config_paths(A_Generator):
    """
    Check that generated paths are coherent
    """
    var = vars(A_Generator)
    for k, v in var.items():
        print(f"{k}\t{v}")


def test_create_antodoc_cli_command(A_Generator):
    A_Generator.make_antidoc_command()
    assert "-a" in A_Generator.antidoc_command
    assert "Resonate Systems" in A_Generator.antidoc_command


def test_asciidoctor(Tweak_Generator):
    Tweak_Generator.make_ascii_doctor_command()

    files = list(Tweak_Generator.paths['output'].glob("*.*"))
    assert Tweak_Generator.head_file in files

    Tweak_Generator.run_command(Tweak_Generator.ascii_doctor_command)

    outfile_name = Path(Tweak_Generator.head_file.stem + ".pdf")
    outfile = Tweak_Generator.paths['output'].joinpath(outfile_name)

    files = list(Tweak_Generator.paths['output'].glob("*.*"))
    assert outfile in files


def test_build_docs(Tweak_Generator):
    # Tweak_Generator.make_antidoc_command()
    # Tweak_Generator.make_ascii_doctor_command()
    # print(Tweak_Generator.antidoc_command)
    # print(Tweak_Generator.ascii_doctor_command)

    # delete output file
    try:
        outfile_name = Path(Tweak_Generator.head_file.stem + ".pdf")
        outfile = Tweak_Generator.paths['output'].joinpath(outfile_name)
        outfile.unlink()
    except:
        print(outfile)

    Tweak_Generator.build_docs()
    # Assert pdf file shows up as expected
    pdf_files = [x for x in Tweak_Generator.paths['output'].glob("*.pdf")]
    assert outfile in pdf_files


def test_add_sources(Tweak_Generator):
    """
    Given a generator with a head_adoc file defined
    add include statements
    """
    Tweak_Generator.add_sources(["Include/src1.adoc", "Include/src2.adoc"])


def test_tweak_adocs(Tweak_Generator):
    """
    Given a generator with a head_adoc file defined
    add include statements
    """
    here = Path(__file__).parent.resolve()
    tmp_file = here.joinpath("fixtures/Antidoc-Output/lv_docs_testing.bck")
    head_file = here.joinpath("fixtures/Antidoc-Output/lv_docs_testing.adoc")
    shutil.copy(tmp_file, head_file)
    Tweak_Generator.tweak_adocs()


# def test_main(capsys):
#    """CLI Tests"""
#    # capsys is a pytest fixture that allows asserts against stdout/stderr
#    # https://docs.pytest.org/en/stable/capture.html
#    main(["7"])
#    captured = capsys.readouterr()
#    assert "The 7-th Fibonacci number is 13" in captured.out
