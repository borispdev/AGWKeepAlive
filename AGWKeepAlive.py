import time
import win32serviceutil  # ServiceFramework and commandline helper
import win32service  # Events
import servicemanager  # Simple setup and logging
import sys
import tomllib # Toml library
import requests
import logging
from os import path

def load_config():
    '''
    Load configuration from config.toml file.
    '''
    try:
        path_to_config = path.abspath(path.join(path.dirname(__file__), 'config.toml'))
        with open(path_to_config, 'rb') as f:
            return tomllib.load(f)
    except Exception as e:
        servicemanager.LogErrorMsg("Cannot load 'config.toml' file.")
            
conf = load_config()

# Determine full path to log file
path_to_log = path.abspath(path.join(path.dirname(__file__), conf['service']['log_file']))

# Setup logging 
logging.basicConfig(level=logging.INFO, filename=path_to_log, format='%(asctime)s, - %(levelname)s - %(message)s')

class AGWKeepAlive:

    def call_agw_api(self, agw_ip):
        '''
        Make request to AGW portal XML endpoint and return response or error.
        '''
        if agw_ip is None:
            logging.error('Invalid AGW IP address, please check config.toml file "ip_list" setting.')
            return {'status' : 'invalid', 'agw' : agw_ip}
        try:
            response = requests.get(f'http://{agw_ip}/portal.xml', timeout=conf['service']['request_timeout'])
            return {'status':response.status_code, 'agw' : agw_ip}
        except requests.exceptions.Timeout:
            logging.error(f"Request timeout. Please ensure {agw_ip} is assigned to AGW, powered on and connected to network.")
            return {'status' : 'timeout', 'agw' : agw_ip}
    
    def check_response(self, response_code, agw_ip):
        '''
        Log message depending on HTTP response code.
        '''
        if response_code == 200:
            if conf['service']['log_success'] == True:
                logging.info(f'IP: {agw_ip} - connection success.')
        elif response_code >= 400 and response_code < 500:
            logging.error(f'IP: {agw_ip} - Request rejected by AGW.')
        elif response_code >= 500:
            logging.error(f'IP: {agw_ip} - AGW software error, infusion data possibly unaccessible.')
            
    def request_loop(self):
        '''
        Loop through list of AGW IPs, call HTTP request and check response.
        '''
        for device in conf['AGW']['ip_list']:
            response = self.call_agw_api(device)
            if response['status'] == 'timeout':
                continue
            elif response['status'] == 'invalid':
                continue
            self.check_response(response['status_code'], response['agw'])
        
    def stop(self):
        '''
        Service stop trigger function.
        '''
        logging.info("Service stopped.")
        self.running = False

    def run(self):
        '''
        Start main service loop.
        '''
        logging.info("Service started.")
        self.running = True
        while self.running:
            self.request_loop()
            time.sleep(conf['service']['interval'])


class AGWKeepAliveService(win32serviceutil.ServiceFramework):

    _svc_name_ = 'AGWKeepAlive.' 
    _svc_display_name_ = 'AGW Keep Alive.'
    _svc_description_ = 'AGW Keep alive and connectivity test service.'

    def SvcStop(self):
        '''
        Service stop function.
        '''
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        self.service_impl.stop()
        self.ReportServiceStatus(win32service.SERVICE_STOPPED)

    def SvcDoRun(self):
        '''
        Initialize and start service.
        '''
        self.ReportServiceStatus(win32service.SERVICE_START_PENDING)
        self.service_impl = AGWKeepAlive()
        self.ReportServiceStatus(win32service.SERVICE_RUNNING)
        # Run the service
        self.service_impl.run()


def init():
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(AGWKeepAliveService)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(AGWKeepAliveService)


if __name__ == '__main__':
    init()