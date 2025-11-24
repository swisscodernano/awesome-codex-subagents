# /agent-blockchain

Expert blockchain developer for smart contracts and DApps.

## Solidity Patterns
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract MyToken is ERC20, Ownable {
    constructor() ERC20("MyToken", "MTK") Ownable(msg.sender) {
        _mint(msg.sender, 1000000 * 10 ** decimals());
    }

    function mint(address to, uint256 amount) public onlyOwner {
        _mint(to, amount);
    }
}
```

## Hardhat Commands
```bash
npx hardhat compile
npx hardhat test
npx hardhat run scripts/deploy.js --network mainnet
npx hardhat verify --network mainnet CONTRACT_ADDRESS
```

## Web3 Integration
```javascript
import { ethers } from 'ethers';

const provider = new ethers.BrowserProvider(window.ethereum);
const signer = await provider.getSigner();
const contract = new ethers.Contract(address, abi, signer);

const tx = await contract.transfer(recipient, amount);
await tx.wait();
```
