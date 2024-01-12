import time
from multiprocessing import Process, Pipe

def main(conn):
    simulation_finished = False
    while not simulation_finished:
        '''
        main program of the simulation, using all the fcts defined in the other files: fct_protocol,fct_reseau
        '''
        simulation_finished = True
    conn.send("END")
    conn.close()

def write_file(file_name, content):
    with open(file_name, 'w') as f:
        f.write(content)

if __name__ == '__main__':
    simulator_conn, monitor_conn = Pipe()
    p = Process(target=main, args=(simulator_conn,))
    p.start()
    while True: 
        recv = monitor_conn.recv()
        '''
        all the fcts to generate the Cisco command files for each router
        '''
        
        if recv == "END":
            break
    p.join()




