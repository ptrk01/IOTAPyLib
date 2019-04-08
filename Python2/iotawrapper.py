# The software is released under MIT License.
#
# Copyright 2017 github.com/ptrk01
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
# documentation files (the "Software"), to deal in the Software # without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and
# to permit persons to whom the Software is furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all copies or substantial portions 
# of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
# THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A #PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF 
# CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER 
# DEALINGS IN THE SOFTWARE.
#
# Notice: Some parts of the class comments were taken from iota.readme.io.

import urllib2
import json
import sys

class Api:
    """ This class acts as an intermediary and invoker for all classes. """
    
    def __init__(self, url):
        self.url = url

    def getNodeInfo(self):
        return NodeInfo(self.url)
    
    def getNeighbors(self):
        return GetNeighbors(self.url)
    
    def addNeighbors(self, neighborsList):
        return AddNeighbors(self.url, neighborsList)
    
    def removeNeighbors(self, neighborsList):
        return RemoveNeighbors(self.url, neighborsList)
    
    def getTips(self):
        return GetTips(self.url)

    def findTransactions(self, addressesList):
        return FindTransactions(self.url, addressesList)

    def getTrytes(self, hashesList):
        return GetTrytes(self.url, hashesList)
    
    def getInclusionStates(self, transactionsList, tipsList):
        return GetInclusionStates(self.url, transactionsList, tipsList)
    
    def getBalance(self, addressesList, threshold):
        return GetBalance(self.url, addressesList, threshold)
    
    def getTransactionsToApprove(self, depth):
        return GetTransactionsToApprove(self.url, depth)
    
    def attachToTangle(self, trunkTransaction, branchTransaction, minWeightMagnitude, trytesList):
        return AttachToTangle(self.url, trunkTransaction, branchTransaction, minWeightMagnitude, trytesList)
    
    def interruptAttachingToTangle(self):
        return InterruptAttachingToTangle(self.url)
    
    def broadcastTransactions(self, trytesList):
        return BroadcastTransactions(self.url, trytesList)
    
    def storeTransactions(self, trytesList):
        return StoreTransactions(self.url, trytesList)


class StoreTransactions:
    """ Store transactions into the local storage. The trytes to be used for this call are returned by attachToTangle.

        Constructor:
            url (str): URL of node sever including port
            trytes (array of strings): List of raw data of transactions to be rebroadcast.
    
        Methods:
            duration: Duration of request.
            jsonResponse: Return the complete JSON response.
    """
    
    def __init__(self, url, trytesList):
        command = {'command': 'storeTransactions', 'trytes': [', '.join('{0}'.format(w) for w in trytesList)] if len(trytesList) > 0 else []}
        stringified = json.dumps(command)
        stringified = stringified.encode('utf-8')
        headers = {'content-type': 'application/json', 'X-IOTA-API-Version': '1'}
        request = urllib2.Request(url=url, data=stringified, headers=headers)
        try:
            returnData = urllib2.urlopen(request).read()
            self.jsonData = json.loads(returnData)
        except urllib2.HTTPError, e:
            sys.exit("%s in class: %s" % (str(e), self.__class__.__name__))
    
    def duration(self):
        return self.jsonData["duration"]

    def jsonResponse(self):
        return self.jsonData

class BroadcastTransactions:
    """ Broadcast a list of transactions to all neighbors. The input trytes for this call are provided by attachToTangle.

        Constructor:
            url (str): URL of node sever including port
            trytes (array of strings): List of raw data of transactions to be rebroadcast.
    
        Methods:
            duration: Duration of request.
            jsonResponse: Return the complete JSON response.
    """
    
    def __init__(self, url, trytesList):
        command = {'command': 'broadcastTransactions', 'trytes': [', '.join('{0}'.format(w) for w in trytesList)] if len(trytesList) > 0 else []}
        stringified = json.dumps(command)
        stringified = stringified.encode('utf-8')
        headers = {'content-type': 'application/json', 'X-IOTA-API-Version': '1'}
        request = urllib2.Request(url=url, data=stringified, headers=headers)
        try:
            returnData = urllib2.urlopen(request).read()
            self.jsonData = json.loads(returnData)
        except urllib2.HTTPError, e:
            sys.exit("%s in class: %s" % (str(e), self.__class__.__name__))
    
    def duration(self):
        return self.jsonData["duration"]

    def jsonResponse(self):
        return self.jsonData

