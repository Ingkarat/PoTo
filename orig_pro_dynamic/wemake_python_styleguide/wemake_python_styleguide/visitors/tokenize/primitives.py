import re
import tokenize
from typing import ClassVar, FrozenSet, Optional
from typing.re import Pattern

from flake8_quotes.docstring_detection import get_docstring_tokens
from typing_extensions import final

from wemake_python_styleguide.logic.tokens import (
    has_triple_string_quotes,
    split_prefixes,
)
from wemake_python_styleguide.violations import consistency
from wemake_python_styleguide.violations.best_practices import (
    WrongUnicodeEscapeViolation,
)
from wemake_python_styleguide.visitors.base import BaseTokenVisitor


def _replace_braces(string: str) -> str:
    if string.startswith('"'):
        return string.lstrip('"').rstrip('"')
    return string.lstrip("'").rstrip("'")


@final
class WrongNumberTokenVisitor(BaseTokenVisitor):
    """Visits number tokens to find incorrect usages."""

    _bad_number_suffixes: ClassVar[Pattern] = re.compile(
        r'^[0-9\.]+[BOXE]',
    )

    _leading_zero_pattern: ClassVar[Pattern] = re.compile(
        r'^[0-9\.]+([box]|e\+?\-?)0.+', re.IGNORECASE | re.ASCII,
    )
    _leading_zero_float_pattern: ClassVar[Pattern] = re.compile(
        r'^[0-9]*\.[0-9]+0+$',
    )

    _positive_exponent_patterns: ClassVar[Pattern] = re.compile(
        r'^[0-9\.]+e\+', re.IGNORECASE | re.ASCII,
    )

    _bad_hex_numbers: ClassVar[FrozenSet[str]] = frozenset((
        'a', 'b', 'c', 'd', 'e', 'f',
    ))

    _bad_complex_suffix: ClassVar[str] = 'J'

    _float_zero: ClassVar[Pattern] = re.compile(
        r'^0\.0$',
    )

    def visit_number(self, token: tokenize.TokenInfo) -> None:
        """
        Checks number declarations.

        Raises:
            UnderscoredNumberViolation
            PartialFloatViolation
            BadNumberSuffixViolation
            BadComplexNumberSuffixViolation
            NumberWithMeaninglessZeroViolation
            PositiveExponentViolation
            FloatZeroViolation

        Regressions:
        https://github.com/wemake-services/wemake-python-styleguide/issues/557

        """
        self._check_complex_suffix(token)
        self._check_underscored_number(token)
        self._check_partial_float(token)
        self._check_bad_number_suffixes(token)
        self._check_float_zeros(token)

    def _check_complex_suffix(self, token: tokenize.TokenInfo) -> None:
        if self._bad_complex_suffix in token.string:
            self.add_violation(
                consistency.BadComplexNumberSuffixViolation(
                    token,
                    text=self._bad_complex_suffix,
                ),
            )

    def _check_underscored_number(self, token: tokenize.TokenInfo) -> None:
        if '_' in token.string:
            self.add_violation(
                consistency.UnderscoredNumberViolation(
                    token,
                    text=token.string,
                ),
            )

    def _check_partial_float(self, token: tokenize.TokenInfo) -> None:
        if token.string.startswith('.') or token.string.endswith('.'):
            self.add_violation(
                consistency.PartialFloatViolation(token, text=token.string),
            )

    def _check_bad_number_suffixes(self, token: tokenize.TokenInfo) -> None:
        if self._bad_number_suffixes.match(token.string):
            self.add_violation(
                consistency.BadNumberSuffixViolation(token, text=token.string),
            )

        float_zeros = self._leading_zero_float_pattern.match(token.string)
        other_zeros = self._leading_zero_pattern.match(token.string)
        if float_zeros or other_zeros:
            self.add_violation(
                consistency.NumberWithMeaninglessZeroViolation(
                    token,
                    text=token.string,
                ),
            )

        if self._positive_exponent_patterns.match(token.string):
            self.add_violation(
                consistency.PositiveExponentViolation(
                    token,
                    text=token.string,
                ),
            )

        if token.string.startswith('0x') or token.string.startswith('0X'):
            has_wrong_hex_numbers = any(
                char in self._bad_hex_numbers
                for char in token.string
            )
            if has_wrong_hex_numbers:
                self.add_violation(
                    consistency.WrongHexNumberCaseViolation(
                        token,
                        text=token.string,
                    ),
                )

    def _check_float_zeros(self, token: tokenize.TokenInfo) -> None:
        if self._float_zero.match(token.string):
            self.add_violation(
                consistency.FloatZeroViolation(token, text=token.string),
            )


