from library.device import ClassDevice

CiscoDevice = ClassDevice.read("list_ip","txt","r")

print(CiscoDevice)