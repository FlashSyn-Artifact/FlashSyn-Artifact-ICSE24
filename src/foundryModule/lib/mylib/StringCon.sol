// SPDX-License-Identifier: MIT
// Adapted from OpenZeppelin Contracts v4.4.1 (utils/Strings.sol)

pragma solidity ^0.8.0;

/**
 * @dev String operations.
 */
library Strings {
    bytes16 private constant _HEX_SYMBOLS = "0123456789abcdef";

    function bool2str(bool x) internal pure returns (uint256 r) {
        assembly {
            r := x
        }
    }

    /**
     * @dev Converts a `uint256` to its ASCII `string` decimal representation.
     */
    function toString(uint256 value) internal pure returns (string memory) {
        // Inspired by OraclizeAPI's implementation - MIT licence
        // https://github.com/oraclize/ethereum-api/blob/b42146b063c7d6ee1358846c198246239e9360e8/oraclizeAPI_0.4.25.sol
        if (value == 0) {
            return "0";
        }
        uint256 temp = value;
        uint256 digits;
        while (temp != 0) {
            digits++;
            temp /= 10;
        }
        bytes memory buffer = new bytes(digits);
        while (value != 0) {
            digits -= 1;
            buffer[digits] = bytes1(uint8(48 + uint256(value % 10)));
            value /= 10;
        }
        return string(buffer);
    }

    /**
     * @dev Converts a `uint256` to its ASCII `string` hexadecimal representation.
     */
    function toHexString(uint256 value) internal pure returns (string memory) {
        if (value == 0) {
            return "0x00";
        }
        uint256 temp = value;
        uint256 length = 0;
        while (temp != 0) {
            length++;
            temp >>= 8;
        }
        return toHexString(value, length);
    }

    /**
     * @dev Converts a `uint256` to its ASCII `string` hexadecimal representation with fixed length.
     */
    function toHexString(uint256 value, uint256 length) internal pure returns (string memory) {
        bytes memory buffer = new bytes(2 * length + 2);
        buffer[0] = "0";
        buffer[1] = "x";
        for (uint256 i = 2 * length + 1; i > 1; --i) {
            buffer[i] = _HEX_SYMBOLS[value & 0xf];
            value >>= 4;
        }
        require(value == 0, "Strings: hex length insufficient");
        return string(buffer);
    }

    function uint2str(uint256 _i) internal pure returns (string memory _uintAsString) {
        return Strings.toString(_i);
    }

    function append(string memory a, string memory b) internal pure returns (string memory) {
        return string(abi.encodePacked(a, b));
    }

    function append(uint256 a, uint256 b) internal pure returns (string memory) {
        return append(uint2str(a), uint2str(b));
    }

    function appendWithSpace(uint256 a, uint256 b) internal pure returns (string memory) {
        return appendWithSpace(uint2str(a), uint2str(b));
    }

    function append(string memory a, uint256 b) internal pure returns (string memory) {
        return append(a, uint2str(b));
    }

    function append(uint256 a, string memory b) internal pure returns (string memory) {
        return append(uint2str(a), b);
    }

    function appendWithSpace(string memory a, string memory b) internal pure returns (string memory) {
        return append(a, append(" ", b));
    }

    function appendWithSpace(string memory a, uint256 b) internal pure returns (string memory) {
        return append(a, append(" ", uint2str(b)));
    }

    function appendWithSpace(string memory a, string memory b, string memory c) internal pure returns (string memory) {
        return append(append(a, " "), append(b, append(" ", c)));
    }

    function appendWithSpace(string memory a, string memory b, uint256 c) internal pure returns (string memory) {
        return append(append(a, " "), append(b, append(" ", c)));
    }

    function appendWithSpace(string memory a, string memory b, uint256 c, uint256 d)
        internal
        pure
        returns (string memory)
    {
        return append(append(a, " "), append(b, append(" ", append(c, append(" ", d)))));
    }

    function appendWithSpace(string memory a, string memory b, string memory c, string memory d)
        internal
        pure
        returns (string memory)
    {
        return append(append(a, " "), append(b, append(" ", append(c, append(" ", d)))));
    }

    function appendWithSpace(string memory a, string memory b, string memory c, uint256 d)
        internal
        pure
        returns (string memory)
    {
        return append(append(a, " "), append(b, append(" ", append(c, append(" ", d)))));
    }

    function appendWithSpace(string memory a, string memory b, string memory c, string memory d, string memory e)
        internal
        pure
        returns (string memory)
    {
        return append(append(a, " "), append(b, append(" ", append(c, append(" ", append(d, append(" ", e)))))));
    }

    function appendWithSpace(string memory a, string memory b, string memory c, string memory d, uint256 e)
        internal
        pure
        returns (string memory)
    {
        return append(append(a, " "), append(b, append(" ", append(c, append(" ", append(d, append(" ", e)))))));
    }

    function toString(address account) public pure returns (string memory) {
        return toString(abi.encodePacked(account));
    }

    // function toString(uint256 value) public pure returns(string memory) {
    //     return toString(abi.encodePacked(value));
    // }

    function toString(bytes32 value) public pure returns (string memory) {
        return toString(abi.encodePacked(value));
    }

    function toString(bytes memory data) public pure returns (string memory) {
        bytes memory alphabet = "0123456789abcdef";

        bytes memory str = new bytes(2 + data.length * 2);
        str[0] = "0";
        str[1] = "x";
        for (uint256 i = 0; i < data.length; i++) {
            str[2 + i * 2] = alphabet[uint256(uint8(data[i] >> 4))];
            str[3 + i * 2] = alphabet[uint256(uint8(data[i] & 0x0f))];
        }
        return string(str);
    }
}
