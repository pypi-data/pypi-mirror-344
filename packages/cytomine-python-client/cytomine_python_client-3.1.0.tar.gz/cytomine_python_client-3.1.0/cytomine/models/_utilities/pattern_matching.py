# -*- coding: utf-8 -*-

# * Copyright (c) 2009-2024. Authors: see NOTICE file.
# *
# * Licensed under the Apache License, Version 2.0 (the "License");
# * you may not use this file except in compliance with the License.
# * You may obtain a copy of the License at
# *
# *      http://www.apache.org/licenses/LICENSE-2.0
# *
# * Unless required by applicable law or agreed to in writing, software
# * distributed under the License is distributed on an "AS IS" BASIS,
# * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# * See the License for the specific language governing permissions and
# * limitations under the License.

import re
from copy import copy
from typing import Any, List


def is_iterable(obj: Any) -> bool:
    """Portable way to check that an object is iterable"""
    try:
        iter(obj)
        return True
    except TypeError:
        return False


def resolve_pattern(pattern: str, attr_source: object) -> List[str]:
    """Resolve a string pattern using values from an attribute source.
    If one attribute is an iterable (and not a string)
    the pattern will be resolved once for each value in the iterable.

    Parameters
    ----------
    pattern: str
        A string pattern such as '{placeholder1}/___aa__{placeholder2).stg'.
    attr_source: object
        An object with attributes matching the names of the placeholders in the patterns.

    Returns
    -------
    resolved: iterable
        The list of resolved patterns
    """
    matches = re.findall(r"{([^\}]+)}", pattern)
    attr_dict = {match: getattr(attr_source, match, "_") for match in matches}

    # remaining attributes to fill in the pattern
    remaining = set(attr_dict.keys())
    patterns = [pattern]
    for attr, values in attr_dict.items():
        remaining.remove(attr)
        resolved = []
        if isinstance(values, str) or not is_iterable(values):
            values = [values]
        format_params = {a: "{" + a + "}" for a in remaining}
        for v in values:
            for p in patterns:
                format_params = copy(format_params)
                format_params[attr] = v
                resolved.append(p.format(**format_params))
        patterns = resolved

    return patterns