class InterruptAttachingToTangle:
    """ Interrupts and completely aborts the attachToTangle process.

        Constructor:
            url (str): URL of node sever including port
    
        Methods:
            jsonResponse: Return the complete JSON response.
    """
    
    def __init__(self, url):
        command = {'command': 'interruptAttachingToTangle'}
        stringified = json.dumps(command)
        stringified = stringified.encode('utf-8')
        headers = {'content-type': 'application/json', 'X-IOTA-API-Version': '1'}
        request = urllib2.Request(url=url, data=stringified, headers=headers)
        try:
            returnData = urllib2.urlopen(request).read()
            self.jsonData = json.loads(returnData)
        except urllib2.HTTPError, e:
            sys.exit("%s in class: %s" % (str(e), self.__class__.__name__))

    def jsonResponse(self):
        return self.jsonData

class AttachToTangle:
    """ Attaches the specified transactions (trytes) to the Tangle by doing Proof of Work. You need to supply branchTransaction as well as trunkTransaction 
            (basically the tips which you're going to validate and reference with this transaction) - both of which you'll get through the getTransactionsToApprove API call.
            The returned value is a different set of tryte values which you can input into broadcastTransactions and storeTransactions. 
            The returned tryte value, the last 243 trytes basically consist of the: trunkTransaction + branchTransaction + nonce. These are valid trytes which are then accepted by the network.

        Constructor:
            url (str): URL of node sever including port
            trunkTransaction (integer): Trunk transaction to approve.
            branchTransaction (str): Branch transaction to approve.
            minWeightMagnitude (integer): Proof of Work intensity. Minimum value is 18
            trytes (str): List of trytes (raw transaction data) to attach to the tangle.
    
        Methods:
            trytes: List of added trytes.
            jsonResponse: Return the complete JSON response.
    """
    
    def __init__(self, url, trunkTransaction, branchTransaction, minWeightMagnitude, trytesList):
        command = {'command': 'attachToTangle', 'trunkTransaction': trunkTransaction, 'branchTransaction': branchTransaction, 'minWeightMagnitude': minWeightMagnitude, 'trytes': [', '.join('{0}'.format(w) for w in trytesList)] if len(trytesList) > 0 else []}
        stringified = json.dumps(command)
        stringified = stringified.encode('utf-8')
        headers = {'content-type': 'application/json', 'X-IOTA-API-Version': '1'}
        request = urllib2.Request(url=url, data=stringified, headers=headers)
        try:
            returnData = urllib2.urlopen(request).read()
            self.jsonData = json.loads(returnData)
        except urllib2.HTTPError, e:
            sys.exit("%s in class: %s" % (str(e), self.__class__.__name__))
            
    def trytes(self):
        return self.jsonData["trytes"]

    def jsonResponse(self):
        return self.jsonData


