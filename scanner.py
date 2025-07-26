import sys
import socket
from datetime import datetime
import threading

#Function to scan a port

def scan_port(target,port):
    try:
        # Sockets - can be used to connect two nodes
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        result = s.connect_ex((target,port)) #error indicator - if 0, port is open else not
        if result == 0: #if port is open, lets user know, then shuts that port
            print(f"Port {port} is open")
        s.close() #close to try next port
    except socket.error as e:
        print(f"Socket error on port {port}: {e}") #Socket error: could be anything - DNS issue, connection refused, timed out
    except Exception as e:
        print(f"Unexpected error on port {port}: {e}")

#Main Function - argument validation and target definition
def main():
    if len(sys.argv) == 2: #if argument (comment below ex.) is length 2 (pyth.. scan.. 192.128...) 
        target = sys.argv[1] #then pull target (IP address) example below
    else:
        print("Invalid number of arguments.")
        print("Usage: python.exe scanner.py <target>")
        sys.exit(1) #should be sys.exit(1)
    #python.exe scanner.py 192.128.1.1 (example executable)

    # Resolve the target hostname to an IP address 
    try:
        target_ip = socket.gethostbyname(target) #if hostname provided instead of IP, converts it to IP
    except socket.gaierror:
        print(f"Error: Unable to resolve hostname {target}")
        sys.exit(1)
    
    # Add a pretty banner
    print("-" * 50)
    print(f"Scanning target {target_ip}")
    print(f"Time started: {datetime.now()}")
    print("-" * 50)

    try:
        # Use multithreading to scan ports concurrently (same time instead of one by one)
        threads = []
        for port in range(1, 65536):
            #thread - seperate flow of execution that runs concurrently with other programs
            thread = threading.Thread(target=scan_port, args=(target_ip, port)) #want to use function scan_port with those arguments
            threads.append(thread) #after running it gets rid of that thread in the threads list
            thread.start() #actually executes thread

        # Wait for all threads to complete
        for thread in threads:
            thread.join()

    except KeyboardInterrupt: #ctrl c
        print("\nExiting program.")
        sys.exit(0)

    except socket.error as e: #when socket error occurs = an issue establishing, maintaining, or closing nodes connection
        print(f"Socket error: {e}")
        sys.exit(1)

    #if everything runs through and scan is finished - print
    print("\nScan completed!")

#Can only be executed here on its own (cant be imported) name is main
if __name__ == "__main__":
    main()

    #run file [IP address] - in terminal
