import lxml.etree as etree
from getInformation import getSkey,getCertificate,encryptPid,encryptHmac
from hashlib import sha256

def createNode(nodeName, elements, values,text = None):
	'''
	Creates one XML node for given elements and their values and the text.
	'''
	node = etree.Element(nodeName)
	for i,j in zip(elements,values):
		if j is not None:
			node.set(i,j)
	if text is not None:
		node.text = text
	return node

def prepareRequest(Auth = {},Uses = {},Tkn = {},Meta = {},Skey = {},Data = {},\
					Demo = {},Pid = {},Pi = {},Pa = {},Pfa = {},Bios = {},Pv = {},\
					aua="TEST_CENTER",is_asa_cert=False,dtype="X",skey="",EncSkey=""):
	'''
	Creates the request Auth XML bytes.
	'''

	AuthNode = createNode('Auth',Auth.keys(),Auth.values())
	UsesNode = createNode('Uses',Uses.keys(),Uses.values())
	TknNode = createNode('Tkn',Tkn.keys(),Tkn.values())
	MetaNode = createNode('Meta', Meta.keys(),Meta.values())
	SkeyNode = createNode('Skey',Skey.keys(),Skey.values(),EncSkey)
	DataNode = createNode('Data',Data.keys(),Data.values())
	PidNode = createNode('Pid',Pid.keys(),Pid.values())
	DemoNode = createNode('Demo',Demo.keys(),Demo.values())
	PiNode = createNode('Pi',Pi.keys(),Pi.values())
	PaNode = createNode('Pa',Pa.keys(),Pa.values())
	PfaNode = createNode('Pfa',Pfa.keys(),Pfa.values())
	PvNode = createNode('Pv',Pv.keys(),Pv.values())
	BiosNode = createNode('Bios',[],[])

	if not is_asa_cert:
		SignatureNode = createNode('Signature',[],[],getCertificate('raw'))
	else:
		SignatureNode = createNode('Signature',[],[])

	for i,lst in zip(Bios.keys(),Bios.values()):
		for j,k in lst:
			BiosNode.append(createNode('Bio',["type","posh"],[i,j],k))


	AuthNode.append(UsesNode)
	AuthNode.append(TknNode)
	AuthNode.append(MetaNode)
	AuthNode.append(SkeyNode)

	DemoNode.append(PiNode)
	DemoNode.append(PaNode)
	DemoNode.append(PfaNode)

	PidNode.append(DemoNode)
	PidNode.append(BiosNode)
	PidNode.append(PvNode)

	PidNodeBytes = etree.tostring(PidNode)
	EncryptedPid = encryptPid(PidNodeBytes)

	DataNode = createNode('Data',['type'],[dtype],EncryptedPid)

	AuthNode.append(DataNode)

	PidHmac = sha256(PidNodeBytes).digest()
	HmacNode = createNode('Hmac',[],[],encryptHmac(skey,PidHmac))

	AuthNode.append(HmacNode)
	AuthNode.append(SignatureNode)
	return etree.tostring(AuthNode)
