"""First blockchain for one peer only"""
from random import randint
import numpy as np
from datetime import datetime
import time
from time import gmtime, strftime
import hashlib

database = np.array([]) #Inittiliazing database

class Block():
    """Block generator, a block for the chain"""
    
    def __init__(self, index, latestHash, timestamp, data, thisHash, externaldb):
        """Block initiator"""
        
        self.index = index
        self.latestHash = latestHash
        self.timestamp = timestamp
        """Data should not be stored in the open blocks that are transmitted on P2P"""
        self.data = data
        self.thisHash = thisHash
        self.currentBlock = np.array([self.index, self.latestHash, self.timestamp, self.data, self.thisHash])
        
        if not externaldb:
            CleanUp(self.currentBlock)
            



class CleanUp():
    
    def __init__(self, currentBlock):
        """Last cleanup, validate, POW and add if solved"""
        global database
        if len(database) == 0:
            database = currentBlock
            database = database[np.newaxis, :]
        else:
            #validate the chain and block
            chainValidator = ChainValidator(database)
            blockValidator = BlockValidator(currentBlock)

            #Add block to chain
            if chainValidator.genesisValidated:
                #first validate block
                if blockValidator.blockValidated:
                    #Initiate proof of work
                    if ProofOfWork(currentBlock, database).gotThereFirst:
                        #now add to chain
                        AddBlockToChain(currentBlock)
                    else:
                        pass
                        #Someone else got there first and we do nothing
                else:
                    pass
                    #Somthing here cuz we are not adding the block to the chain
            else:
                pass
                #Something here cuz we are not accepting the chain
            

class ProofOfWork():
    """Start mining, and see which node gets there first"""
    
    def __init__(self, currentBlock, db):
        """Initiates proof of work"""
        while True:
            #check here if other node got there first
            if int(currentBlock[0]) == int(db[-1, 0]) + 1:
                """No one have solved yet"""
                _nounce = randint(0, 100)
                _stringForHash = 'CheckThisOut:'+str(_nounce)
                _hash = hashlib.sha256(_stringForHash).hexdigest()
                if _hash[:1] == '0': #Very easy
                    #Add block to chain and tell other nodes that you got their first
                    self.gotThereFirst = True
                    print 'winner %s' %(_hash)
                    break
                else:
                    continue
            elif int(currentBlock[0]) == int(db[-1, 0]):
                """Has been solved by another node"""
                self.gotThereFirst = False
                print 'fail'
            
            
        


class AddBlockToChain():
    """Adding the block to the chain"""
    
    def __init__(self, currentBlock):
        """Add block initiator"""
        global database
        database = np.vstack((database, currentBlock))
        

class LatestBlock():
    """Retrieving latest block and data from the request to the chain"""
    
    def __init__(self):
        """initiator to get the latest block"""
        global database
        _latest = database[-1]
        self.index = _latest[0]
        self.previousHash = _latest[1]
        self.timestamp = _latest[2]
        self.data = _latest[3]
        self.thisHash = _latest[4]

class GetGenesisBlock():
    """If no blocks are in the chain, a hardcoded random block is generated"""
    def __init__(self, validate):
        """Genesis block initiator"""
        if validate:
            self.input = ['0', '0', '1498665763', 'genesis block', '346f598c5a3ca5a1763975bfbd7bef930dc09f23c892db784107d2594c60ad91']
        if not validate:
            self.genesisBlock = Block('0', '0', '1498665763', 'genesis block', '346f598c5a3ca5a1763975bfbd7bef930dc09f23c892db784107d2594c60ad91', False) 

class CreateHash():
    """Hash generator for a new block and validation"""
    def __init__(self, index, latestHash, timestamp, dataInput):
        _stringForHash = str(index) + str(latestHash) + str(timestamp) + str(dataInput)
        self.createdHash = hashlib.sha256(_stringForHash).hexdigest()
        

class BlockValidator():
    """Validate the block integrity"""
    
    def __init__(self, currentBlock):
        """Initiator for the block validator"""
        self.latestBlock = LatestBlock()
        self.currentBlock = currentBlock
        self.checkIndex()
        self.checkHash()
        if self.indexValidated and self.hashValidated:
            self.blockValidated = True
        else:
            self.blockValidated = False
    
    def checkIndex(self):
        """Checker to see if the index matches"""
        if int(self.latestBlock.index) + 1 != int(self.currentBlock[0]):
            self.indexValidated = False
        else:
            self.indexValidated = True
    
    def checkHash(self):
        """Checking if hashes are the same and as the generator would create"""
        if self.latestBlock.thisHash != self.currentBlock[1]:
            self.latestHashValidated = False
            self.hashValidated = False
        elif CreateHash(self.currentBlock[0], self.currentBlock[1], self.currentBlock[2], self.currentBlock[3]).createdHash != self.currentBlock[-1]:
            self.nextHashValidated = False
            self.hashValidated = False
        else:
            self.hashValidated = True
            
            
            
    

