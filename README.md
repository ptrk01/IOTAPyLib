# IOTAPyLib

IOTAPyLib is an easy to use wrapper for IOTA API written in Python. It is lightweight and offers all basic functionality of IOTA.

##Prerequisites

Requires Python 2.7 or higher.

##Usage

To use the library simply import *iotawrapper.py*

```import iotawrapper.py```

and initialize the node server URL

```iota = iotawrapper.Api("http://localhost:14265/")```

*If you want to use a public node add the public server url instead of localhost. You can find a list of public notes on [IOTA Support Public Node](http://www.iotasupport.com/lightwallet.shtml). Consider that some public nodes do not allow operations like add or remove neighbors. The API then returns a 401 error.*

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


##Example

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