import pytest
from pytest_mock import MockerFixture
import asyncio
from typing import Tuple
from .test_cases import (
    test_case_get_do_option,
    test_case_get_do_option_name,
    test_case_prompt,
    test_case_should_exit,
    test_case_validate_prompt,
    test_case_should_exit,
)
from pygottado.utils.functions import (
    prompt,
    get_do_option,
    get_do_option_name,
    get_do_options,
    validate_prompt,
    should_exit,
)
from pygottado.utils import DoOption, DO_OPTION_DICT, COLOR
from pygottado.utils.classes import ColorCycler
from unittest import mock
from termcolor import colored


class TestFunctions:

    @pytest.mark.asyncio
    @pytest.mark.parametrize("option_no, expected", test_case_get_do_option)
    async def test_get_do_option(
        self, option_no: int, expected: DoOption | None
    ) -> None:

        result: DoOption | None = await get_do_option(option_no=option_no)
        assert result == expected

    @pytest.mark.asyncio
    @pytest.mark.parametrize("do_option, expected", test_case_get_do_option_name)
    async def test_get_do_option_name(
        self, do_option: DoOption, expected: str | None
    ) -> None:
        result: str | None = await get_do_option_name(do_option=do_option)
        assert result == expected

    @pytest.mark.asyncio
    async def test_get_do_options(self) -> None:
        result: Tuple[DoOption, ...] = await get_do_options()
        assert result == tuple(DO_OPTION_DICT.values())

    @pytest.mark.parametrize("mock_result, mocked_color, expected", test_case_prompt)
    @pytest.mark.asyncio  # Use the async decorator to run the test asynchronously
    async def test_prompt(
        self,
        mocker: MockerFixture,
        mock_result: str,
        mocked_color: COLOR,
        expected: str | None,
    ) -> None:
        # Mock the input function to simulate user input
        mock_input = mocker.patch("builtins.input")
        mock_input.return_value = mock_result

        # Mock the ColorCycler class and its get_next_color method
        mock_color_cycler = mocker.patch.object(
            ColorCycler, "get_next_color", return_value=mocked_color
        )

        # Run the async prompt function
        text: str = colored("\r\t> ", color=mocked_color)
        result = await prompt(
            mock_color_cycler, text
        )  # Use await instead of asyncio.run() since pytest-asyncio handles async

        # Assert that the mocks were called
        mock_color_cycler.get_next_color.assert_called_once()
        mock_input.assert_called_once_with(text)

        # Assert the result is as expected
        assert result == expected

    @pytest.mark.asyncio
    @pytest.mark.parametrize("prompt_str, expected", test_case_validate_prompt)
    async def test_validate_prompt(self, prompt_str: str, expected: bool) -> None:
        result: bool = await validate_prompt(prompt_str=prompt_str)
        assert result == expected

    @pytest.mark.asyncio
    @pytest.mark.parametrize("code, expected", test_case_should_exit)
    async def test_should_exit(self, code: str, expected: bool) -> None:
        assert await should_exit(code) == expected
