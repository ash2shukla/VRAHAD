from bigchaindb_driver import BigchainDB
from os import urandom
from hashlib import sha256
from bigchaindb_driver.crypto import generate_keypair

bdb_root_url = 'http://localhost:59984/'

bdb = BigchainDB(bdb_root_url)

def putonBlockChain(record, Hi, GUi):
	recordID = sha256(urandom(16)).hexdigest()
	# Define Asset
	record_asset = {
		'data': {
		'recordID':recordID,
		'report': record
		},
	}
	patient = generate_keypair()

	record_asset_metadata = {'HID': Hi}
	prepared_creation_tx = bdb.transactions.prepare(
	operation='CREATE',
	signers=patient.public_key,
	asset=record_asset,
	metadata=record_asset_metadata
	)

	fulfilled_creation_tx = bdb.transactions.fulfill(
		prepared_creation_tx,
		private_keys=patient.private_key
	)

	sent_creation_tx = bdb.transactions.send(fulfilled_creation_tx)

	txid = fulfilled_creation_tx['id']

	trials = 0
	while trials < 60:
		try:
			if bdb.transactions.status(txid).get('status') == 'valid':
				print('Tx valid in:', trials, 'secs')
				break
		except bigchaindb_driver.exceptions.NotFoundError:
			trials += 1
			sleep(1)

	if trials == 60:
		print('Tx is still being processed... Bye!')
		exit(0)
	return txid

def findRecord(txid):
	print(bdb.transactions.retrieve(txid))
