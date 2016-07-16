

import sys, random, threading, webbrowser
from flask import Flask, render_template, redirect, request
import shelve
shelve = shelve.open('ucsshelve')

def rangeexpand(txt):
    lst = []
    for r in txt.split(','):
        if '-' in r[1:]:
            r0, r1 = r[1:].split('-', 1)
            lst += range(int(r[0] + r0), int(r1) + 1)
        else:
            lst.append(str(r))
    return lst
	
def add(a,b):
	if a + b < 10:
		return a + b
	elif a + b == 10:
		return "A"
	elif a + b == 11:
		return "B"
	elif a + b == 12:
		return "C"		
	elif a + b == 13:
		return "D"
	elif a + b == 14:
		return "E"
	elif a + b == 15:
		return "F"

app = Flask(__name__)
@app.route('/configureucs', methods = ['POST'])
def configureucs():
	ipaddress = request.form['ipaddress']
	username = request.form['username']
	password = request.form['password']	
	shelve['ipaddress'] = ipaddress
	shelve['username'] = username
	shelve['password'] = password
	
	#Login to UCS
	handle = UcsHandle()
	handle.Login(ipaddress, username, password, noSsl=True, port=80, dumpXml=YesOrNo.FALSE)


	#Global Configuration Settings

	"""
	# DNS Configuration
		dnsserver = request.form['dnsserver']
		dnsserver2 = request.form['dnsserver2']
		if dnsserver != "":
			obj = handle.GetManagedObject(None, CommDns.ClassId(), {CommDns.DN:"sys/svc-ext/dns-svc"})
			handle.AddManagedObject(obj, CommDnsProvider.ClassId(),
			{CommDnsProvider.DN:"sys/svc-ext/dns-svc/dns-',dnsserver,",	
			CommDnsProvider.NAME:dnsserver})
		if dnsserver2 != "":	
			obj = handle.GetManagedObject(None, CommDns.ClassId(), {CommDns.DN:"sys/svc-ext/dns-svc"})
			handle.AddManagedObject(obj, CommDnsProvider.ClassId(),
			{CommDnsProvider.DN:"sys/svc-ext/dns-svc/dns-',dnsserver2,",	
			CommDnsProvider.NAME:dnsserver2})
		
	#NTP Configuration
			ntpserver = request.form['ntpserver']
			if ntpserver != "":
				obj = handle.GetManagedObject(None, CommDateTime.ClassId(),
				{CommDateTime.DN:"sys/svc-ext/datetime-svc"})
				handle.AddManagedObject(obj, CommNtpProvider.ClassId(),
				{CommNtpProvider.NAME:ntpserver,
				CommNtpProvider.DN:"sys/svc-ext/datetime-svc/ntp-',ntpserver,"})
	
	#Time Zone Configuration
			timezonex = request.form['timezone']	
			obj = handle.GetManagedObject(None, CommDateTime.ClassId(),
			{CommDateTime.DN:"sys/svc-ext/datetime-svc"})
			handle.SetManagedObject(obj, CommDateTime.ClassId(),
			{CommDateTime.ADMIN_STATE:"enabled",
			CommDateTime.TIMEZONE:timezonex})

	# Uplink Ports

			uplinkrange = request.form['uplinkrange']
			uplinkChannelA = request.form['channelA']
			uplinkChannelB = request.form['channelB']
			handle.StartTransaction()
			obj = handle.GetManagedObject(None, None, {"Dn":"fabric/lan/A"})
			mo = handle.AddManagedObject(obj, "fabricEthLanPc", {"AdminSpeed":"10gbps", "Descr":"", "OperSpeed":"10gbps",
			"Name":"", "FlowCtrlPolicy":"default", "AdminState":"enabled", "Dn":"fabric/lan/A/pc-" +uplinkChannelA, "LacpPolicyName":"default"}, True)
			for x in rangeexpand(uplinkrange):	
				y = str(x)
				mo_1 = handle.AddManagedObject(mo, "fabricEthLanPcEp", {"EthLinkProfileName":"default", "SlotId":"1", "AdminState":"enabled",
				"PortId":y, "Dn":"fabric/lan/A/pc-" + uplinkChannelA + "/ep-slot-1-port-" + y, "Name":""})
				
			obj = handle.GetManagedObject(None, None, {"Dn":"fabric/lan/B"})
			mo = handle.AddManagedObject(obj, "fabricEthLanPc", {"AdminSpeed":"10gbps", "Descr":"", "OperSpeed":"10gbps",
			"Name":"", "FlowCtrlPolicy":"default", "AdminState":"enabled", "Dn":"fabric/lan/B/pc-" +uplinkChannelB, "LacpPolicyName":"default"}, True)
			for x in rangeexpand(uplinkrange):	
				y = str(x)
				mo_1 = handle.AddManagedObject(mo, "fabricEthLanPcEp", {"EthLinkProfileName":"default", "SlotId":"1", "AdminState":"enabled",
				"PortId":y, "Dn":"fabric/lan/B/pc-" + uplinkChannelB + "/ep-slot-1-port-" + y, "Name":""})			
			handle.CompleteTransaction()

	# Create Chassis Discovery Policy
			chassisdicover = request.form['yesno']
			if chassisdicover == 'Yes':	
				handle.StartTransaction()
				obj = handle.GetManagedObject(None, OrgOrg.ClassId(),
				{OrgOrg.DN:"org-root"})
				handle.AddManagedObject(obj, ComputeChassisDiscPolicy.ClassId(),
				{ComputeChassisDiscPolicy.REBALANCE:
				"user-acknowledged",
				ComputeChassisDiscPolicy.DN:
				"org-root/chassis-discovery",
				ComputeChassisDiscPolicy.ACTION:
				"2-link",
				ComputeChassisDiscPolicy.LINK_AGGREGATION_PREF:
				"port-channel"}
				,True)
				handle.CompleteTransaction()
	
	
	"""
	
#Create Sub Organization
	OrgName = request.form['OrgName']
	shelve['OrgName'] = OrgName
	obj = handle.GetManagedObject(None,OrgOrg.ClassId(),{OrgOrg.DN:"org-root"})
	handle.AddManagedObject(obj, OrgOrg.ClassId(),
	{OrgOrg.NAME:OrgName,OrgOrg.DN:"org-root/org-',OrgName,"})
		
# Maintenance Policy
	maintpolicyname = request.form['maintpolicy']
	shelve['maintpolicyname'] = maintpolicyname
	handle.StartTransaction()
	orgdnmaint	= 'org-root/org-' + OrgName + '/maint-' + maintpolicyname
	obj = handle.GetManagedObject(None, OrgOrg.ClassId(), {OrgOrg.DN:"org-root"})
	handle.AddManagedObject(obj, LsmaintMaintPolicy.ClassId(),
	{LsmaintMaintPolicy.UPTIME_DISR:"user-ack",
	LsmaintMaintPolicy.DN:orgdnmaint,
	LsmaintMaintPolicy.NAME:maintpolicyname})
	handle.CompleteTransaction()

#Create BIOS Policy
	BiosPolicyName = request.form['bios']
	shelve['BiosPolicyName'] = BiosPolicyName
	handle.StartTransaction()
	obj = handle.GetManagedObject(None, None, {"Dn":"org-root/',OrgName,"})
	mo = handle.AddManagedObject(obj, "biosVProfile", {"PolicyOwner":"local", "RebootOnUpdate":"no",
	"Dn":"org-root/org-" + OrgName + "/bios-prof-" + BiosPolicyName, "Name": BiosPolicyName, "Descr":""})
	mo_1 = handle.AddManagedObject(mo, "biosVfQuietBoot", {"Dn":"org-root/org-" + OrgName + "/bios-prof-" + BiosPolicyName + "/Quiet-Boot",
	"VpQuietBoot":"disabled"}, True)
	handle.CompleteTransaction()
	

