import subprocess
import os


class Exogenous_Spawner:
    def __init__(self):
        self.subprocesses = dict()
    
    def start_investor_and_jumps(self, group_id, investor_name, investor_url, investor_data, jumps_name, jumps_url, jumps_data):
        investor = self.spawn(group_id, investor_name, investor_url,investor_data)
        jumps = self.spawn(group_id, jumps_name, jumps_url, jumps_data)

        self.subprocesses[group_id] = {'investor': investor, 'jumps': jumps}}


    def spawn(self, id, name, url, data):
        cmd = ['python', name, str(id), url, data]
        p = subprocess.Popen(cmd)
        return p
        
    def kill(self, group_id):
        for p in self.subprocesses[group_id]:
            p.kill()