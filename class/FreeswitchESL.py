from freeswitchESL import ESL

class FreeswitchESL():
    def __init__(self, caller:str="", receiver:str="") -> None:
        self.caller = caller
        self.receiver = receiver
        
        self.con = ESL.ESLconnection(
            "51.91.97.8", "8021", "ClueCon"
        )  # Replace with your FreeSWITCH server details
        self.__data = []
        
    def originate_and_bridge_calls(self):
        try:
            gateway = "kolmisoft"
            prefix = ""

            call1 = (
                " {ignore_early_media=true,origination_caller_id_number=%s}sofia/gateway/%s/%s%s"
                % (self.receiver, gateway, prefix, self.caller)
            )
            call2 = "&bridge(sofia/gateway/%s/%s%s)" % (gateway, prefix, self.receiver)

            originate_cmd = "%s %s" % (call1, call2)

            result = self.con.bgapi("originate", originate_cmd)
            if result:
                print(result.getBody())
                
            e = self.con.recvEvent()
            raw_data = e.serialize().split('\n')
            cdr = {}
            for item in raw_data:
                if ': ' in item:
                    header, value = item.split(': ', 1)
                    header = header.replace('variable_', '')
                    cdr[header] = value

            self.__data = cdr
            # cdr contains a complete list of channel variables
            # print('---------\n')
            # print('---------\n')
            # print('---------\n')
            # print('New CDR:', end=' ')
            # print(f"[{cdr}]")
            # print(cdr.get('uuid'), cdr.get('direction'), cdr.get('answer_epoch'), cdr.get('end_epoch'), cdr.get('hangup_cause'))
        except Exception as e:
            print("Error originate:", e)
            return False
        finally:
            return self.__data