# Boot Policy
	LocalBootPolicyName = request.form['LocalBootPolicyName']
	shelve['LocalBootPolicyName'] = LocalBootPolicyName
	SanBootPolicyName = request.form['SanBootPolicyName']
	shelve['SanBootPolicyName'] = SanBootPolicyName
	if SanBootPolicyName != "":
		obj = handle.GetManagedObject(None, None, {"Dn":"org-root/org-',OrgName,"})
		mo = handle.AddManagedObject(obj, "lsbootPolicy", {"RebootOnUpdate":"no", "BootMode":"legacy", "Descr":"", "PolicyOwner":"local",
		"EnforceVnicName":"yes", "Dn":"org-root/org-" + OrgName + "/boot-policy-',SanBootPolicyName,", "Name":SanBootPolicyName})
		mo_1 = handle.AddManagedObject(mo, "lsbootVirtualMedia", {"Order":"1", "MappingName":"", "Access":"read-only-local",
		"Dn":"org-root/org-" + OrgName + "/boot-policy-" + SanBootPolicyName + "/read-only-local-vm", "LunId":"0"})
		mo_2 = handle.AddManagedObject(mo, "lsbootSan", {"Dn":"org-root/org-" + OrgName + "/boot-policy-" + SanBootPolicyName + "/san", "Order":"2"}, True)
		mo_2_1 = handle.AddManagedObject(mo_2, "lsbootSanCatSanImage", {"Type":"primary",
		"Dn":"org-root/org-" + OrgName + "/boot-policy-" + SanBootPolicyName + "/san/sanimg-primary", "VnicName":"fc0"})
		mo_2_1_1 = handle.AddManagedObject(mo_2_1, "lsbootSanCatSanImagePath", {"Type":"primary", "Wwn":"20:00:00:00:00:00:00:00",
		"Dn":"org-root/org-" + OrgName + "/boot-policy-" + SanBootPolicyName + "/san/sanimg-primary/sanimgpath-primary", "Lun":"0"})
		mo_2_1_2 = handle.AddManagedObject(mo_2_1, "lsbootSanCatSanImagePath", {"Type":"secondary", "Wwn":"20:00:00:00:00:00:00:00",
		"Dn":"org-root/org-" + OrgName + "/boot-policy-" + SanBootPolicyName + "/san/sanimg-primary/sanimgpath-secondary", "Lun":"0"})
		mo_2_2 = handle.AddManagedObject(mo_2, "lsbootSanCatSanImage", {"Type":"secondary",
		"Dn":"org-root/org-" + OrgName + "/boot-policy-" + SanBootPolicyName + "/san/sanimg-secondary", "VnicName":"fc1"})
		mo_2_2_1 = handle.AddManagedObject(mo_2_2, "lsbootSanCatSanImagePath", {"Type":"primary", "Wwn":"20:00:00:00:00:00:00:00",
		"Dn":"org-root/org-" + OrgName + "/boot-policy-" + SanBootPolicyName + "/san/sanimg-secondary/sanimgpath-primary", "Lun":"0"})
		mo_2_2_2 = handle.AddManagedObject(mo_2_2, "lsbootSanCatSanImagePath", {"Type":"secondary", "Wwn":"20:00:00:00:00:00:00:00",
		"Dn":"org-root/org-" + OrgName + "/boot-policy-" + SanBootPolicyName + "/san/sanimg-secondary/sanimgpath-secondary", "Lun":"0"})
		handle.CompleteTransaction()
		
	if LocalBootPolicyName != "":
		handle.StartTransaction()
		obj = handle.GetManagedObject(None, None, {"Dn":"org-root/org-',OrgName,"})
		mo = handle.AddManagedObject(obj, "lsbootPolicy", {"RebootOnUpdate":"no", "BootMode":"legacy", "Descr":"", "PolicyOwner":"local",
		"EnforceVnicName":"yes", "Dn":"org-root/org-" + OrgName + "/boot-policy-" + LocalBootPolicyName, "Name":LocalBootPolicyName})
		mo_1 = handle.AddManagedObject(mo, "lsbootVirtualMedia", {"Order":"2", "MappingName":"", "Access":"read-only",
		"Dn":"org-root/org-" + OrgName + "/boot-policy-" + LocalBootPolicyName + "/read-only-vm", "LunId":"0"})
		mo_2 = handle.AddManagedObject(mo, "lsbootStorage",
		{"Dn":"org-root/org-" + OrgName + "/boot-policy-" + LocalBootPolicyName + "/storage", "Order":"1"})
		mo_2_1 = handle.AddManagedObject(mo_2, "lsbootLocalStorage", {"Dn":"org-root/org-" + OrgName + "/boot-policy-" + LocalBootPolicyName + "/storage/local-storage"})
		mo_2_1_1 = handle.AddManagedObject(mo_2_1, "lsbootDefaultLocalImage",
		{"Dn":"org-root/org-" + OrgName + "/boot-policy-" + LocalBootPolicyName + "/storage/local-storage/local-any", "Order":"1"})
		handle.CompleteTransaction()


	# Configure CIMC Management IPs

	cimc_name = request.form['cimc_name']	
	cimc_start = request.form['cimc_start']
	cimc_end = request.form['cimc_end']
	cimc_mask = request.form['cimc_mask']	
	cimc_gw = request.form['cimc_gw']
	if cimc_name != "":
		orgdnx = 'org-root/org-' + OrgName + '/'
		orgdnx2 = 'org-root/org-' + OrgName + '/ip-pool-' + cimc_name
		orgndx3 = 'org-root/org-' + OrgName + '/ip-pool-' + cimc_name + '/block-' + cimc_start + '-' + cimc_end
		handle.StartTransaction()
		obj = handle.GetManagedObject(None, None, {"Dn":orgdnx})
		mo=handle.AddManagedObject(obj, "ippoolPool", 
		{"AssignmentOrder":"sequential", "Descr":"", "PolicyOwner":"local", "IsNetBIOSEnabled":"disabled",
		"Name":cimc_name, "Guid":"", "Dn":orgdnx2, "ExtManaged":"internal", "SupportsDHCP":"disabled"})
		mo_1 = handle.AddManagedObject(mo, "ippoolBlock", {"To":cimc_end,
		"Dn":orgndx3,
		"From":cimc_start, "DefGw":cimc_gw})
		handle.CompleteTransaction()	
	shelve['cimc_name'] = cimc_name
	
	# Configure VLANs
	vlanrange = request.form['vlanrange']
	for x in rangeexpand(vlanrange):		
		handle.StartTransaction()
		y = str(x)
		obj = handle.GetManagedObject(None, FabricLanCloud.ClassId(), {FabricLanCloud.DN:"fabric/lan"})
		handle.AddManagedObject(obj, FabricVlan.ClassId(),
		{FabricVlan.DN:"fabric/lan/net-" + y,
		FabricVlan.ID:y,
		FabricVlan.NAME:y})
		handle.CompleteTransaction()
	