class ChainValidator():
    """Validate the blockchain integrity"""
    
    def __init__(self, chainToValidate):
        """Chain validator initiator"""
        #Check if genesis blocks are equal
        self.checkGenesisBlocks(chainToValidate)
        self.checkRestOfChain(chainToValidate)
        
        if self.genesisValidated and self.chainFullyValidated:
            """Valid chain"""
            self.chainValidated = True
        else:
            """Chain is not valid so we do nothing"""
            self.chainValidated = False
            
        
    def checkGenesisBlocks(self, chainToValidate):
        """Method to check if genesis blocks are equal"""
        _string1 = ''
        for i in chainToValidate[0]:
            _string1 +=  i
        _string2 = ''
        for i in np.array(GetGenesisBlock(True).input):
            _string2 += i
            
        """Validate if the genesis blocks are the same"""
        if _string1 == _string2:
            self.genesisValidated = True
        else:
            self.genesisValidated = False
            
    def checkRestOfChain(self, chainToValidate):
        """Validating the rest of all the blocks"""
        global database
        for rc, lc in zip(chainToValidate[:len(database)], database):
            """checking if all blocks are the same in the two chains, before replacing"""
            _string1 = ''
            for m in rc:
                _string1 += m
            _string2 = ''
            for n in lc:
                _string2 += n

            """Validate if the genesis blocks are the same"""
            if _string1 == _string2:
                self.chainFullyValidated = True
            else:
                self.chainFullyValidated = False
            
            
            

        
        
        
            

class ChainReplace():
    """Replacing a short chain with the longest chain """
    pass
    def __init__(self, receivedChain):
        """replacing short with long chain if valid"""
        global database
        if ChainValidator(receivedChain).chainValidated and len(receivedChain) > len(database):
            database = receivedChain
            self.ChainReplace = True
        else:
            self.ChainReplace = False
            
        

class ChainRequest():
    """Request class for the BlockChain"""
    
    def __init__(self, **kwargs):
        """Init method for the http or data request. Can be either a simple datainput from this peer or a new block from another peer"""
        for key, value in kwargs.iteritems():
            if key == 'dataInput':
                """Simple datainput from this peer"""
                self.dataInput = value
                self.newBlockRequest = False
                break
            elif key == 'blockInput':
                """Blockinput from external peer"""
                self.blockInputReceived = Block(value[0], value[1], value[2], value[3], value[4], True)
                self.newBlockRequest = True
            elif key == 'db':
                self.newChainReceived = value
                
        self.databaseExist()
        
        
        
        if self.newBlockRequest:
            if self.databaseExists:
                self.checkLongestChain() 
        else:
            self.callBlockchain()

    def databaseExist(self):
        """Checks if a database exists"""
        global database
        if len(database) > 0:
            self.databaseExists = True
        else:
            self.databaseExists = False
        

        
        
    def checkLongestChain(self):
        """Checks for the longest chain in case index of two chains matches"""
        _latestBlockHeld = LatestBlock()
        
        """THIS IS ONLY CORRECT FOR ONE PEER. CHANGE THIS TO LATEST BLOCK FROM INCOMING DATABASE"""

        
        if self.blockInputReceived.index > _latestBlockHeld.index:
            """If true, we possibly have a valid blockchain behind, so we can check if it is valid and append if true"""
            if _latestBlockHeld.thisHash == self.blockInputReceived.latestHash:
                """We had a blockchain behind, so we can append the received block to the current chain"""
                AddBlockToChain(self.blockInputReceived.currentBlock)
#           elif Something about query for new peers -> send the blockchain to the peer 
            else:
                """The chain that has been received is longer so we check if we can replace chain"""
                #call replace chain which checks if we should replace chain
                ChainReplace(self.newChainReceived)
                
        else:
            """Block is not longer, so we neither append or replace"""
            pass
            
                    
    def callBlockchain(self):
        """Call the Blockchain"""
        self.blockchain = Blockchain(self)
        
    

class Blockchain():
    
    def __init__(self, chainRequest):
        """Init function. Receive blockchain, get latest block and create next block"""
        self.chainRequest = chainRequest
        self.getLatestBlock()
        self.createNextBlock()
        
    def getLatestBlock(self):
        """Function stores the latest block"""
        if self.chainRequest.databaseExists:
            """Adding next block"""
            self.latestBlock = LatestBlock()
        if not self.chainRequest.databaseExists:
            """Since there are no blocks in the chain, we get the genesis block without validating the blockchain"""
            self.latestBlock = GetGenesisBlock(False)
            self.latestBlock = self.latestBlock.genesisBlock

    
    def createNextBlock(self):
        """Block preparation for creation"""
        _upIndex = int(self.latestBlock.index) + 1
        _upDateTime = datetime.now()
        _upTimetuple = _upDateTime.timetuple()
        _upTimestamp = int(time.mktime(_upTimetuple))
        _upHash = CreateHash(_upIndex, self.latestBlock.thisHash, _upTimestamp, self.chainRequest.dataInput).createdHash
        self.nextBlock = Block(_upIndex, self.latestBlock.thisHash, _upTimestamp, self.chainRequest.dataInput, _upHash, False)

    
        
    
        
        