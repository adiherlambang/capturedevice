from datetime import datetime
from netmiko import ConnectHandler,NetmikoTimeoutException, NetmikoAuthenticationException, ConnectionException
import os.path

class ClassDevice:

    def __init__(self):
        pass

    def read(self,namaFIle,typeFile,typeAction):
        """Function untuk membaca list IP device dari file"""
        with open("./ListFile/"+namaFIle+"."+typeFile, typeAction) as listFile:
            return listFile.read().split("\n")

    def connect_device(self,ip,cmd,usr,pas,sec):
        ##Perintah untuk mendifinisikan tanggal untuk nama file
        try:
            date_now   = datetime.now()
            time_stamp = date_now.strftime("%d-%m-%y_%H_%M")
            ### Proses Connect ke Device
            device = {
                'device_type': 'cisco_ios'
            }

            device['host'] = ip
            device['username'] = usr
            device['password'] = pas
            device['secret'] = sec

            #Function dari modul netmiko
            connect_device = ConnectHandler(**device)
            connect_device.enable()

            print("connecting to device: "+ip)

            #Mencari Hostname
            req_hostname = connect_device.send_command('show running-config | in hostname')

            if req_hostname :
                split_hostname = req_hostname.split()
            else:
                split_hostname = "NotFound"

            ### Define file name dari hostname dan tanggal
            self.file_path = "CaptureLog/"
            hostname_date = split_hostname[1] + '-' + time_stamp + '.log'
            self.file_name = os.path.join(self.file_path, hostname_date)
            ### Proses Capture untuk setiap command yang ada di list file
            for command in cmd:
                #print(command) Optional untuk checking
                output_command = connect_device.send_command(f"{command}")
                with open(self.file_name, 'a') as file:
                    file.write(f'''\n{command}\n{output_command}\n\n''')
            result = "Success capture log : " + ip
        except NetmikoTimeoutException as err:
            result = "capture log Failed"+ str(err) +" : " + ip
            with open(os.path.join(self.file_path, ip+'-'+time_stamp+'.log'), 'a') as file:
                    file.write(f"Error while capturing log, cause {err}")
        except NetmikoAuthenticationException as err:
            result = "capture log Failed "+ str(err) +" : " + ip
            with open(os.path.join(self.file_path, ip+'-'+time_stamp+'.log'), 'a') as file:
                    file.write(f"Error while capturing log, cause {err}")
        except ConnectionException as err:
            result = "capture log Failed "+ str(err) +" : " + ip
            with open(os.path.join(self.file_path, ip+'-'+time_stamp+'.log'), 'a') as file:
                    file.write(f"Error while capturing log, cause {err}")
        finally:
            return result

        