# Create Mac Address, WWN, WWPN and UUID Pools
	os = request.form['os']
	TemplateType = request.form['TemplateType']
	if os == 'ESX':	
		MacPoolName = request.form['macpoolname']
		SiteID = request.form['siteid']
		DomainID = request.form['domainid']
		shelve['MacPoolName'] = MacPoolName
		shelve['SiteID'] = SiteID
		shelve['DomainID'] = DomainID
		
		macpoolnumberA = 0
		macpoolnumberB = 0
		wwnnpoolnumber = 0
		wwpnpoolnumbera = 0
		wwpnpoolnumberb = 0
		UUIDPoolNumber = 0

			
	#Create Mac Addres Pool for VMware Management on Fabric A	

		a = macpoolnumberA
		if a > 0:
			b = 1
		else:
			b = 0	
		macpoolnumberA = add(a,b)
		macpoolnumberA = str(macpoolnumberA)
		handle.StartTransaction()
		obj = handle.GetManagedObject(None, None, {"Dn":"org-root/org-',OrgName,"})
		mo = handle.AddManagedObject(obj, "macpoolPool", {"PolicyOwner":"local", "AssignmentOrder":"default",
		 "Dn":"org-root/org-" + OrgName + "/mac-pool-" + MacPoolName + "MGMT", "Name":MacPoolName + "MGMT", "Descr":""})
		mo_1 = handle.AddManagedObject(mo, "macpoolBlock", {"To":"00:25:B5:" + SiteID + DomainID + ":A" + macpoolnumberA +":FF", "From":"00:25:B5:" + SiteID + DomainID + ":A" + macpoolnumberA + ":00",
		 "Dn":"org-root/org-" + OrgName + "/mac-pool-" + MacPoolName + "MGMT/block-00:25:B5:" + SiteID + DomainID + ":A" + macpoolnumberA + ":00-00:25:B5:" + SiteID + DomainID + ":A" + macpoolnumberA + ":FF"})
		handle.CompleteTransaction()
		shelve['macpoolnumberA'] = macpoolnumberA
		macpoolnumberA = int(macpoolnumberA)
		
	#Create vNIC Template for VMware Managment Interface

		mgmtvnic =  os + TemplateType + "_MGMT"
		shelve['mgmtvnic'] = mgmtvnic
		vlanrange = request.form['vlanmgmt']
		handle.StartTransaction()
		obj = handle.GetManagedObject(None, None, {"Dn":"org-root/org-' ,OrgName, "})
		mo = handle.AddManagedObject(obj, "vnicLanConnTempl", {"IdentPoolName":MacPoolName + "MGMT",
		 "Dn":"org-root/org-" + OrgName + "/lan-conn-templ-"+ mgmtvnic, "QosPolicyName":"",
		 "Descr":"", "PolicyOwner":"local", "NwCtrlPolicyName":"", "TemplType":"initial-template",
		 "StatsPolicyName":"default", "Mtu":"1500", "PinToGroupName":"", "Name":mgmtvnic, "SwitchId":"A"})
		handle.CompleteTransaction()
		
		handle.StartTransaction()
		obj = handle.GetManagedObject(None, None, {"Dn":"org-root/org-', OrgName, "})
		mo = handle.AddManagedObject(obj, "vnicLanConnTempl", {"IdentPoolName":MacPoolName + "MGMT",
		"Dn":"org-root/org-" + OrgName + "/lan-conn-templ-" + mgmtvnic,
		 "QosPolicyName":"", "Descr":"", "PolicyOwner":"local", "NwCtrlPolicyName":"", "TemplType":"initial-template",
		 "StatsPolicyName":"default", "Mtu":"1500", "PinToGroupName":"", "SwitchId":"A-B"}, True)
		for x in rangeexpand(vlanrange):		
			y = str(x)
			mo_1 = handle.AddManagedObject(mo, "vnicEtherIf", {"DefaultNet":"no", "Name":y,
			 "Dn":"org-root/org-" + OrgName + "/lan-conn-templ-" + mgmtvnic + "/if-" + y}, True)
		handle.CompleteTransaction()



	#Create Mac Addres Pool for vMotion on  Fabric B
		a = macpoolnumberB
		if a > 0:
			b = 1
		else:
			b = 0		
		macpoolnumberB = add(a,b)
		macpoolnumberB = str(macpoolnumberB)
		MacPoolNamevMotion = MacPoolName + "_vMotion"
		handle.StartTransaction()
		obj = handle.GetManagedObject(None, None, {"Dn":"org-root/org-',OrgName,"})
		mo = handle.AddManagedObject(obj, "macpoolPool", {"PolicyOwner":"local", "AssignmentOrder":"default",
		 "Dn":"org-root/org-" + OrgName + "/mac-pool-" + MacPoolNamevMotion, "Name":MacPoolNamevMotion, "Descr":""})
		mo_1 = handle.AddManagedObject(mo, "macpoolBlock", {"To":"00:25:B5:" + SiteID + DomainID + ":B" + macpoolnumberB +":FF", "From":"00:25:B5:" + SiteID + DomainID + ":B" + macpoolnumberB + ":00",
		 "Dn":"org-root/org-" + OrgName + "/mac-pool-" + MacPoolNamevMotion + "/block-00:25:B5:" + SiteID + DomainID + ":B" + macpoolnumberB + ":00-00:25:B5:" + SiteID + DomainID + ":B" + macpoolnumberB + ":FF"})
		handle.CompleteTransaction()
		

	#Create vNIC Template for VMware vMotion 
		motionvnic = os + TemplateType + "_vMotion"
		shelve['motionvnic'] = motionvnic
		handle.StartTransaction()
		obj = handle.GetManagedObject(None, None, {"Dn":"org-root/org-' ,OrgName, "})
		mo = handle.AddManagedObject(obj, "vnicLanConnTempl", {"IdentPoolName":MacPoolNamevMotion,
		 "Dn":"org-root/org-" + OrgName + "/lan-conn-templ-"+ motionvnic, "QosPolicyName":"",
		 "Descr":"", "PolicyOwner":"local", "NwCtrlPolicyName":"", "TemplType":"initial-template",
		 "StatsPolicyName":"default", "Mtu":"1500", "PinToGroupName":"", "Name":motionvnic, "SwitchId":"B"})
		handle.CompleteTransaction()
		vlanrange = request.form['vlanmotion']
		handle.StartTransaction()
		obj = handle.GetManagedObject(None, None, {"Dn":"org-root/org-', OrgName, "})
		mo = handle.AddManagedObject(obj, "vnicLanConnTempl", {"IdentPoolName":MacPoolNamevMotion,
		"Dn":"org-root/org-" + OrgName + "/lan-conn-templ-" + motionvnic,
		 "QosPolicyName":"", "Descr":"", "PolicyOwner":"local", "NwCtrlPolicyName":"", "TemplType":"initial-template",
		 "StatsPolicyName":"default", "Mtu":"1500", "PinToGroupName":"", "SwitchId":"B-A"}, True)
		for x in rangeexpand(vlanrange):		
			y = str(x)
			mo_1 = handle.AddManagedObject(mo, "vnicEtherIf", {"DefaultNet":"no", "Name":y,
			 "Dn":"org-root/org-" + OrgName + "/lan-conn-templ-" + motionvnic + "/if-" + y}, True)
		handle.CompleteTransaction()
		shelve['macpoolnumberB'] = macpoolnumberB	
		macpoolnumberB = int(macpoolnumberB)				

	#Create Mac Addres Pool for Fabric A

		a = macpoolnumberA
		b = 1
		macpoolnumberA = add(a,b)		
		macpoolnumberA = str(macpoolnumberA)
		MacPoolNameESX = MacPoolName + TemplateType
		

		handle.StartTransaction()
		obj = handle.GetManagedObject(None, None, {"Dn":"org-root/org-',OrgName,"})
		mo = handle.AddManagedObject(obj, "macpoolPool", {"PolicyOwner":"local", "AssignmentOrder":"default",
		 "Dn":"org-root/org-" + OrgName + "/mac-pool-" + MacPoolNameESX + "A", "Name":MacPoolNameESX + "A", "Descr":""})
		mo_1 = handle.AddManagedObject(mo, "macpoolBlock", {"To":"00:25:B5:" + SiteID + DomainID + ":A" + macpoolnumberA +":FF", "From":"00:25:B5:" + SiteID + DomainID + ":A" + macpoolnumberA + ":00",
		 "Dn":"org-root/org-" + OrgName + "/mac-pool-" + MacPoolNameESX + "A/block-00:25:B5:" + SiteID + DomainID + ":A" + macpoolnumberA + ":00-00:25:B5:" + SiteID + DomainID + ":A" + macpoolnumberA + ":FF"})
		handle.CompleteTransaction()
		shelve['macpoolnumberA'] = macpoolnumberA
		macpoolnumberA = int(macpoolnumberA)
		
	#Create Mac Addres Pool for Fabric B

		a = macpoolnumberB
		b = 1
		macpoolnumberB = add(a,b)
		macpoolnumberB = str(macpoolnumberB)

		handle.StartTransaction()
		obj = handle.GetManagedObject(None, None, {"Dn":"org-root/org-',OrgName,"})
		mo = handle.AddManagedObject(obj, "macpoolPool", {"PolicyOwner":"local", "AssignmentOrder":"default",
		 "Dn":"org-root/org-" + OrgName + "/mac-pool-" + MacPoolNameESX + "B", "Name":MacPoolNameESX + "B", "Descr":""})
		mo_1 = handle.AddManagedObject(mo, "macpoolBlock", {"To":"00:25:B5:" + SiteID + DomainID + ":B" + macpoolnumberB + ":FF", "From":"00:25:B5:" + SiteID + DomainID + ":B" + macpoolnumberB + ":00",
		 "Dn":"org-root/org-" + OrgName + "/mac-pool-" + MacPoolNameESX + "B/block-00:25:B5:" + SiteID + DomainID + ":B" + macpoolnumberB + ":00-00:25:B5:" + SiteID + DomainID + ":B" + macpoolnumberB + ":FF"})
		handle.CompleteTransaction()
		shelve['macpoolnumberB'] = macpoolnumberB	
		macpoolnumberB = int(macpoolnumberB)

	#vNIC Template

	# Create vNIC Template for VMware Data Interfaces

		datavnic = os + TemplateType
		handle.StartTransaction()
		obj = handle.GetManagedObject(None, None, {"Dn":"org-root/org-' ,OrgName, "})
		mo = handle.AddManagedObject(obj, "vnicLanConnTempl", {"IdentPoolName":MacPoolNameESX + "A",
		 "Dn":"org-root/org-" + OrgName + "/lan-conn-templ-" + datavnic + "A", "QosPolicyName":"",
		 "Descr":"", "PolicyOwner":"local", "NwCtrlPolicyName":"", "TemplType":"initial-template",
		 "StatsPolicyName":"default", "Mtu":"1500", "PinToGroupName":"", "Name":datavnic + "A", "SwitchId":"A"})
		handle.CompleteTransaction()

		handle.StartTransaction()
		obj = handle.GetManagedObject(None, None, {"Dn":"org-root/org-' ,OrgName, "})
		mo = handle.AddManagedObject(obj, "vnicLanConnTempl", {"IdentPoolName":MacPoolNameESX + "B",
		 "Dn":"org-root/org-" + OrgName + "/lan-conn-templ-" + datavnic + "B", "QosPolicyName":"",
		 "Descr":"", "PolicyOwner":"local", "NwCtrlPolicyName":"", "TemplType":"initial-template",
		 "StatsPolicyName":"default", "Mtu":"1500", "PinToGroupName":"", "Name":datavnic + "B", "SwitchId":"B"})
		handle.CompleteTransaction()

		#Add VLANs for vNIC template 

		vlanrange = request.form['vlandata']
		handle.StartTransaction()
		obj = handle.GetManagedObject(None, None, {"Dn":"org-root/org-', OrgName, "})
		mo = handle.AddManagedObject(obj, "vnicLanConnTempl", {"IdentPoolName":MacPoolNameESX + "A",
		"Dn":"org-root/org-" + OrgName + "/lan-conn-templ-" + datavnic + "A",
		 "QosPolicyName":"", "Descr":"", "PolicyOwner":"local", "NwCtrlPolicyName":"", "TemplType":"initial-template",
		 "StatsPolicyName":"default", "Mtu":"1500", "PinToGroupName":"", "SwitchId":"A"}, True)
		for x in rangeexpand(vlanrange):		
			y = str(x)
			mo_1 = handle.AddManagedObject(mo, "vnicEtherIf", {"DefaultNet":"no", "Name":y,
			 "Dn":"org-root/org-" + OrgName + "/lan-conn-templ-" + datavnic + "A/if-" + y}, True)
		handle.CompleteTransaction()
			
		handle.StartTransaction()	
		obj = handle.GetManagedObject(None, None, {"Dn":"org-root/org-', OrgName, "})
		mo = handle.AddManagedObject(obj, "vnicLanConnTempl", {"IdentPoolName":MacPoolNameESX + "B",
		"Dn":"org-root/org-" + OrgName + "/lan-conn-templ-" + datavnic + "B",
		 "QosPolicyName":"", "Descr":"", "PolicyOwner":"local", "NwCtrlPolicyName":"", "TemplType":"initial-template",
		 "StatsPolicyName":"default", "Mtu":"1500", "PinToGroupName":"", "SwitchId":"B"}, True)
		for x in rangeexpand(vlanrange):		
			y = str(x)
			mo_1 = handle.AddManagedObject(mo, "vnicEtherIf", {"DefaultNet":"no", "Name":y,
			 "Dn":"org-root/org-" + OrgName + "/lan-conn-templ-" + datavnic + "B/if-" + y}, True)
		handle.CompleteTransaction()
		

	#Create WWNN Pool
		WWNPoolName = request.form['wwnnpoolname']
		shelve['WWNPoolName'] = WWNPoolName	
		WWNPoolName = WWNPoolName + os + TemplateType
		a = wwnnpoolnumber
		if a > 0:
			b = 1
		else:
			b = 0
		wwnnpoolnumber = add(a,b)
		wwnnpoolnumber = str(wwnnpoolnumber)
		handle.StartTransaction()
		obj = handle.GetManagedObject(None, None, {"Dn":"org-root/org-',OrgName,"})
		mo = handle.AddManagedObject(obj, "fcpoolInitiators", {"Descr":"", "PolicyOwner":"local", "AssignmentOrder":"default", 
		"Purpose":"node-wwn-assignment","Dn":"org-root/org-" + OrgName + "/wwn-pool-" + WWNPoolName, "Name":WWNPoolName})
		mo_1 = handle.AddManagedObject(mo, "fcpoolBlock", {"To":"20:00:00:25:B5:" + SiteID + DomainID + ":F" + wwnnpoolnumber + ":FF", "From":"20:00:00:25:B5:" + SiteID + DomainID + ":F" + wwnnpoolnumber + ":00",
		 "Dn":"org-root/org-" + OrgName + "/wwn-pool-" + WWNPoolName + "/block-20:00:00:25:B5:" + SiteID + DomainID + ":FF" + wwnnpoolnumber + ":00-20:00:00:25:B5:" + SiteID + DomainID + ":F" + wwnnpoolnumber + ":FF"})
		handle.CompleteTransaction()
		shelve['wwnnpoolnumber'] = wwnnpoolnumber		
		wwnnpoolnumber = int(wwnnpoolnumber)

	#Create WWPN Pool for Fabric A
		WWPNPoolName = request.form['wwpnpoolname']
		shelve['WWPNPoolName'] = WWPNPoolName			
		WWPNPoolName = WWPNPoolName + os + TemplateType
		a = wwpnpoolnumbera
		if a > 0:
			b = 1
		else:
			b = 0	
		wwpnpoolnumbera = add(a,b)
		wwpnpoolnumbera = str(wwpnpoolnumbera)
		handle.StartTransaction()
		obj = handle.GetManagedObject(None, None, {"Dn":"org-root/org-',OrgName,"})
		mo = handle.AddManagedObject(obj, "fcpoolInitiators", {"Descr":"", "PolicyOwner":"local", "AssignmentOrder":"default", "Purpose":"port-wwn-assignment",
		"Dn":"org-root/org-" + OrgName + "/wwn-pool-" + WWNPoolName + "A", "Name":WWPNPoolName + "A"})
		mo_1 = handle.AddManagedObject(mo, "fcpoolBlock", {"To":"20:00:00:25:B5:" + SiteID + DomainID + ":A" + wwpnpoolnumbera + ":FF", "From":"20:00:00:25:B5:" + SiteID + DomainID + ":A" + wwpnpoolnumbera + ":00",
		 "Dn":"org-root/org-" + OrgName + "/wwn-pool-" + WWPNPoolName + "A/block-20:00:00:25:B5:" + SiteID + DomainID + ":A" + wwpnpoolnumbera + ":00-20:00:00:25:B5:" + SiteID + DomainID + ":A" + wwpnpoolnumbera + ":FF"})
		handle.CompleteTransaction()
		shelve['wwpnpoolnumbera'] = wwpnpoolnumbera	
		wwpnpoolnumbera = int(wwpnpoolnumbera)

	#Create WWPN Pool for Fabric B
		a = wwpnpoolnumberb
		if a > 0:
			b = 1
		else:
			b = 0	
		wwpnpoolnumberb = add(a,b)
		wwpnpoolnumberb = str(wwpnpoolnumberb)
		handle.StartTransaction()
		obj = handle.GetManagedObject(None, None, {"Dn":"org-root/org-',OrgName,"})
		mo = handle.AddManagedObject(obj, "fcpoolInitiators", {"Descr":"", "PolicyOwner":"local", "AssignmentOrder":"default", "Purpose":"port-wwn-assignment",
		"Dn":"org-root/org-" + OrgName + "/wwn-pool-" + WWPNPoolName + "B", "Name":WWPNPoolName + "B"})
		mo_1 = handle.AddManagedObject(mo, "fcpoolBlock", {"To":"20:00:00:25:B5:" + SiteID + DomainID + ":B" + wwpnpoolnumberb + ":FF", "From":"20:00:00:25:B5:" + SiteID + DomainID + ":B" + wwpnpoolnumberb + ":00",
		 "Dn":"org-root/org-" + OrgName + "/wwn-pool-" + WWPNPoolName + "B/block-20:00:00:25:B5:" + SiteID + DomainID + ":B" + wwpnpoolnumberb + ":00-20:00:00:25:B5:" + SiteID + DomainID + ":B" + wwpnpoolnumberb + ":FF"})
		handle.CompleteTransaction()
		shelve['wwpnpoolnumberb'] = wwpnpoolnumberb	
		wwpnpoolnumberb = int(wwpnpoolnumberb)			

		VSANA = request.form['VSANA']
		FCOEVSANA = request.form['FCOEA']
		VSANB = request.form['VSANB']
		FCOEVSANB = request.form['FCOEB']
		shelve["VSANA"] = VSANA
		shelve["VSANB"] = VSANB
		shelve["FCOEVSANA"] = FCOEVSANA
		shelve["FCOEVSANB"] = FCOEVSANB
		
		
	# Create Fabric A VSAN
		handle.StartTransaction()
		obj = handle.GetManagedObject(None, None, {"Dn":"fabric/san/A"})
		handle.AddManagedObject(obj, "fabricVsan", {"FcZoneSharingMode":"coalesce", "ZoningState":"disabled",
		 "FcoeVlan":FCOEVSANA, "PolicyOwner":"local", "Dn":"fabric/san/A/", "Name":VSANA, "Id":VSANA})

	# Create Fabric B VSAN
		obj = handle.GetManagedObject(None, None, {"Dn":"fabric/san/B"})
		handle.AddManagedObject(obj, "fabricVsan", {"FcZoneSharingMode":"coalesce", "ZoningState":"disabled",
		 "FcoeVlan":FCOEVSANB, "PolicyOwner":"local", "Dn":"fabric/san/B/", "Name":VSANB, "Id":VSANB})
		handle.CompleteTransaction()

	#Create vHBA_Fabric A
		vHBATemplate = os + TemplateType
		handle.StartTransaction()
		obj = handle.GetManagedObject(None, None, {"Dn":"org-root/',OrgName,"})
		mo = handle.AddManagedObject(obj, "vnicSanConnTempl", {"StatsPolicyName":"default",
		 "QosPolicyName":"", "Descr":"", "PolicyOwner":"local", "IdentPoolName": WWPNPoolName + "A",
		 "MaxDataFieldSize":"2048", "TemplType":"initial-template",
		 "Dn":"org-root/org-" + OrgName + "/san-conn-templ-" + vHBATemplate + "HBA_A", "PinToGroupName":"", "Name":vHBATemplate + "HBA_A", "SwitchId":"A"})
		mo_1 = handle.AddManagedObject(mo, "vnicFcIf", {"Name":VSANA, "Dn":"org-root/org-" + OrgName + "/san-conn-templ-" + vHBATemplate + "HBA_A/if-default"}, True)
		handle.CompleteTransaction()

	#Create vHBA_Fabric B
		handle.StartTransaction()
		obj = handle.GetManagedObject(None, None, {"Dn":"org-root/',OrgName,"})
		mo = handle.AddManagedObject(obj, "vnicSanConnTempl", {"StatsPolicyName":"default",
		 "QosPolicyName":"", "Descr":"", "PolicyOwner":"local", "IdentPoolName": WWPNPoolName + "B",
		 "MaxDataFieldSize":"2048", "TemplType":"initial-template",
		 "Dn":"org-root/org-" + OrgName + "/san-conn-templ-" + vHBATemplate + "HBA_B", "PinToGroupName":"", "Name":vHBATemplate + "HBA_B", "SwitchId":"B"})
		mo_1 = handle.AddManagedObject(mo, "vnicFcIf", {"Name":VSANB, "Dn":"org-root/org-" + OrgName + "/san-conn-templ-" + vHBATemplate + "HBA_B/if-default"}, True)
		handle.CompleteTransaction()

	# Create UUID Pool
		UUIDPoolName = request.form['uuidpoolname']
		UUIDPoolName = UUIDPoolName + os + TemplateType
		print UUIDPoolName
		a = UUIDPoolNumber
		if a > 0:
			b = 1
		else:
			b = 0	
		UUIDPoolNumber = add(a,b)
		UUIDPoolNumber = str(UUIDPoolNumber)
		print UUIDPoolNumber
		handle.StartTransaction()
		obj = handle.GetManagedObject(None, None, {"Dn":"org-root/org-' OrgName,"})
		mo = handle.AddManagedObject(obj, "uuidpoolPool", {"Descr":"", "Prefix":"derived", "AssignmentOrder":"default",
		 "Dn":"org-root/org-" + OrgName + "/uuid-pool-" + UUIDPoolName, "PolicyOwner":"local", "Name":UUIDPoolName})
		mo_1 = handle.AddManagedObject(mo, "uuidpoolBlock", {"To":""  + SiteID + DomainID + "0" + UUIDPoolNumber + "-0000000000FF", "From":""  + SiteID + DomainID + "0" + UUIDPoolNumber + "-000000000001",
		 "Dn":"org-root/org-" + OrgName + "/uuid-pool-" + UUIDPoolName + "/block-from-"  + SiteID + DomainID + "0" + UUIDPoolNumber + "-000000000001-to-"  + SiteID + DomainID + "0" + UUIDPoolNumber + "0-0000000000FF"})
		handle.CompleteTransaction()

		shelve['UUIDPoolNumber'] = UUIDPoolNumber
		shelve['UUIDPoolName'] = UUIDPoolName
		UUIDPoolNumber = int(UUIDPoolNumber)	

	# Create Service Profle Template

		TemplateName = os + TemplateType
		handle.StartTransaction()
		obj = handle.GetManagedObject(None, None, {"Dn":"org-root/',OrgName,"})
		mo = handle.AddManagedObject(obj, "lsServer", {"ResolveRemote":"yes", "MgmtFwPolicyName":"", 
		"StatsPolicyName":"default", "HostFwPolicyName":"", "PowerPolicyName":"default", "Name":TemplateName, "IdentPoolName":UUIDPoolName,
		 "BootPolicyName":"SANBoot", "UsrLbl":"", "ExtIPState":"pooled", "Dn":"org-root/org-" + OrgName + "/ls-" + TemplateName,
		 "KvmMgmtPolicyName":"", "BiosProfileName":BiosPolicyName, "DynamicConPolicyName":"",
		 "VmediaPolicyName":"", "MaintPolicyName":maintpolicyname, "AgentPolicyName":"", "MgmtAccessPolicyName":"", "Type":"updating-template",
		 "ExtIPPoolName":cimc_name, "Descr":"", "VconProfileName":"", "SolPolicyName":"", "Uuid":"0", "LocalDiskPolicyName":"default", "PolicyOwner":"local",
		 "SrcTemplName":"", "ScrubPolicyName":""})
		mo_1 = handle.AddManagedObject(mo, "lsVConAssign", {"Dn":"org-root/org-" + OrgName + "/ls-" + TemplateName + "/assign-ethernet-vnic-" + mgmtvnic,
		 "VnicName":mgmtvnic, "Transport":"ethernet", "AdminVcon":"any", "Order":"1"}, True)
		mo_2 = handle.AddManagedObject(mo, "lsVConAssign", {"Dn":"org-root/org-" + OrgName + "/ls-" + TemplateName +"/assign-ethernet-vnic-" + datavnic + "A",
		 "VnicName":datavnic + "A", "Transport":"ethernet", "AdminVcon":"any", "Order":"2"}, True)
		mo_3 = handle.AddManagedObject(mo, "lsVConAssign", {"Dn":"org-root/org-" + OrgName + "/ls-" + TemplateName +"/assign-ethernet-vnic-" + datavnic + "B",
		 "VnicName":datavnic + "B", "Transport":"ethernet", "AdminVcon":"any", "Order":"3"}, True)
		mo_4 = handle.AddManagedObject(mo, "lsVConAssign", {"Dn":"org-root/org-" + OrgName + "/ls-" + TemplateName +"/assign-ethernet-vnic-" + motionvnic,
		"VnicName":motionvnic, "Transport":"ethernet", "AdminVcon":"any", "Order":"4"}, True)
		mo_5 = handle.AddManagedObject(mo, "lsVConAssign", {"Dn":"org-root/org-" + OrgName + "/ls-" + TemplateName +"/assign-fc-vnic-fc0", "VnicName":"fc0",
		 "Transport":"fc", "AdminVcon":"any", "Order":"5"}, True)
		mo_6 = handle.AddManagedObject(mo, "lsVConAssign", {"Dn":"org-root/org-" + OrgName + "/ls-" + TemplateName +"/assign-fc-vnic-fc1", "VnicName":"fc1",
		 "Transport":"fc", "AdminVcon":"any", "Order":"6"}, True)
		mo_7 = handle.AddManagedObject(mo, "vnicEther", {"Order":"1", "Name":mgmtvnic, "IdentPoolName":"", "Mtu":"1500",
		 "AdaptorProfileName":"VMWare", "SwitchId":"A-B", "AdminCdnName":"", "AdminHostPort":"ANY", "Addr":"derived", "QosPolicyName":"",
		 "Dn":"org-root/org-" + OrgName + "/ls-" + TemplateName + "/ether-" + mgmtvnic, "AdminVcon":"any", "StatsPolicyName":"default", "NwCtrlPolicyName":"",
		 "PinToGroupName":"", "NwTemplName":mgmtvnic})
		mo_8 = handle.AddManagedObject(mo, "vnicEther", {"Order":"2", "Name":datavnic + "A", "IdentPoolName":"", "Mtu":"1500",
		 "AdaptorProfileName":"VMWare", "SwitchId":"A", "AdminCdnName":"", "AdminHostPort":"ANY", "Addr":"derived", "QosPolicyName":"",
		 "Dn":"org-root/org-" + OrgName + "/ls-" + TemplateName + "/ether-" + datavnic + "A", "AdminVcon":"any", "StatsPolicyName":"default",
		 "NwCtrlPolicyName":"", "PinToGroupName":"", "NwTemplName":datavnic + "A"})
		mo_9 = handle.AddManagedObject(mo, "vnicEther", {"Order":"3", "Name":datavnic + "B", "IdentPoolName":"", "Mtu":"1500",
		 "AdaptorProfileName":"VMWare", "SwitchId":"B", "AdminCdnName":"", "AdminHostPort":"ANY", "Addr":"derived", "QosPolicyName":"",
		 "Dn":"org-root/org-" + OrgName + "/ls-" + TemplateName + "/ether-" + datavnic + "B", "AdminVcon":"any", "StatsPolicyName":"default", "NwCtrlPolicyName":"",
		 "PinToGroupName":"", "NwTemplName":datavnic + "B"})
		mo_10 = handle.AddManagedObject(mo, "vnicEther", {"Order":"4", "Name":motionvnic, "IdentPoolName":"", "Mtu":"1500",
		 "AdaptorProfileName":"VMWare", "SwitchId":"B-A", "AdminCdnName":"", "AdminHostPort":"ANY", "Addr":"derived",
		 "QosPolicyName":"", "Dn":"org-root/org-" + OrgName + "/ls-" + TemplateName + "/ether-" + motionvnic, "AdminVcon":"any", "StatsPolicyName":"default",
		 "NwCtrlPolicyName":"", "PinToGroupName":"", "NwTemplName":motionvnic})
		mo_11 = handle.AddManagedObject(mo, "vnicFc", {"Order":"5", "Name":"fc0", "AdminVcon":"any", "MaxDataFieldSize":"2048",
		 "IdentPoolName":"", "AdaptorProfileName":"VMWare", "SwitchId":"A", "AdminCdnName":"", "AdminHostPort":"ANY", "Addr":"derived",
		 "QosPolicyName":"", "Dn":"org-root/org-" + OrgName + "/ls-" + TemplateName + "/fc-fc0", "PersBind":"disabled", "StatsPolicyName":"default",
		 "PersBindClear":"no", "PinToGroupName":"", "NwTemplName":vHBATemplate + "HBA_A"})
		mo_11_1 = handle.AddManagedObject(mo_11, "vnicFcIf", {"Name":"", "Dn":"org-root/org-" + OrgName + "/ls-" + TemplateName + "/fc-fc0/if-default"}, True)
		mo_12 = handle.AddManagedObject(mo, "vnicFc", {"Order":"6", "Name":"fc1", "AdminVcon":"any", "MaxDataFieldSize":"2048",
		 "IdentPoolName":"", "AdaptorProfileName":"VMWare", "SwitchId":"A", "AdminCdnName":"", "AdminHostPort":"ANY", "Addr":"derived",
		 "QosPolicyName":"", "Dn":"org-root/org-" + OrgName + "/ls-" + TemplateName + "/fc-fc1", "PersBind":"disabled", "StatsPolicyName":"default",
		 "PersBindClear":"no", "PinToGroupName":"", "NwTemplName":vHBATemplate + "HBA_B"})
		mo_12_1 = handle.AddManagedObject(mo_12, "vnicFcIf", {"Name":"", "Dn":"org-root/org-" + OrgName + "/ls-" + TemplateName + "/fc-fc1/if-default"}, True)
		mo_13 = handle.AddManagedObject(mo, "vnicFcNode", {"IdentPoolName":WWPNPoolName, "Addr":"pool-derived",
		 "Dn":"org-root/org-" + OrgName + "/ls-" + TemplateName + "/fc-node"}, True)
		mo_14 = handle.AddManagedObject(mo, "lsPower", {"State":"admin-up", "Dn":"org-root/org-" + OrgName + "/ls-" + TemplateName + "/power"}, True)
		mo_15 = handle.AddManagedObject(mo, "fabricVCon", {"Transport":"ethernet,fc", "Placement":"physical",
		 "Select":"all", "Fabric":"NONE", "InstType":"auto", "Share":"shared", "Dn":"org-root/org-" + OrgName + "/ls-" + TemplateName + "/vcon-1", "Id":"1"}, True)
		mo_16 = handle.AddManagedObject(mo, "fabricVCon", {"Transport":"ethernet,fc", "Placement":"physical",
		 "Select":"all", "Fabric":"NONE", "InstType":"auto", "Share":"shared", "Dn":"org-root/org-" + OrgName + "/ls-" + TemplateName + "/vcon-2", "Id":"2"}, True)
		mo_17 = handle.AddManagedObject(mo, "fabricVCon", {"Transport":"ethernet,fc", "Placement":"physical",
		 "Select":"all", "Fabric":"NONE", "InstType":"auto", "Share":"shared", "Dn":"org-root/org-" + OrgName + "/ls-" + TemplateName + "/vcon-3", "Id":"3"}, True)
		mo_18 = handle.AddManagedObject(mo, "fabricVCon", {"Transport":"ethernet,fc", "Placement":"physical",
		 "Select":"all", "Fabric":"NONE", "InstType":"auto", "Share":"shared", "Dn":"org-root/org-" + OrgName + "/ls-" + TemplateName + "/vcon-4", "Id":"4"}, True)
		handle.CompleteTransaction()
	
	return render_template('templateconfig.html')

