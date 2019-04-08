![IOTA Logo](http://fs5.directupload.net/images/170402/8d5xdkkb.png)

# IOTAPyLib

IOTAPyLib is an easy to use wrapper for IOTA API written in Python. It is lightweight and offers all basic functionality of IOTA.

## Prerequisites

Requires Python 2.6 or higher.

## Usage

To use the library simply import *iotawrapper.py* from the respective python version folder. Notice there are two folders for Python 2 and Python 3 in the repository. 

```import iotawrapper.py```

and initialize the node server URL

```iota = iotawrapper.Api("http://localhost:14265/")```

*If you want to use a public node add the public server url instead of localhost. You find a list of public nodes on [IOTA Support Public Node](http://www.iotasupport.com/lightwallet.shtml). Consider that some public nodes do not allow operations like add or remove neighbors. The API returns a 401 error in that case.*

The API wrapper library offers the following operations:

* iota.getNodeInfo()
* iota.getNeighbors()
* iota.addNeighbors(neighborsList)
* iota.removeNeighbors(neighborsList)
* iota.getTips()
* iota.findTransactions(addressesList)
* iota.getTrytes(hashesList)
* iota.getInclusionStates(transactionsList, tipsList)
* iota.getBalance(addressesList, threshold)
* iota.getTransactionsToApprove(depth)
* iota.attachToTangle(trunkTransaction, branchTransaction, minWeightMagnitude, trytesList)
* iota.interruptAttachingToTangle()
* iota.broadcastTransactions(trytesList)
* iota.storeTransactions(trytesList)


## Example

If you need a single node information you can use this approach

```
appName = iota.getNodeInfo().appName()
```

If you need more information from a node, better use this more efficient approach
```
node = iota.getNodeInfo()
appName = node.appName()
appVersion = node.appVersion()
```

*The package included file test.py shows all possible examples.*
