class Solution:
    def validIPAddress(self, queryIP: str) -> str:
        # Helper for IPv4 check
        def isIPv4(ip):
            parts = ip.split(".")
            if len(parts) != 4:
                return False
            for part in parts:
                if not part:
                    return False
                if not part.isdigit():
                    return False
                if part[0] == '0' and len(part) != 1:
                    return False
                if not 0 <= int(part) <= 255:
                    return False
            return True

        # Helper for IPv6 check
        def isIPv6(ip):
            parts = ip.split(":")
            if len(parts) != 8:
                return False
            hex_digits = "0123456789abcdefABCDEF"
            for part in parts:
                if not (1 <= len(part) <= 4):
                    return False
                if not all(c in hex_digits for c in part):
                    return False
            return True

        # Apply checks
        if isIPv4(queryIP):
            return "IPv4"
        elif isIPv6(queryIP):
            return "IPv6"
        else:
            return "Neither"




if __name__ == "__main__":
    queryIP = "172.16.254.1"
    print(Solution().validIPAddress(queryIP))