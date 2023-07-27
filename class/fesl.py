from freeswitchESL import ESL


def originate_and_bridge_calls(number1, number2):
    gateway = "kolmisoft"
    prefix = ""

    con = ESL.ESLconnection(
        "51.91.97.8", "8021", "ClueCon"
    )  # Replace with your FreeSWITCH server details

    call1 = (
        " {ignore_early_media=true,origination_caller_id_number=%s}sofia/gateway/%s/%s%s"
        % (number2, gateway, prefix, number1)
    )
    call2 = "&bridge(sofia/gateway/%s/%s%s)" % (gateway, prefix, number2)

    originate_cmd = "%s %s" % (call1, call2)

    result = con.bgapi("originate", originate_cmd)
    if result:
        print(result.getBody())

    # Hang up the ESL connection
    con.disconnect()


# Example usage
#originate_and_bridge_calls("2250153148864", "2250700003331")
