"""
This library was built to have minimal dependencies, to minimize dependency conflicts for users.
The following code was ripped out of eth-brownie on 2022-Aug-06.
A big thanks to the many maintainers and contributors for their valuable work!
"""

from typing import Union

import cchecksum
from eth_typing import ChecksumAddress

from checksum_dict._typing import Contract


# must not be Final so it can be redefined with lru cache in ypricemagic
to_checksum_address = cchecksum.to_checksum_address


def attempt_checksum(value: Union[str, bytes, Contract]) -> ChecksumAddress:
    # sourcery skip: merge-duplicate-blocks
    if isinstance(value, str):
        return checksum_or_raise(value)
    elif (valtype := type(value)) is bytes:  # only actual bytes type, mypyc will optimize this
        return checksum_or_raise(value.hex())
    elif valtype.__name__ == "Contract":
        # already checksummed
        return value.address  # type: ignore [union-attr]
    else:  # other bytes types, mypyc will not optimize this
        return checksum_or_raise(value.hex())


def checksum_or_raise(string: str) -> ChecksumAddress:
    try:
        return to_checksum_address(string)
    except ValueError as e:
        raise ValueError(f"'{string}' is not a valid ETH address") from e