class GetTransactionsToApprove:
    """ Tip selection which returns trunkTransaction and branchTransaction. The input value is depth, which basically determines how many bundles to go back to for finding the transactions to approve. 
        The higher your depth value, the more "babysitting" you do for the network (as you have to confirm more transactions).

        Constructor:
            url (str): URL of node sever including port
            depth (integer): Number of bundles to go back to determine the transactions for approval.
    
        Methods:
            trunkTransaction : The transaction of the trunk.
            branchTransaction: The transaction of the branch.
            duration: Duration of request.
            jsonResponse: Return the complete JSON response.
    """
    
    
    def __init__(self, url, depth):
        command = {'command': 'getTransactionsToApprove', 'depth': depth}
        stringified = json.dumps(command)
        stringified = stringified.encode('utf-8')
        headers = {'content-type': 'application/json', 'X-IOTA-API-Version': '1'}
        request = urllib2.Request(url=url, data=stringified, headers=headers)
        try:
            returnData = urllib2.urlopen(request).read()
            self.jsonData = json.loads(returnData)
        except urllib2.HTTPError, e:
            sys.exit("%s in class: %s" % (str(e), self.__class__.__name__))
            
    def trunkTransaction(self):
        return self.jsonData["trunkTransaction"]
    
    def branchTransaction(self):
        return self.jsonData["branchTransaction"]
    
    def duration(self):
        return self.jsonData["duration"]
    
    def jsonResponse(self):
        return self.jsonData


class GetBalance:
    """ Similar to getInclusionStates. It returns the confirmed balance which a list of addresses have at the latest confirmed milestone. 
        In addition to the balances, it also returns the milestone as well as the index with which the confirmed balance was determined. 
        The balances is returned as a list in the same order as the addresses were provided as input.

        Constructor:
            url (str): URL of node sever including port
            addressList (array of strings): List of addresses you want to get the confirmed balance from
            threshold (integer): Confirmation threshold, should be set to 100.
    
        Methods:
            balances : List of balances.
            references: The referencing tips.
            milestoneIndex: Index number of milestone.
            jsonResponse: Return the complete JSON response.
    """
    
    def __init__(self, url, addressesList, threshold):
        command = {'command': 'getBalances', 'addresses': [', '.join('{0}'.format(w) for w in addressesList)] if len(addressesList) > 0 else [], 'threshold' : threshold}
        stringified = json.dumps(command)
        stringified = stringified.encode('utf-8')
        headers = {'content-type': 'application/json', 'X-IOTA-API-Version': '1'}
        request = urllib2.Request(url=url, data=stringified, headers=headers)
        try:
            returnData = urllib2.urlopen(request).read()
            self.jsonData = json.loads(returnData)
        except urllib2.HTTPError, e:
            sys.exit("%s in class: %s" % (str(e), self.__class__.__name__))
            
    def balances(self):
        return self.jsonData["balances"]
    
    def references(self):
        return self.jsonData["references"]
    
    def milestoneIndex(self):
        return self.jsonData["milestoneIndex"]
    
    def duration(self):
        return self.jsonData["duration"]
    
    def jsonResponse(self):
        return self.jsonData


class GetInclusionStates:
    """ Get the inclusion states of a set of transactions. This is for determining if a transaction was accepted and confirmed by the network or not. 
        You can search for multiple tips (and thus, milestones) to get past inclusion states of transactions.
        This API call simply returns a list of boolean values in the same order as the transaction list you submitted, thus you get a true/false whether a transaction is confirmed or not.

        Constructor:
            url (str): URL of node sever including port
            transactionsList (array of strings): List of transactions you want to get the inclusion state for.
            tipsList (array of strings): List of tips (including milestones) you want to search for the inclusion state.
    
        Methods:
            states : Number of states.
            duration: Duration of request.
            jsonResponse: Return the complete JSON response.
    """
    
    def __init__(self, url, transactionsList, tipsList):
        command = {'command': 'getInclusionStates', 'transactions': [', '.join('{0}'.format(w) for w in transactionsList)] if len(transactionsList) > 0 else [], 'tips': [', '.join('{0}'.format(w) for w in tipsList)] if len(tipsList) > 0 else []}
        stringified = json.dumps(command)
        stringified = stringified.encode('utf-8')
        headers = {'content-type': 'application/json', 'X-IOTA-API-Version': '1'}
        request = urllib2.Request(url=url, data=stringified, headers=headers)
        try:
            returnData = urllib2.urlopen(request).read()
            self.jsonData = json.loads(returnData)
        except urllib2.HTTPError, e:
            sys.exit("%s in class: %s" % (str(e), self.__class__.__name__))
            
    def states(self):
        return self.jsonData["states"]
    
    def duration(self):
        return self.jsonData["duration"]
    
    def jsonResponse(self):
        return self.jsonData


