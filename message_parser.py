import re

async def parse_user_input(text, flag = False):

    if flag:
        category = re.split('\s+', text)
        category = ' '.join(category)
        print(category)
        return category
    else:
        parse_input = re.split('\n', text)
        print(parse_input)
        category = parse_input[0]
        user_goods = parse_input[1]
        expence = parse_input[2]
        return category, user_goods, expence


