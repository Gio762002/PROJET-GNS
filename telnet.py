import telnetlib
import time

HOST = "2001:127:100:1::1"  
PORT = 23  
user = "admin"  
password = "admin"  

# Establishing Telnet connection
try:
    tn = telnetlib.Telnet(HOST, PORT)

    tn.read_until(b"Username: ")
    tn.write(user.encode('ascii') + b"\n")
    if password:
        tn.read_until(b"Password: ")
        tn.write(password.encode('ascii') + b"\n")

    # Waiting for the command prompt
    time.sleep(1)
    tn.write(b"en\n")
    time.sleep(1)
    output = tn.read_very_eager().decode('ascii')
    print(output)
    tn.write(b"admin\n")
    time.sleep(1)
    output = tn.read_very_eager().decode('ascii')
    print(output)
    # Get config from a file
    with open('config.txt', 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if line == "!":
                tn.write(b"end\n")
                time.sleep(1)
                output = tn.read_very_eager().decode('ascii')
                print(output)
                tn.write(b"conf t\n")
                time.sleep(1)
                output = tn.read_very_eager().decode('ascii')
                print(output)
            else:
                tn.write(line.encode() + b"\n")
                time.sleep(1)  # Waiting for the command to execute
                output = tn.read_very_eager().decode('ascii')
                print(output)

    # Closing the connection
    tn.write(b"exit\n")
    tn.close()

except Exception as e:
    print(f"Failed to connect to the router: {e}")
