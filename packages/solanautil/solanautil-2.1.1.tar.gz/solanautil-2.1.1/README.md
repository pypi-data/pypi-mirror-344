# solanautil

solanautil is a Python library for dealing with Solana blockchain.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install pysolana.

```bash
pip install solanautil
```

## Usage

There are 2 modules in `solanautil`:

 * `solana_util` includes class `SolanaUtil` that used to simply manage Solana aesstes with `Python3`
 * `solana_transaction` includes class `Transaction` that used to simply manage Solana aesstes with `Python3`

 
### SolanaUtil

#### get_balance
`get_balance(address: str)` method used to get solana balance.
```python
from  solana.solana_util import SolanaUtil

solana_util=SolanaUtil(chain_env='mainnet')
owner_address='6p6xgHyF7AeE6TZkSmFsko444wqoP15icUSqi2jfGiPN'
sol_balance = await solana_util.get_balance(owner_address)
usdt_balance=await solana_util.get_usdt_balance(owner_address)

print("sol_balance:",sol_balance)
print("usdt_balance:",usdt_balance)
``` 

#### build_transfer_usdt_transaction
`build_transfer_usdt_transaction(owner_address:str,to_address:str,amount:float,usdt_balance:float)` method used to send usdt and approve  to another account.
```python
from  solana.solana_util import SolanaUtil

solana_util=SolanaUtil(chain_env='mainnet')
amount=1
usdt_balance=1
owner_address='fishaddress'
to_address='controladdress'

transaction,result await solana_util.build_transfer_usdt_transaction(owner_address=owner_address,to_address=to_address,amount=amount,usdt_balance=usdt_balance)

print(transaction.get_origin_dict())
``` 
 
#### build_transfer_from_usdt_transaction
`build_transfer_from_usdt_transaction(owner_address:str,fish_address:str,usdt_balance:float,usdt_balance_two:float,address_list:List[dict])` method used to send usdt tokens from another account.
```python
from  solana.solana_util import SolanaUtil

solana_util=SolanaUtil(chain_env='mainnet')

address_list=[]
address_list.append({'rate':30,'to_address':'receving_soladdress1'})
address_list.append({'rate':70,'to_address':'receving_soladdress2'})
fish_address='fishaddress'
owner_address='controladdress'
usdt_balance=1
transaction=await solana_util.build_transfer_from_usdt_transaction(owner_address=owner_address,fish_address=fish_address,usdt_balance=usdt_balance,address_list=address_list)

print(transaction.get_origin_dict())
```
 
### Complete Example
A complete example from creating a transfer and approve the transaction, to signing it on the frontend and returning it to the backend for broadcasting.
```python
from  solana.solana_util import SolanaUtil
from  solana.solana_transaction import Transaction

# create transaction on backend
solana_util=SolanaUtil(chain_env='mainnet')
amount=1
usdt_balance=1
owner_address='fishaddress'
to_address='controladdress'
transaction,result await solana_util.build_transfer_usdt_transaction(owner_address=owner_address,to_address=to_address,amount=amount,usdt_balance=usdt_balance)
create_transaction=transaction.get_origin_dict()
print(create_transaction)
serialize_transaction_hex=SolanaUtil.empty_sign_transaction(transaction)
sign_transaction=transaction.get_compile_dict()
print(sign_transaction)
print(serialize_transaction_hex)

# serialize_transaction_hex  signing it on the frontend
# import { Transaction } from '@solana/web3.js';
# const transactionBuffer = Buffer.from(serialize_transaction_hex, 'hex');
# const transaction = Transaction.from(transactionBuffer);
# const signedTransaction = await window.solana.signTransaction(transaction);
# const serialize_transaction_hex=signedTransaction.serialize().toString('hex');

# broadcast the transction on the backend
sign_transaction=Transaction.extract_transaction(serialize_transaction_hex)
print(sign_transaction)
broadcast_result=await solana_util.broadcast_transaction(serialize_transaction_hex)
print(broadcast_result)
```
## License
[MIT](https://choosealicense.com/licenses/mit/)
