import subprocess
import os
import sys
import traceback
from confluent_kafka import KafkaException

def execute_command(command):
    env = os.environ.copy()
    run_command = command.strip()
    run_command_list = run_command.split()
    run_result = subprocess.run(run_command_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env, text=True)
    return run_result

def get_challenge(restserver):
    try:
        classpath_result = execute_command('mapr classpath')

        if classpath_result.returncode != 0:
            print(f"ERROR Failed to get classpath. Response: {out} : {classpath_result.stderr}")
            raise KafkaException("Check whether classpath is set or not")

        classpath = classpath_result.stdout

        result = execute_command( 'java -cp {} com.mapr.security.client.examples.MapRClient challengeresponse -url {}'.format( classpath, restserver ) )
        # Capture the output and error
        if result.returncode != 0:
            print(f"ERROR Failed to get challenge. Response: {out} : {result.stderr}")
            raise KafkaException("Check if all 'restServers' specified are valid")
        out = result.stdout

        # Parse the output to find the challenge string
        challenge_str = None
        strlines = out.splitlines()
        for line in strlines:
            if "Bad server key" in line or "Exception while processing ticket data" in line:
                raise KafkaException("Exception while processing ticket data")
            elif line.startswith("Obtained challenge string"):
                challenge_str = line.split()[3]
                break
            
        return challenge_str if challenge_str else None

    except Exception as e:
        print(traceback.format_exc(), file=sys.stderr)
        print(f"Error: {e}")
        return None
