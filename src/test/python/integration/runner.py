#!/usr/bin/env python3
#/*******************************************************************************
# * Copyright (c) 2024 - Fundação CERTI
# * All rights reserved.
# ******************************************************************************/

import pathlib, sys

import pytest

cwd = pathlib.Path.cwd()

sys.path.append(str( cwd.parent ))

sys.path.append(str( cwd / 'app/charge_point_dummy' ))
sys.path.append(str( cwd / 'app/app_dummy' ))
sys.path.append(str( cwd / 'app/db_helper' ))

errors = pytest.main(['-vv'])

exit(errors)
