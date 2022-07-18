//SPDX-License-Identifier: MIT

pragma solidity ^0.6.0;

contract SimpleStorage {
    uint256 FavoriteNumber;

    struct People {
        uint256 FavoriteNumber;
        string Name;
    }

    People[] public person;
    mapping(string => uint256) public nameToFavoriteNumber;

    function Store(uint256 _FavoriteNumber) public returns (uint256) {
        FavoriteNumber = _FavoriteNumber;
        return FavoriteNumber;
    }

    function retrieve() public view returns (uint256) {
        return FavoriteNumber;
    }

    function addperson(string memory _Name, uint256 _FavoriteNumber) public {
        person.push(People(_FavoriteNumber, _Name));
        nameToFavoriteNumber[_Name] = _FavoriteNumber;
    }
}
