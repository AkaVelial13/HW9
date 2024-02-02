import unittest
from unittest.mock import patch

from main import (
    input_error,
    handle_contact_add,
    handle_contact_change,
    handle_contact_get_by_name,
    handle_contact_get_all,
    handle_invalid_command,
    handle_hello,
    handle_end,
    get_handler,
    main,
)


class TestContactHandler(unittest.TestCase):

    def setUp(self):
        # Перенаправляем потоки ввода/вывода
        self.patch_input = patch('builtins.input', side_effect=['input_data'])
        self.patch_print = patch('builtins.print')

        # Стартуем перенаправление потоков
        self.mock_input = self.patch_input.start()
        self.mock_print = self.patch_print.start()

    def tearDown(self):
        # Останавливаем перенаправление потоков
        self.patch_input.stop()
        self.patch_print.stop()

    def test_handle_contact_add(self):
        with patch.dict('main.contacts', {}, clear=True):
            result = handle_contact_add(['John', '123456789'])
            self.assertEqual(result, 'Contact John added with phone number 123456789')

            result = handle_contact_add(['John', '987654321'])
            self.assertEqual(result, 'Contact John already exists!')

    def test_handle_contact_change(self):
        with patch.dict('main.contacts', {'John': '123456789'}, clear=True):
            result = handle_contact_change(['John', '987654321'])
            self.assertEqual(result, 'Phone number for John changed to 987654321')

            result = handle_contact_change(['Alice', '123'])
            self.assertEqual(result, 'Contact Alice not found')

    def test_handle_contact_get_by_name(self):
        with patch.dict('main.contacts', {'John': '123456789'}, clear=True):
            result = handle_contact_get_by_name(['John'])
            self.assertEqual(result, 'Phone number for John is 123456789')

            result = handle_contact_get_by_name(['Alice'])
            self.assertEqual(result, 'Contact Alice not found')

    def test_handle_contact_get_all(self):
        with patch.dict('main.contacts', {'John': '123456789', 'Alice': '987654321'}, clear=True):
            result = handle_contact_get_all()
            expected_output = '   Name: Phone number\n   Alice: 987654321\n   John: 123456789\n'

            # Разбиваем строки на списки для учета различий в формате вывода
            result_lines = result.strip().split('\n')
            expected_lines = expected_output.strip().split('\n')

            # Проверяем, что количество строк совпадает
            assert len(result_lines) == len(expected_lines)

            # Проверяем, что каждая строка из result_lines есть в expected_lines
            for line in result_lines:
                assert line in expected_lines

        # Тест без данных
        with patch.dict('main.contacts', {}, clear=True):
            result = handle_contact_get_all()
            assert result == 'No contacts found'

    def test_input_error_decorator(self):
        @input_error
        def function_that_raises_key_error():
            raise KeyError('Test Key Error')

        result = function_that_raises_key_error()
        self.assertEqual(result, 'Enter user name')

        @input_error
        def function_that_raises_value_error():
            raise ValueError('Test Value Error')

        result = function_that_raises_value_error()
        self.assertEqual(result, 'Give me name and phone please')

        @input_error
        def function_that_raises_index_error():
            raise IndexError('Test Index Error')

        result = function_that_raises_index_error()
        self.assertEqual(result, 'Invalid command format')

    def test_handle_invalid_command(self):
        result = handle_invalid_command()
        self.assertEqual(result, 'Invalid command format')

    def test_handle_hello(self):
        result = handle_hello()
        self.assertEqual(result, 'How can I help you?')

    def test_handle_end(self):
        result = handle_end()
        self.assertEqual(result, 'Good bye!')

    def test_get_handler(self):
        result = get_handler('hello')
        self.assertEqual(result[0], handle_hello)
        self.assertEqual(result[1], [])

        result = get_handler('add John 123456789')
        self.assertEqual(result[0], handle_contact_add)
        self.assertEqual(result[1], ['John', '123456789'])

        result = get_handler('invalid_command')
        self.assertEqual(result[0], handle_invalid_command)
        self.assertEqual(result[1], [])


def test_main():
    with patch('builtins.input', side_effect=['add John 123456789', 'show all', 'exit']):
        with patch('builtins.print') as mock_print:
            main()
            expected_output = '   Name: Phone number\n   John: 123456789\nGood bye!\n'
            mock_print.assert_called_with(expected_output)


if __name__ == '__main__':
    unittest.main()
