import os
import sys
import shutil
import argparse
from pdf_to_markdown import (
    MarkdownToDocument,
    PrintDocument,
    WriteAsLangchainDocuments,
)

DEBUG = False


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Convert Rob Burbea's document to canonical markdown."
    )
    parser.add_argument(
        "--output_directory",
        type=str,
        metavar="DIR",
        help="Relative path to output directory (default is CWD).",
    )

    args = parser.parse_args()

    return args


class Converter:

    @staticmethod
    def markdown_output_filename():
        return "output.md"

    @staticmethod
    def markdown_output_filepath():
        return os.path.join(os.getcwd(), Converter.markdown_output_filename())

    @staticmethod
    def sentences_output_filepath():
        return os.path.join(os.getcwd(), "Sentences_as_LangChain_Document.json")

    def markdown_target_filename(self):
        file_no_ext = os.path.splitext(
            os.path.basename(self.original_document_filename)
        )[0]
        return file_no_ext + "_-_local_converter.md"

    def sentences_target_filename(self):
        file_no_ext = os.path.splitext(
            os.path.basename(self.original_document_filename)
        )[0]
        return file_no_ext + "_-_Sentences_as_LangChain_Document.json"

    def __init__(self, original_document_filename):
        self.original_document_filename = original_document_filename

    def run(self):
        document_filename = os.path.join(
            os.path.dirname(__file__),
            "..",
            "original_data",
            self.original_document_filename,
        )

        document = MarkdownToDocument(document_filename).get_document()
        # On debugging purposes
        if False:
            PrintDocument(document).pages()
            PrintDocument(document).paragraphs()
            PrintDocument(document).sentences()

        # Write the markdown file
        document.to_markdown(Converter.markdown_output_filepath())

        # For downstream Knowledge Graph extraction
        if True:
            WriteAsLangchainDocuments(document).write_sentences(
                Converter.sentences_output_filepath()
            )

    def move_outputs_to_output_dir(self, target_output_dir):
        converted_markdown_source = Converter.markdown_output_filepath()

        if not os.path.exists(converted_markdown_source):
            print(
                f"Converted markdown output file ({converted_markdown_source}) not found. Exiting."
            )
            sys.exit()

        converted_markdown_target = os.path.join(
            target_output_dir, self.markdown_target_filename()
        )
        shutil.move(converted_markdown_source, converted_markdown_target)

        sentences_source = Converter.sentences_output_filepath()
        if not os.path.exists(sentences_source):
            print(f"Sentences output file ({sentences_source}) not found. Exiting.")
            sys.exit()

        sentences_target = os.path.join(
            target_output_dir,
            self.sentences_target_filename(),
        )
        shutil.move(sentences_source, sentences_target)
        if DEBUG:
            print("Following files moved to output:")
            print(f"  - {converted_markdown_target}")
            print(f"  - {sentences_target}")


def convert(original_document_filename):
    args = parse_arguments()
    converter = Converter(original_document_filename)
    converter.run()
    if args.output_directory:
        converter.move_outputs_to_output_dir(args.output_directory)
    return converter


if __name__ == "__main__":
    convert(
        "2010_01_20_-_Rob_Burbea_-_Meditation_on_emptiness_Retreat_-_Opening_talk_Orienting_and_relating_to_the_emptiness_retreat.md"
    )
