"""Test that converter output matches reference file."""

from pathlib import Path


def test_main_output_matches_reference():
    # Compare converter output with conversion validated reference
    from main import convert

    converter = convert(
        "2010_01_20_-_Rob_Burbea_-_Meditation_on_emptiness_Retreat_-_Opening_talk_Orienting_and_relating_to_the_emptiness_retreat.md"
    )

    script_dir = Path(__file__).parent
    output_path = script_dir / converter.markdown_output_filename()
    output = output_path.read_text()
    reference = (
        script_dir / ".." / "result_data" / converter.markdown_target_filename()
    ).read_text()
    assert output == reference
