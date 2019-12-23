"""
thainlp tokenize command line.
"""
import argparse

from pythainlp import cli
from pythainlp.tokenize import (
    word_tokenize,
    subword_tokenize,
    syllable_tokenize,
    sent_tokenize,
)


class SubAppBase:
    def __init__(self, name, argv):
        parser = argparse.ArgumentParser(**cli.make_usage("tokenize " + name))
        parser.add_argument(
            "text", type=str, help="input text",
        )

        parser.add_argument(
            "-s",
            "--sep",
            type=bool,
            help=f"default: {self.sep}",
            default=self.sep,
        )

        parser.add_argument(
            "-a",
            "--algo",
            type=str,
            help=f"default: {self.algo}",
            default=self.algo,
        )

        parser.add_argument(
            "-kw",
            "--keep-whitespace",
            type=bool,
            help=f"default: {self.keep_whitespace}",
            default=self.keep_whitespace,
        )

        args = parser.parse_args(argv)

        self.args = args

        cli.exit_if_empty(args.text, parser)

        result = self.run(args.text, engine=args.algo)
        print(self.sep.join(result))


class WordTokenizationApp(SubAppBase):
    def __init__(self, *args, **kwargs):

        self.keep_whitespace = True
        self.algo = "newmm"
        self.sep = "|"
        self.run = word_tokenize

        super().__init__(*args, **kwargs)


class SyllableTokenizationApp(SubAppBase):
    def __init__(self, *args, **kwargs):

        self.keep_whitespace = True
        self.algo = "ssg"
        self.sep = "~"
        self.run = syllable_tokenize

        super().__init__(*args, **kwargs)


class SentenceTokenizationApp(SubAppBase):
    def __init__(self, *args, **kwargs):

        self.keep_whitespace = True
        self.algo = "crfcut"
        self.sep = "^"
        self.run = syllable_tokenize

        super().__init__(*args, **kwargs)


class SubwordTokenizationApp(SubAppBase):
    def __init__(self, *args, **kwargs):

        self.keep_whitespace = True
        self.algo = "tcc"
        self.sep = "/"
        self.run = syllable_tokenize

        super().__init__(*args, **kwargs)


class App:
    def __init__(self, argv):
        parser = argparse.ArgumentParser(**cli.make_usage("tokenize"))
        parser.add_argument(
            "subcommand",
            type=str,
            nargs="?",
            help="[subword|syllable|word|sent]",
        )

        args = parser.parse_args(argv[2:3])

        cli.exit_if_empty(args.subcommand, parser)
        subcommand = str.lower(args.subcommand)

        argv = argv[3:]

        if subcommand.startswith("w"):
            WordTokenizationApp("word", argv)
        elif subcommand.startswith("sy"):
            SyllableTokenizationApp("syllable", argv)
        elif subcommand.startswith("su"):
            SubwordTokenizationApp("subword", argv)
        elif subcommand.startswith("se"):
            SubwordTokenizationApp("sent", argv)
        else:
            raise NotImplementedError(
                f"Subcommand not available: {subcommand}"
            )