class GetTrytes: 
    """ Returns the list of tips

        Constructor:
            url (str): URL of node sever including port
            hashesList (array of strings): List of transaction hashes of which you want to get trytes from.
    
        Methods:
            trytes : List of trytes.
            jsonResponse: Return the complete JSON response.
    """
    
    
    def __init__(self, url, hashesList):
        command = {'command': 'getTrytes', 'hashes': [', '.join('{0}'.format(w) for w in hashesList)] if len(hashesList) > 0 else []}
        stringified = json.dumps(command)
        stringified = stringified.encode('utf-8')
        headers = {'content-type': 'application/json', 'X-IOTA-API-Version': '1'}
        request = urllib2.Request(url=url, data=stringified, headers=headers)
        try:
            returnData = urllib2.urlopen(request).read()
            self.jsonData = json.loads(returnData)
        except urllib2.HTTPError, e:
            sys.exit("%s in class: %s" % (str(e), self.__class__.__name__))
            
    def trytes(self):
        return self.jsonData["trytes"]
    
    def jsonResponse(self):
        return self.jsonData
        
class FindTransactions:
    """ Find the transactions which match the specified input and return. All input values are lists, for which a list of return values (transaction hashes), in the same order, is returned for all individual elements. 
        The input fields can either be bundles, addresses, tags or approvees. Using multiple of these input fields returns the intersection of the values.
        
        NOTICE: Only finding transactions by addresses is implemented. Searching by bundles, tags or approvees still needs to be implemented.

        Constructor:
            url (str): URL of node sever including port
            addressesList (array of strings): List of addresses.
    
        Methods:
            hashes: List of hashes.
            duration: Duration of request.
            jsonResponse: Return the complete JSON response.
    """
    
    def __init__(self, url, addressesList):
        command = {'command': 'findTransactions', 'addresses': [', '.join('{0}'.format(w) for w in addressesList)] if len(addressesList) > 0 else []}
        stringified = json.dumps(command)
        stringified = stringified.encode('utf-8')
        headers = {'content-type': 'application/json', 'X-IOTA-API-Version': '1'}
        request = urllib2.Request(url=url, data=stringified, headers=headers)
        try:
            returnData = urllib2.urlopen(request).read()
            self.jsonData = json.loads(returnData)
        except urllib2.HTTPError, e:
            sys.exit("%s in class: %s" % (str(e), self.__class__.__name__))
            
    def hashes(self):
        return self.jsonData["hashes"]
    
    def duration(self):
        return self.jsonData["duration"]
    
    def jsonResponse(self):
        return self.jsonData

class GetNeighbors:
    """ Returns the set of neighbors you are connected with, as well as their activity count. The activity counter is reset after restarting IRI.

        Constructor:
            url (str): URL of node sever including port
    
        Methods:
            address : address of your peer
            numberOfAllTransactions: Number of all transactions sent (invalid, valid, already-seen)
            numberOfInvalidTransactions: Invalid transactions your peer has sent you. These are transactions with invalid signatures or overall schema.
            numberOfNewTransactions: New transactions which were transmitted.
            jsonResponse: Return the complete JSON response.
    """
    
    
    def __init__(self, url):
        command = {'command': 'getNeighbors'}
        stringified = json.dumps(command)
        stringified = stringified.encode('utf-8')
        headers = {'content-type': 'application/json', 'X-IOTA-API-Version': '1'}
        request = urllib2.Request(url=url, data=stringified, headers=headers)
        try:
            returnData = urllib2.urlopen(request).read()
            self.jsonData = json.loads(returnData)
        except urllib2.HTTPError, e:
            sys.exit("%s in class: %s" % (str(e), self.__class__.__name__))
        
    def address(self):
        return self.jsonData["address"]

    def numberOfAllTransactions(self):
        return self.jsonData["numberOfAllTransactions"]
    
    def numberOfInvalidTransactions(self):
        return self.jsonData["numberOfInvalidTransactions"]

    def numberOfNewTransactions(self):
        return self.jsonData["numberOfNewTransactions"]
    
    def jsonResponse(self):
        return self.jsonData
    
