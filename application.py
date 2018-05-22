from flask import Flask, request, render_template
from netaddr import IPNetwork
import random
import sqlite3

# Dependencies that need to be 'pip install'ed:
# -> netaddr
# -> flask
#
# Reference for Flask: http://flask.pocoo.org/docs/0.12/quickstart/
#
# How to run:
#
# $ FLASK_APP=application.py flask run --host=0.0.0.0
#
# Note: Omit the "--host=0.0.0.0" when running in debug mode to prevent external hosts from accessing the site
#
#
# How to send test request:
#  curl -i -X POST -H 'Content-Type: application/{"key":"posted value"}' http://127.0.0.1:5000
#
# Taken from https://stackoverflow.com/questions/4797534/how-do-i-manually-fire-http-post-requests-with-firefox-or-chrome

app = Flask(__name__)
application = app # Needed by Elastic Beanstalk

HACKTAVIST_IP_FILE = 'hacktavist_ip_blocks.txt'
APT_IP_FILE = 'apt_ip_blocks.txt'
INFRASTRUCTURE_IP_FILE = 'infrastructure_ip_blocks.txt'

HACKTAVIST_IP_TYPE = 'hacktavist'
APT_IP_TYPE = 'apt'
INFRASTRUCTURE_IP_TYPE = 'infrastructure'

MAX_IP_GUESSES = 100

DB_NAME = 'used_ips.db'
CREATE_TABLE_COMMAND = """
    CREATE TABLE IF NOT EXISTS used_ips(
        ip TEXT PRIMARY KEY
    );
"""

def execute_command(command):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.executescript(command)
    conn.commit()
    conn.close()

def execute_query(query):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute(query)
    results = c.fetchall()
    conn.commit()
    conn.close()

    return results

def create_db_tables_if_not_exists():
    execute_command(CREATE_TABLE_COMMAND)

# TODO: remove
def get_list_of_ips_from_cidr_blocks(list_of_cidrs):
    list_of_ip_lists = [ list(IPNetwork(ip_block)) for ip_block in list_of_cidrs ]
    return [ item for sublist in list_of_ip_lists for item in sublist ]

def load_ips(type):
    ip_list = []
    file_name = None
    
    if type == HACKTAVIST_IP_TYPE:
        file_name = HACKTAVIST_IP_FILE
    elif type == APT_IP_TYPE:
        file_name = APT_IP_FILE
    elif type == INFRASTRUCTURE_IP_TYPE:
        file_name = INFRASTRUCTURE_IP_FILE
    else:
        return None # TODO: Turn into a HTTP error code ultimately
        
    with open(file_name) as f:
        for line in f:
            ip_list.append(line)

    return ip_list

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ip', methods=['GET'])
def get_ip():
    create_db_tables_if_not_exists()

    # TODO: Remove
    # Uncomment this to prove that the used IP's are being stored to the database
    # print("Current DB contents:")
    # result = execute_query("SELECT * FROM used_ips;")
    # for row in result:
    #     print(row)
    # print("")
    
    used_ips_by_type = {}
    used_ips_by_type[HACKTAVIST_IP_TYPE] = []
    used_ips_by_type[APT_IP_TYPE] = []
    used_ips_by_type[INFRASTRUCTURE_IP_TYPE] = []

    requested_ip_type = request.args.get('type', None)

    # TODO: Return HTTP error codes for these error cases
    if requested_ip_type == None:
        return ''

    if not requested_ip_type in [HACKTAVIST_IP_TYPE, APT_IP_TYPE, INFRASTRUCTURE_IP_TYPE]:
        return ''

    cidr_block_list = load_ips(requested_ip_type)

    ip = None
    num_guesses = 0
    while num_guesses < MAX_IP_GUESSES: 
        cidr_block = random.choice(cidr_block_list)
        ip_list = list(IPNetwork(cidr_block))
        ip = str(random.choice(ip_list))
        result = execute_query("SELECT * FROM used_ips WHERE ip = '%s';" % ip)

        # This means that we not used this IP address already
        if len(result) == 0:
            break

    execute_command("INSERT INTO used_ips (ip) VALUES ('%s');" % ip)
    return ip
    
