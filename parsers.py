import re
import asyncio


def function_to_lamda_handler(text):
    return (not bool(re.search('\d', text)) and len(text.split(' ')) == 1) or \
           (not bool(re.search('\d', text)) and len(text.split(' ')) > 1) or \
           (len(
               re.findall(
                   '[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?', text
               )
           ) > 2)


async def parse_user_expence(text: str):
    parse_digits = [float(digit) for digit in digits_parser(text)]
    price = max(parse_digits)  # передаётся в таблицу
    split_input = text.split(' ')
    for element in split_input:
        if digits_parser(element):
            digit = float(digits_parser(element)[0])
            if price == digit:
                split_input.pop(split_input.index(element))
    price_and_good = {'merchandise': ' '.join(split_input), 'price': price}
    # print(price_and_good)
    return price_and_good
    # print(' '.join(split_input), price)


def digits_parser(string_input):
    parsed = re.findall(
        '[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?', string_input)
    return parsed
