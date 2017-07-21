CoreChain README (Still work in progress. Use with caution, and only with prior Knowledge)

Corechain is a blockchain inspired script with focus on validation. No HTTP module for initial node or peer have been included.

PROOF of work is easy but can easily be made more difficult. And its Bitcoin inspired.

Completely python 2.7 based

Steps to initiate the chain. Beware that on every rerun of the program, database is initialized (Wiped)

#Some user inputs data at your server, and the data pushes into the blockchain. Note with HTTP, this data should be send to all peers.

chain = ChainRequest(dataInput='Some Data')

#If peer solved POW, a block is created and set throughout the network for other nodes to accept.. The POST includes database for chain validation

newBlock = np.array(['2', 'ac2b12f4b5f9c3df1c31338e41654484c154377bc4ef165843fdfbe0b3ad5625', '1499093274', 'External block2', _createdHash])
databasePeer = np.vstack((databasePeer, newBlock))

#Trying to append a block from external peer
chain = ChainRequest(blockInput=databasePeer[-1], db=databasePeer)