@app.route('/configuremore', methods = ['POST'])
def configuremore():

	ipaddress = shelve['ipaddress']
	username = shelve['username'] 
	password = shelve['password']
	SiteID = shelve['SiteID']
	DomainID = shelve['DomainID']
	OrgName = shelve['OrgName']
	maintpolicyname = shelve['maintpolicyname']
	BiosPolicyName = shelve['BiosPolicyName']
	LocalBootPolicyName = shelve['LocalBootPolicyName']
	SanBootPolicyName = shelve['SanBootPolicyName']
	cimc_name = shelve['cimc_name']
	WWNPoolName	= shelve['WWNPoolName'] 
	WWPNPoolName =	shelve['WWPNPoolName']	
	
	MacPoolName = shelve['MacPoolName']
	macpoolnumberA = shelve['macpoolnumberA']
	macpoolnumberB = shelve['macpoolnumberB']
	wwpnpoolnumbera = shelve['wwpnpoolnumbera']
	wwpnpoolnumberb = shelve['wwpnpoolnumberb']
	wwnnpoolnumber = shelve['wwnnpoolnumber']
	
	mgmtvnic = shelve['mgmtvnic']
	motionvnic = shelve['motionvnic']
	UUIDPoolName = 	shelve['UUIDPoolName'] 
	UUIDPoolNumber = shelve['UUIDPoolNumber'] 
	
	VSANA = shelve["VSANA"]
	VSANB = shelve["VSANB"]
	FCOEVSANA = shelve["FCOEVSANA"]
	FCOEVSANB = shelve["FCOEVSANB"]

	
	#Login to UCS
	handle = UcsHandle()
	handle.Login(ipaddress, username, password, noSsl=True, port=80, dumpXml=YesOrNo.FALSE)


	#Global Configuration Settings

	# Create Mac Address, WWN, WWPN and UUID Pools
	os = request.form['os']
	TemplateType = request.form['TemplateType']
	if os == 'ESX':	

	#Create Mac Addres Pool for VMware Management on Fabric A	

	#Create Mac Addres Pool for Fabric A

		a = int(macpoolnumberA)
		if a > 0:
			b = 1
		else:
			b = 0
		print a
		print macpoolnumberA
		macpoolnumberA = add(a,b)
		print macpoolnumberA
		macpoolnumberA = str(macpoolnumberA)
		MacPoolNameESX = MacPoolName + TemplateType
		

		handle.StartTransaction()
		obj = handle.GetManagedObject(None, None, {"Dn":"org-root/org-',OrgName,"})
		mo = handle.AddManagedObject(obj, "macpoolPool", {"PolicyOwner":"local", "AssignmentOrder":"default",
		 "Dn":"org-root/org-" + OrgName + "/mac-pool-" + MacPoolNameESX + "A", "Name":MacPoolNameESX + "A", "Descr":""})
		mo_1 = handle.AddManagedObject(mo, "macpoolBlock", {"To":"00:25:B5:" + SiteID + DomainID + ":A" + macpoolnumberA +":FF", "From":"00:25:B5:" + SiteID + DomainID + ":A" + macpoolnumberA + ":00",
		 "Dn":"org-root/org-" + OrgName + "/mac-pool-" + MacPoolNameESX + "A/block-00:25:B5:" + SiteID + DomainID + ":A" + macpoolnumberA + ":00-00:25:B5:" + SiteID + DomainID + ":A" + macpoolnumberA + ":FF"})
		handle.CompleteTransaction()
		shelve['macpoolnumberA'] = macpoolnumberA
		macpoolnumberA = int(macpoolnumberA)
		
	#Create Mac Addres Pool for Fabric B

		a = int(macpoolnumberB)
		if a > 0:
			b = 1
		else:
			b = 0
		macpoolnumberB = add(a,b)
		macpoolnumberB = str(macpoolnumberB)

		handle.StartTransaction()
		obj = handle.GetManagedObject(None, None, {"Dn":"org-root/org-',OrgName,"})
		mo = handle.AddManagedObject(obj, "macpoolPool", {"PolicyOwner":"local", "AssignmentOrder":"default",
		 "Dn":"org-root/org-" + OrgName + "/mac-pool-" + MacPoolNameESX + "B", "Name":MacPoolNameESX + "B", "Descr":""})
		mo_1 = handle.AddManagedObject(mo, "macpoolBlock", {"To":"00:25:B5:" + SiteID + DomainID + ":B" + macpoolnumberB + ":FF", "From":"00:25:B5:" + SiteID + DomainID + ":B" + macpoolnumberB + ":00",
		 "Dn":"org-root/org-" + OrgName + "/mac-pool-" + MacPoolNameESX + "B/block-00:25:B5:" + SiteID + DomainID + ":B" + macpoolnumberB + ":00-00:25:B5:" + SiteID + DomainID + ":B" + macpoolnumberB + ":FF"})
		handle.CompleteTransaction()
		shelve['macpoolnumberB'] = macpoolnumberB	
		macpoolnumberB = int(macpoolnumberB)

	#vNIC Template

	# Create vNIC Template for VMware Data Interfaces

		datavnic = os + TemplateType
		handle.StartTransaction()
		obj = handle.GetManagedObject(None, None, {"Dn":"org-root/org-' ,OrgName, "})
		mo = handle.AddManagedObject(obj, "vnicLanConnTempl", {"IdentPoolName":MacPoolNameESX + "A",
		 "Dn":"org-root/org-" + OrgName + "/lan-conn-templ-" + datavnic + "A", "QosPolicyName":"",
		 "Descr":"", "PolicyOwner":"local", "NwCtrlPolicyName":"", "TemplType":"initial-template",
		 "StatsPolicyName":"default", "Mtu":"1500", "PinToGroupName":"", "Name":datavnic + "A", "SwitchId":"A"})
		handle.CompleteTransaction()

		handle.StartTransaction()
		obj = handle.GetManagedObject(None, None, {"Dn":"org-root/org-' ,OrgName, "})
		mo = handle.AddManagedObject(obj, "vnicLanConnTempl", {"IdentPoolName":MacPoolNameESX + "B",
		 "Dn":"org-root/org-" + OrgName + "/lan-conn-templ-" + datavnic + "B", "QosPolicyName":"",
		 "Descr":"", "PolicyOwner":"local", "NwCtrlPolicyName":"", "TemplType":"initial-template",
		 "StatsPolicyName":"default", "Mtu":"1500", "PinToGroupName":"", "Name":datavnic + "B", "SwitchId":"B"})
		handle.CompleteTransaction()

		#Add VLANs for vNIC template 

		vlanrange = request.form['vlandata']
		handle.StartTransaction()
		obj = handle.GetManagedObject(None, None, {"Dn":"org-root/org-', OrgName, "})
		mo = handle.AddManagedObject(obj, "vnicLanConnTempl", {"IdentPoolName":MacPoolNameESX + "A",
		"Dn":"org-root/org-" + OrgName + "/lan-conn-templ-" + datavnic + "A",
		 "QosPolicyName":"", "Descr":"", "PolicyOwner":"local", "NwCtrlPolicyName":"", "TemplType":"initial-template",
		 "StatsPolicyName":"default", "Mtu":"1500", "PinToGroupName":"", "SwitchId":"A"}, True)
		for x in rangeexpand(vlanrange):		
			y = str(x)
			mo_1 = handle.AddManagedObject(mo, "vnicEtherIf", {"DefaultNet":"no", "Name":y,
			 "Dn":"org-root/org-" + OrgName + "/lan-conn-templ-" + datavnic + "A/if-" + y}, True)
		handle.CompleteTransaction()
			
		handle.StartTransaction()	
		obj = handle.GetManagedObject(None, None, {"Dn":"org-root/org-', OrgName, "})
		mo = handle.AddManagedObject(obj, "vnicLanConnTempl", {"IdentPoolName":MacPoolNameESX + "B",
		"Dn":"org-root/org-" + OrgName + "/lan-conn-templ-" + datavnic + "B",
		 "QosPolicyName":"", "Descr":"", "PolicyOwner":"local", "NwCtrlPolicyName":"", "TemplType":"initial-template",
		 "StatsPolicyName":"default", "Mtu":"1500", "PinToGroupName":"", "SwitchId":"B"}, True)
		for x in rangeexpand(vlanrange):		
			y = str(x)
			mo_1 = handle.AddManagedObject(mo, "vnicEtherIf", {"DefaultNet":"no", "Name":y,
			 "Dn":"org-root/org-" + OrgName + "/lan-conn-templ-" + datavnic + "B/if-" + y}, True)
		handle.CompleteTransaction()
		

	#Create WWNN Pool
		WWNPoolName = WWNPoolName + os + TemplateType
		a = int(wwnnpoolnumber)
		b = 1

		wwnnpoolnumber = add(a,b)
		wwnnpoolnumber = str(wwnnpoolnumber)
		handle.StartTransaction()
		obj = handle.GetManagedObject(None, None, {"Dn":"org-root/org-',OrgName,"})
		mo = handle.AddManagedObject(obj, "fcpoolInitiators", {"Descr":"", "PolicyOwner":"local", "AssignmentOrder":"default", 
		"Purpose":"node-wwn-assignment","Dn":"org-root/org-" + OrgName + "/wwn-pool-" + WWNPoolName, "Name":WWNPoolName})
		mo_1 = handle.AddManagedObject(mo, "fcpoolBlock", {"To":"20:00:00:25:B5:" + SiteID + DomainID + ":F" + wwnnpoolnumber + ":FF", "From":"20:00:00:25:B5:" + SiteID + DomainID + ":F" + wwnnpoolnumber + ":00",
		 "Dn":"org-root/org-" + OrgName + "/wwn-pool-" + WWNPoolName + "/block-20:00:00:25:B5:" + SiteID + DomainID + ":FF" + wwnnpoolnumber + ":00-20:00:00:25:B5:" + SiteID + DomainID + ":F" + wwnnpoolnumber + ":FF"})
		handle.CompleteTransaction()
		shelve['wwnnpoolnumber'] = wwnnpoolnumber		
		wwnnpoolnumber = int(wwnnpoolnumber)

	#Create WWPN Pool for Fabric A
		WWPNPoolName = WWPNPoolName + os + TemplateType
		a = int(wwpnpoolnumbera)
		b = 1

		wwpnpoolnumbera = add(a,b)
		wwpnpoolnumbera = str(wwpnpoolnumbera)
		handle.StartTransaction()
		obj = handle.GetManagedObject(None, None, {"Dn":"org-root/org-',OrgName,"})
		mo = handle.AddManagedObject(obj, "fcpoolInitiators", {"Descr":"", "PolicyOwner":"local", "AssignmentOrder":"default", "Purpose":"port-wwn-assignment",
		"Dn":"org-root/org-" + OrgName + "/wwn-pool-" + WWNPoolName + "A", "Name":WWPNPoolName + "A"})
		mo_1 = handle.AddManagedObject(mo, "fcpoolBlock", {"To":"20:00:00:25:B5:" + SiteID + DomainID + ":A" + wwpnpoolnumbera + ":FF", "From":"20:00:00:25:B5:" + SiteID + DomainID + ":A" + wwpnpoolnumbera + ":00",
		 "Dn":"org-root/org-" + OrgName + "/wwn-pool-" + WWPNPoolName + "A/block-20:00:00:25:B5:" + SiteID + DomainID + ":A" + wwpnpoolnumbera + ":00-20:00:00:25:B5:" + SiteID + DomainID + ":A" + wwpnpoolnumbera + ":FF"})
		handle.CompleteTransaction()
		shelve['wwpnpoolnumbera'] = wwpnpoolnumbera	
		wwpnpoolnumbera = int(wwpnpoolnumbera)

	#Create WWPN Pool for Fabric B
		a = int(wwpnpoolnumberb)
		b = 1

		wwpnpoolnumberb = add(a,b)
		wwpnpoolnumberb = str(wwpnpoolnumberb)
		handle.StartTransaction()
		obj = handle.GetManagedObject(None, None, {"Dn":"org-root/org-',OrgName,"})
		mo = handle.AddManagedObject(obj, "fcpoolInitiators", {"Descr":"", "PolicyOwner":"local", "AssignmentOrder":"default", "Purpose":"port-wwn-assignment",
		"Dn":"org-root/org-" + OrgName + "/wwn-pool-" + WWPNPoolName + "B", "Name":WWPNPoolName + "B"})
		mo_1 = handle.AddManagedObject(mo, "fcpoolBlock", {"To":"20:00:00:25:B5:" + SiteID + DomainID + ":B" + wwpnpoolnumberb + ":FF", "From":"20:00:00:25:B5:" + SiteID + DomainID + ":B" + wwpnpoolnumberb + ":00",
		 "Dn":"org-root/org-" + OrgName + "/wwn-pool-" + WWPNPoolName + "B/block-20:00:00:25:B5:" + SiteID + DomainID + ":B" + wwpnpoolnumberb + ":00-20:00:00:25:B5:" + SiteID + DomainID + ":B" + wwpnpoolnumberb + ":FF"})
		handle.CompleteTransaction()
		shelve['wwpnpoolnumberb'] = wwpnpoolnumberb	
		wwpnpoolnumberb = int(wwpnpoolnumberb)			
		
	# Create UUID Pool
		UUIDPoolName = UUIDPoolName + os + TemplateType
		a = int(UUIDPoolNumber)
		b = 1

		UUIDPoolNumber = add(a,b)
		UUIDPoolNumber = str(UUIDPoolNumber)	
		handle.StartTransaction()
		obj = handle.GetManagedObject(None, None, {"Dn":"org-root/org-' OrgName,"})
		mo = handle.AddManagedObject(obj, "uuidpoolPool", {"Descr":"", "Prefix":"derived", "AssignmentOrder":"default",
		 "Dn":"org-root/org-" + OrgName + "/uuid-pool-" + UUIDPoolName, "PolicyOwner":"local", "Name":UUIDPoolName})
		mo_1 = handle.AddManagedObject(mo, "uuidpoolBlock", {"To":""  + SiteID + DomainID + "0" + UUIDPoolNumber + "-0000000000FF", "From":""  + SiteID + DomainID + "0" + UUIDPoolNumber + "-000000000001",
		 "Dn":"org-root/org-" + OrgName + "/uuid-pool-" + UUIDPoolName + "/block-from-"  + SiteID + DomainID + "0" + UUIDPoolNumber + "-000000000001-to-"  + SiteID + DomainID + "0" + UUIDPoolNumber + "0-0000000000FF"})
		handle.CompleteTransaction()

		shelve['UUIDPoolNumber'] = UUIDPoolNumber			
		UUIDPoolNumber = str(UUIDPoolNumber)	
		
	#Create vHBA_Fabric A
		vHBATemplate = os + TemplateType
		handle.StartTransaction()
		obj = handle.GetManagedObject(None, None, {"Dn":"org-root/',OrgName,"})
		mo = handle.AddManagedObject(obj, "vnicSanConnTempl", {"StatsPolicyName":"default",
		 "QosPolicyName":"", "Descr":"", "PolicyOwner":"local", "IdentPoolName": WWPNPoolName + "A",
		 "MaxDataFieldSize":"2048", "TemplType":"initial-template",
		 "Dn":"org-root/org-" + OrgName + "/san-conn-templ-" + vHBATemplate + "HBA_A", "PinToGroupName":"", "Name":vHBATemplate + "HBA_A", "SwitchId":"A"})
		mo_1 = handle.AddManagedObject(mo, "vnicFcIf", {"Name":VSANA, "Dn":"org-root/org-" + OrgName + "/san-conn-templ-" + vHBATemplate + "HBA_A/if-default"}, True)
		handle.CompleteTransaction()

	#Create vHBA_Fabric B
		handle.StartTransaction()
		obj = handle.GetManagedObject(None, None, {"Dn":"org-root/',OrgName,"})
		mo = handle.AddManagedObject(obj, "vnicSanConnTempl", {"StatsPolicyName":"default",
		 "QosPolicyName":"", "Descr":"", "PolicyOwner":"local", "IdentPoolName": WWPNPoolName + "B",
		 "MaxDataFieldSize":"2048", "TemplType":"initial-template",
		 "Dn":"org-root/org-" + OrgName + "/san-conn-templ-" + vHBATemplate + "HBA_B", "PinToGroupName":"", "Name":vHBATemplate + "HBA_B", "SwitchId":"B"})
		mo_1 = handle.AddManagedObject(mo, "vnicFcIf", {"Name":VSANB, "Dn":"org-root/org-" + OrgName + "/san-conn-templ-" + vHBATemplate + "HBA_B/if-default"}, True)
		handle.CompleteTransaction()
		
	# Create Service Profle Template
		os = request.form['os']
		TemplateType = request.form['TemplateType']
		TemplateName = os + TemplateType
		handle.StartTransaction()
		obj = handle.GetManagedObject(None, None, {"Dn":"org-root/',OrgName,"})
		mo = handle.AddManagedObject(obj, "lsServer", {"ResolveRemote":"yes", "MgmtFwPolicyName":"", 
		"StatsPolicyName":"default", "HostFwPolicyName":"", "PowerPolicyName":"default", "Name":TemplateName, "IdentPoolName":UUIDPoolName,
		 "BootPolicyName":"SANBoot", "UsrLbl":"", "ExtIPState":"pooled", "Dn":"org-root/org-" + OrgName + "/ls-" + TemplateName,
		 "KvmMgmtPolicyName":"", "BiosProfileName":BiosPolicyName, "DynamicConPolicyName":"",
		 "VmediaPolicyName":"", "MaintPolicyName":maintpolicyname, "AgentPolicyName":"", "MgmtAccessPolicyName":"", "Type":"updating-template",
		 "ExtIPPoolName":cimc_name, "Descr":"", "VconProfileName":"", "SolPolicyName":"", "Uuid":"0", "LocalDiskPolicyName":"default", "PolicyOwner":"local",
		 "SrcTemplName":"", "ScrubPolicyName":""})
		mo_1 = handle.AddManagedObject(mo, "lsVConAssign", {"Dn":"org-root/org-" + OrgName + "/ls-" + TemplateName + "/assign-ethernet-vnic-" + mgmtvnic,
		 "VnicName":mgmtvnic, "Transport":"ethernet", "AdminVcon":"any", "Order":"1"}, True)
		mo_2 = handle.AddManagedObject(mo, "lsVConAssign", {"Dn":"org-root/org-" + OrgName + "/ls-" + TemplateName +"/assign-ethernet-vnic-" + datavnic + "A",
		 "VnicName":datavnic + "A", "Transport":"ethernet", "AdminVcon":"any", "Order":"2"}, True)
		mo_3 = handle.AddManagedObject(mo, "lsVConAssign", {"Dn":"org-root/org-" + OrgName + "/ls-" + TemplateName +"/assign-ethernet-vnic-" + datavnic + "B",
		 "VnicName":datavnic + "B", "Transport":"ethernet", "AdminVcon":"any", "Order":"3"}, True)
		mo_4 = handle.AddManagedObject(mo, "lsVConAssign", {"Dn":"org-root/org-" + OrgName + "/ls-" + TemplateName +"/assign-ethernet-vnic-" + motionvnic,
		"VnicName":motionvnic, "Transport":"ethernet", "AdminVcon":"any", "Order":"4"}, True)
		mo_5 = handle.AddManagedObject(mo, "lsVConAssign", {"Dn":"org-root/org-" + OrgName + "/ls-" + TemplateName +"/assign-fc-vnic-fc0", "VnicName":"fc0",
		 "Transport":"fc", "AdminVcon":"any", "Order":"5"}, True)
		mo_6 = handle.AddManagedObject(mo, "lsVConAssign", {"Dn":"org-root/org-" + OrgName + "/ls-" + TemplateName +"/assign-fc-vnic-fc1", "VnicName":"fc1",
		 "Transport":"fc", "AdminVcon":"any", "Order":"6"}, True)
		mo_7 = handle.AddManagedObject(mo, "vnicEther", {"Order":"1", "Name":mgmtvnic, "IdentPoolName":"", "Mtu":"1500",
		 "AdaptorProfileName":"VMWare", "SwitchId":"A-B", "AdminCdnName":"", "AdminHostPort":"ANY", "Addr":"derived", "QosPolicyName":"",
		 "Dn":"org-root/org-" + OrgName + "/ls-" + TemplateName + "/ether-" + mgmtvnic, "AdminVcon":"any", "StatsPolicyName":"default", "NwCtrlPolicyName":"",
		 "PinToGroupName":"", "NwTemplName":mgmtvnic})
		mo_8 = handle.AddManagedObject(mo, "vnicEther", {"Order":"2", "Name":datavnic + "A", "IdentPoolName":"", "Mtu":"1500",
		 "AdaptorProfileName":"VMWare", "SwitchId":"A", "AdminCdnName":"", "AdminHostPort":"ANY", "Addr":"derived", "QosPolicyName":"",
		 "Dn":"org-root/org-" + OrgName + "/ls-" + TemplateName + "/ether-" + datavnic + "A", "AdminVcon":"any", "StatsPolicyName":"default",
		 "NwCtrlPolicyName":"", "PinToGroupName":"", "NwTemplName":datavnic + "A"})
		mo_9 = handle.AddManagedObject(mo, "vnicEther", {"Order":"3", "Name":datavnic + "B", "IdentPoolName":"", "Mtu":"1500",
		 "AdaptorProfileName":"VMWare", "SwitchId":"B", "AdminCdnName":"", "AdminHostPort":"ANY", "Addr":"derived", "QosPolicyName":"",
		 "Dn":"org-root/org-" + OrgName + "/ls-" + TemplateName + "/ether-" + datavnic + "B", "AdminVcon":"any", "StatsPolicyName":"default", "NwCtrlPolicyName":"",
		 "PinToGroupName":"", "NwTemplName":datavnic + "B"})
		mo_10 = handle.AddManagedObject(mo, "vnicEther", {"Order":"4", "Name":motionvnic, "IdentPoolName":"", "Mtu":"1500",
		 "AdaptorProfileName":"VMWare", "SwitchId":"B-A", "AdminCdnName":"", "AdminHostPort":"ANY", "Addr":"derived",
		 "QosPolicyName":"", "Dn":"org-root/org-" + OrgName + "/ls-" + TemplateName + "/ether-" + motionvnic, "AdminVcon":"any", "StatsPolicyName":"default",
		 "NwCtrlPolicyName":"", "PinToGroupName":"", "NwTemplName":motionvnic})
		mo_11 = handle.AddManagedObject(mo, "vnicFc", {"Order":"5", "Name":"fc0", "AdminVcon":"any", "MaxDataFieldSize":"2048",
		 "IdentPoolName":"", "AdaptorProfileName":"VMWare", "SwitchId":"A", "AdminCdnName":"", "AdminHostPort":"ANY", "Addr":"derived",
		 "QosPolicyName":"", "Dn":"org-root/org-" + OrgName + "/ls-" + TemplateName + "/fc-fc0", "PersBind":"disabled", "StatsPolicyName":"default",
		 "PersBindClear":"no", "PinToGroupName":"", "NwTemplName":vHBATemplate + "HBA_A"})
		mo_11_1 = handle.AddManagedObject(mo_11, "vnicFcIf", {"Name":"", "Dn":"org-root/org-" + OrgName + "/ls-" + TemplateName + "/fc-fc0/if-default"}, True)
		mo_12 = handle.AddManagedObject(mo, "vnicFc", {"Order":"6", "Name":"fc1", "AdminVcon":"any", "MaxDataFieldSize":"2048",
		 "IdentPoolName":"", "AdaptorProfileName":"VMWare", "SwitchId":"A", "AdminCdnName":"", "AdminHostPort":"ANY", "Addr":"derived",
		 "QosPolicyName":"", "Dn":"org-root/org-" + OrgName + "/ls-" + TemplateName + "/fc-fc1", "PersBind":"disabled", "StatsPolicyName":"default",
		 "PersBindClear":"no", "PinToGroupName":"", "NwTemplName":vHBATemplate + "HBA_B"})
		mo_12_1 = handle.AddManagedObject(mo_12, "vnicFcIf", {"Name":"", "Dn":"org-root/org-" + OrgName + "/ls-" + TemplateName + "/fc-fc1/if-default"}, True)
		mo_13 = handle.AddManagedObject(mo, "vnicFcNode", {"IdentPoolName":WWPNPoolName, "Addr":"pool-derived",
		 "Dn":"org-root/org-" + OrgName + "/ls-" + TemplateName + "/fc-node"}, True)
		mo_14 = handle.AddManagedObject(mo, "lsPower", {"State":"admin-up", "Dn":"org-root/org-" + OrgName + "/ls-" + TemplateName + "/power"}, True)
		mo_15 = handle.AddManagedObject(mo, "fabricVCon", {"Transport":"ethernet,fc", "Placement":"physical",
		 "Select":"all", "Fabric":"NONE", "InstType":"auto", "Share":"shared", "Dn":"org-root/org-" + OrgName + "/ls-" + TemplateName + "/vcon-1", "Id":"1"}, True)
		mo_16 = handle.AddManagedObject(mo, "fabricVCon", {"Transport":"ethernet,fc", "Placement":"physical",
		 "Select":"all", "Fabric":"NONE", "InstType":"auto", "Share":"shared", "Dn":"org-root/org-" + OrgName + "/ls-" + TemplateName + "/vcon-2", "Id":"2"}, True)
		mo_17 = handle.AddManagedObject(mo, "fabricVCon", {"Transport":"ethernet,fc", "Placement":"physical",
		 "Select":"all", "Fabric":"NONE", "InstType":"auto", "Share":"shared", "Dn":"org-root/org-" + OrgName + "/ls-" + TemplateName + "/vcon-3", "Id":"3"}, True)
		mo_18 = handle.AddManagedObject(mo, "fabricVCon", {"Transport":"ethernet,fc", "Placement":"physical",
		 "Select":"all", "Fabric":"NONE", "InstType":"auto", "Share":"shared", "Dn":"org-root/org-" + OrgName + "/ls-" + TemplateName + "/vcon-4", "Id":"4"}, True)
		handle.CompleteTransaction()
	return render_template('templateconfig.html')

	
@app.route("/")
def main():
	return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')





