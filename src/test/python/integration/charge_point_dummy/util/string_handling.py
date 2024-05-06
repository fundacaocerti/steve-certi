#/*******************************************************************************
# * Copyright (c) 2024 - Fundação CERTI
# * All rights reserved.
# ******************************************************************************/

import re

def camel_to_snake(camel_str) -> str:
    pattern = re.compile(r'([A-Z])')

    return pattern.sub(lambda x: '_' + x.group(1).lower(), camel_str)

def snake_to_camel(snake_str) -> str:
    pattern = re.compile(r'_([a-z])')

    return pattern.sub(lambda x: x.group(1).upper(), snake_str)