class AddNeighbors:
    """ Add a list of neighbors to your node. It should be noted that this is only temporary, and the added neighbors will be removed from your set of neighbors after you relaunch IRI.
        The URI (Unique Resource Identification) for adding neighbors is: udp://IPADDRESS:PORT

        Constructor:
            url (str): URL of node sever including port
            neighborsList (array of strings): List of neighbor URI elements which should be added.
    
        Methods:
            addedNeighbors: List of added neighbor URI elements.
            duration: Duration of request.
            jsonResponse: Return the complete JSON response.
    """
    
    def __init__(self, url, neighborsList):
        command = {'command': 'addNeighbors', 'uris': [', '.join("'{0}'".format(w) for w in neighborsList)] if len(neighborsList) > 0 else []}
        stringified = json.dumps(command)
        stringified = stringified.encode('utf-8')
        headers = {'content-type': 'application/json', 'X-IOTA-API-Version': '1'}
        request = urllib2.Request(url=url, data=stringified, headers=headers)
        try:
            returnData = urllib2.urlopen(request).read()
            self.jsonData = json.loads(returnData)
        except urllib2.HTTPError, e:
            sys.exit("%s in class: %s" % (str(e), self.__class__.__name__))
        
    def addedNeighbors(self):
        return self.jsonData["addedNeighbors"]

    def duration(self):
        return self.jsonData["duration"]

    def jsonResponse(self):
        return self.jsonData


class RemoveNeighbors:
    """ Removes a list of neighbors to your node. This is only temporary, and if you have your neighbors added via the command line, they will be retained after you restart your node.
        The URI (Unique Resource Identification) for adding neighbors is: udp://IPADDRESS:PORT

        Constructor:
            url (str): URL of node sever including port
            neighborsList (array of strings): List of neighbor URI elements which should be removed.
    
        Methods:
            removeNeighbors: List of removed neighbor URIs elements.
            duration: Duration of request.
            jsonResponse: Return the complete JSON response.
    """
    
    
    def __init__(self, url, neighborsList):
        command = {'command': 'removeNeighbors', 'uris': [', '.join('{0}'.format(w) for w in neighborsList)] if len(neighborsList) > 0 else []}
        stringified = json.dumps(command)
        stringified = stringified.encode('utf-8')
        headers = {'content-type': 'application/json', 'X-IOTA-API-Version': '1'}
        request = urllib2.Request(url=url, data=stringified, headers=headers)
        try:
            returnData = urllib2.urlopen(request).read()
            self.jsonData = json.loads(returnData)
        except urllib2.HTTPError, e:
            sys.exit("%s in class: %s" % (str(e), self.__class__.__name__))
        
    def removedNeighbors(self):
        return self.jsonData["removedNeighbors"]

    def duration(self):
        return self.jsonData["duration"]

    def jsonResponse(self):
        return self.jsonData


class GetTips:
    """ Returns the list of tips.

        Constructor:
            url (str): URL of node sever including port
    
        Methods:
            hashes: List of tips hashes.
            duration: Duration of request.
            jsonResponse: Return the complete JSON response.
    """
    
    def __init__(self, url):
        command = {'command': 'getTips'}
        stringified = json.dumps(command)
        stringified = stringified.encode('utf-8')
        headers = {'content-type': 'application/json', 'X-IOTA-API-Version': '1'}
        request = urllib2.Request(url=url, data=stringified, headers=headers)
        try:
            returnData = urllib2.urlopen(request).read()
            self.jsonData = json.loads(returnData)
        except urllib2.HTTPError, e:
            sys.exit("%s in class: %s" % (str(e), self.__class__.__name__))
        
    def hashes(self):
        return self.jsonData["hashes"]

    def duration(self):
        return self.jsonData["duration"]

    def jsonResponse(self):
        return self.jsonData