@final
class WrongStringTokenVisitor(BaseTokenVisitor):
    """Checks incorrect string tokens usages."""

    _bad_string_modifiers: ClassVar[FrozenSet[str]] = frozenset((
        'R', 'F', 'B', 'U',
    ))

    _unicode_escapes: ClassVar[FrozenSet[str]] = frozenset((
        'u', 'U', 'N',
    ))

    _implicit_raw_strings: ClassVar[Pattern] = re.compile(r'\\{2}.+')

    def __init__(self, *args, **kwargs) -> None:
        """Initializes new visitor and saves all docstrings."""
        super().__init__(*args, **kwargs)
        self._docstrings = get_docstring_tokens(self.file_tokens)

    def visit_string(self, token: tokenize.TokenInfo) -> None:
        """
        Finds incorrect string usages.

        ``u`` can only be the only prefix.
        You cannot combine it with ``r``, ``b``, or ``f``.
        Since it will raise a ``SyntaxError`` while parsing.

        Raises:
            UnicodeStringViolation
            WrongMultilineStringViolation
            ImplicitRawStringViolation
            WrongUnicodeEscapeViolation
            RawStringNotNeededViolation

        """
        self._check_correct_multiline(token)
        self._check_string_modifiers(token)
        self._check_implicit_raw_string(token)
        self._check_wrong_unicode_escape(token)
        self._check_unnecessary_raw_string(token)

    def _check_correct_multiline(self, token: tokenize.TokenInfo) -> None:
        _, string_def = split_prefixes(token.string)
        if has_triple_string_quotes(string_def):
            if '\n' not in string_def and token not in self._docstrings:
                self.add_violation(
                    consistency.WrongMultilineStringViolation(token),
                )

    def _check_string_modifiers(self, token: tokenize.TokenInfo) -> None:
        modifiers, _ = split_prefixes(token.string)

        if 'u' in modifiers.lower():
            self.add_violation(
                consistency.UnicodeStringViolation(token, text=token.string),
            )

        for mod in modifiers:
            if mod in self._bad_string_modifiers:
                self.add_violation(
                    consistency.UppercaseStringModifierViolation(
                        token,
                        text=mod,
                    ),
                )

    def _check_implicit_raw_string(self, token: tokenize.TokenInfo) -> None:
        modifiers, string_def = split_prefixes(token.string)
        if 'r' in modifiers.lower():
            return

        if self._implicit_raw_strings.search(_replace_braces(string_def)):
            self.add_violation(
                consistency.ImplicitRawStringViolation(
                    token,
                    text=token.string,
                ),
            )

    def _check_wrong_unicode_escape(self, token: tokenize.TokenInfo) -> None:
        # See: http://docs.python.org/reference/lexical_analysis.html
        modifiers, string_body = split_prefixes(token.string)

        index = 0
        while True:
            index = string_body.find('\\', index)
            if index == -1:
                break

            next_char = string_body[index + 1]
            if 'b' in modifiers.lower() and next_char in self._unicode_escapes:
                self.add_violation(
                    WrongUnicodeEscapeViolation(token, text=token.string),
                )

            # Whether it was a valid escape or not, backslash followed by
            # another character can always be consumed whole: the second
            # character can never be the start of a new backslash escape.
            index += 2

    def _check_unnecessary_raw_string(self, token: tokenize.TokenInfo) -> None:
        modifiers, string_def = split_prefixes(token.string)

        if 'r' in modifiers.lower() and '\\' not in string_def:
            self.add_violation(
                consistency.RawStringNotNeededViolation(token, text=string_def),
            )


@final
class WrongStringConcatenationVisitor(BaseTokenVisitor):
    """Checks incorrect string concatenation."""

    _ignored_tokens: ClassVar[FrozenSet[int]] = frozenset((
        tokenize.NL,
        tokenize.NEWLINE,
        tokenize.INDENT,
        tokenize.COMMENT,
    ))

    def __init__(self, *args, **kwargs) -> None:
        """Adds extra ``_previous_token`` property."""
        super().__init__(*args, **kwargs)
        self._previous_token: Optional[tokenize.TokenInfo] = None

    def visit(self, token: tokenize.TokenInfo) -> None:
        """
        Ensures that all string are concatenated as we allow.

        Raises:
            ImplicitStringConcatenationViolation

        """
        self._check_concatenation(token)

    def _check_concatenation(self, token: tokenize.TokenInfo) -> None:
        if token.exact_type in self._ignored_tokens:
            return

        if token.exact_type == tokenize.STRING:
            if self._previous_token:
                self.add_violation(
                    consistency.ImplicitStringConcatenationViolation(token),
                )
            self._previous_token = token
        else:
            self._previous_token = None
