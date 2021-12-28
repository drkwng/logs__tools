import sys
import socket
import ipaddress

from get_bot_subnets import googlebot_ips


class BotValidate:
    def __init__(self, _ips):
        self.googlebot_ips = googlebot_ips()
        self.ips = _ips

    @staticmethod
    def soft_validate(_ip, subnet_list):
        """ Validate by IP list """
        try:
            for subnet in subnet_list:
                if ipaddress.ip_address(_ip) in ipaddress.ip_network(subnet):
                    return True, 'Google'
            return False, 'N/A'

        except ValueError:
            print(f'Value error. {_ip} does not appear to be an IPv4 or IPv6 address')
            return False

    @staticmethod
    def rdns(_ip):
        """ Reverse DNS check """
        try:
            name = socket.gethostbyaddr(_ip)[0]
            rdns_ip = socket.gethostbyname(name)
            if rdns_ip == _ip:
                return True, name
            else:
                return False, 'N/A'

        except Exception as e:
            print(e)
            return 'N/A', 'N/A'

    def main(self):
        res = {}
        for ip in self.ips:
            soft_valid = self.soft_validate(ip, self.googlebot_ips)
            if soft_valid[0]:
                res[ip] = soft_valid
            else:
                rdns = self.rdns(ip)
                res[ip] = rdns

        return res


if __name__ == '__main__':
    try:
        ips = sys.argv[1:]
        bot_valid = BotValidate(ips)
        result = bot_valid.main()

        with open('data/results/bot_validate.csv', 'w', encoding='utf-8') as f:
            f.write("IP;VALID;NAME\n")
            for key, value in result.items():
                print(key, value)
                f.write(f"{key};{value[0]};{value[1]}\n")

    except Exception as e:
        print(e, type(e))
