# CoreChain 

- A simple blockchain 

Work in progress. Use with caution, and only with prior knowledge

## Description

CoreChain is a blockchain inspired script with focus on validation. No HTTP module for initial node or peer node have been included.

Proof of Work is easy but can easily be made more difficult. And its Bitcoin inspired.

Beware that on every rerun of the program, database is initialized (Wiped) - Script should run continuously in a terminal, or it will need another DB setup.


### Data input
User inputs data at your server, and pushes data into the blockchain. Note with HTTP, this data should be send to all peers (nodes)

Example
```
chain = ChainRequest(dataInput='Some Data')
```

### Proof of work initiates 

If a peer solved POW, a block should be created and sent throughout the network for other nodes to accept. The POST includes the database for chain validation

Example
```
newBlock = np.array(['2', 'ac2b12f4b5f9c3df1c31338e41654484c154377bc4ef165843fdfbe0b3ad5625', '1499093274', 'External block2', _createdHash])
databasePeer = np.vstack((databasePeer, newBlock))
```

Trying to append a block from peer node. It will be declined if another node solved the POW first

```
chain = ChainRequest(blockInput=databasePeer[-1], db=databasePeer)
```