class NodeInfo:
    """ Returns information about your node.

        Constructor:
            url (str): URL of node sever including port
    
        Methods:
            appName: Name of the IOTA software you're currently using (IRI stands for Initial Reference Implementation).
            appVersion: The version of the IOTA software you're currently running.
            jreAvailableProcesses: Available cores on your machine for JRE.
            jreFreeMemory: Returns the amount of free memory in the Java Virtual Machine.
            jreMaxMemory: Returns the maximum amount of memory that the Java virtual machine will attempt to use.
            jreTotalMemory: Returns the total amount of memory in the Java virtual machine.
            latestMilestone: Latest milestone that was signed off by the coordinator.
            latestMilestoneIndex: Index of the latest milestone.
            latestSolidSubtangleMilestone: The latest milestone which is solid and is used for sending transactions. For a milestone to become solid your local node must basically approve the subtangle of coordinator-approved transactions, and have a consistent view of all referenced transactions.
            latestSolidSubtangleMilestoneIndex: Index of the latest solid subtangle.
            neighbors: Number of neighbors you are directly connected with.
            packetsQueueSize: Packets which are currently queued up.
            milestoneStartIndex: Entrypoint milestone for the current version of the IRI
            time: Current UNIX timestamp.
            tips: Number of tips in the network.
            transactionsToRequest: Transactions to request during syncing process.
            jsonResponse: Return the complete JSON response.
            features: Enabled commands
            coordinatorAddress: Address of the Coordinator
            duration: Number of milliseconds it took to complete the request
    """
    
    def __init__(self, url):
        command = {'command': 'getNodeInfo'}
        stringified = json.dumps(command)
        stringified = stringified.encode('utf-8')
        headers = {'content-type': 'application/json', 'X-IOTA-API-Version': '1'}
        request = urllib2.Request(url=url, data=stringified, headers=headers)
        try:
            returnData = urllib2.urlopen(request).read()
            self.jsonData = json.loads(returnData)
        except urllib2.HTTPError, e:
            sys.exit("%s in class: %s" % (str(e), self.__class__.__name__))
        
    def appName(self):
        return self.jsonData["appName"]

    def neighbors(self):
        return self.jsonData["neighbors"]
    
    def appVersion(self):
        return self.jsonData["appVersion"]

    def jreAvailableProcessors(self):
        return self.jsonData["jreAvailableProcessors"]

    def jreFreeMemory(self):
        return self.jsonData["jreFreeMemory"]

    def jreMaxMemory(self):
        return self.jsonData["jreMaxMemory"]

    def jreTotalMemory(self):
        return self.jsonData["jreTotalMemory"]

    def latestMilestone(self):
        return self.jsonData["latestMilestone"]

    def latestMilestoneIndex(self):
        return self.jsonData["latestMilestoneIndex"]

    def latestSolidSubtangleMilestone(self):
        return self.jsonData["latestSolidSubtangleMilestone"]
    
    def milestoneStartIndex(self):
        return self.jsonData["milestoneStartIndex"]


    def latestSolidSubtangleMilestoneIndex(self):
        return self.jsonData["latestSolidSubtangleMilestoneIndex"]
    
    def packetsQueueSize(self):
        return self.jsonData["packetsQueueSize"]

    def time(self):
        return self.jsonData["time"]

    def tips(self):
        return self.jsonData["tips"]
    
    def transactionsToRequest(self):
        return self.jsonData["transactionsToRequest"]
    
    def coordinatorAddress(self):
        return self.jsonData["coordinatorAddress"]
    
    def features(self):
        return self.jsonData["features"]
    
    def transactionsToRequest(self):
        return self.jsonData["transactionsToRequest"]
    
    def duration(self):
        return self.jsonData["duration"]
    
    def jsonResponse(self):
        return self.jsonData
