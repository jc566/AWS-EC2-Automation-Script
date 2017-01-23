import boto3
import argparse
import time
import sys
#Validate Credentials
session = boto3.session.Session(aws_access_key_id='YOUR ACCESS KEY ID',
                  aws_secret_access_key='YOUR SECRET KEY',
                  region_name='PICK A REGION')
                  
#ec2 is to run commands in AWS sdk in relation to ec2
ec2 = session.resource('ec2')

#To run in command line using argparse
parser = argparse.ArgumentParser()
parser.add_argument('--action',choices=('start','stop'),required=True)
parser.add_argument('--instanceid',nargs ='*',required=True)
args = parser.parse_args()

#Prints the status of All instances
def CheckAllInstances():
    ec2_status = []
    
    instances = ec2.instances.filter(
    Filters=[{'Name': 'instance-state-name', 'Values': ['stopped','running']}])
    for instance in instances:
        ec2_status.append({'instanceid': instance.id, 
                           'instancetype': instance.instance_type,
                           'instancestatus': instance.state['Name']})
    return ec2_status
    
    
def CheckStatus(instances):
    client = ec2.meta.client #boto3.client('ec2') 

    for status in client.describe_instance_status()['InstanceStatuses']:
       #if InstanceID matches we are looking for        
        if((status["InstanceId"]) in  instances):
            StatusString = status["SystemStatus"]["Details"][0]["Status"]
            break
        else:
        #does Not match
            StatusString = "Stopped or N/A"
    return(StatusString)
  
  
def EstablishConnection(instances):
    Num_of_retries = 0
    Max_Retries = 5
    
    while (Num_of_retries < Max_Retries):
        STATE = CheckStatus(instances)
        print(STATE)
        print("\nThis is Attempt " +str(Num_of_retries + 1))
        
        if(STATE == 'passed'):
            print("Connection is Established. Currently running state")
            totalTime = (120 * (Num_of_retries + 1))/60
            print("It took approximately %s minutes." %totalTime)
            break
        else:
            print("\nError. Trying again in 2 minutes.\n")
            Num_of_retries += 1
            time.sleep(120)
        if(Num_of_retries == Max_Retries):
            sys.exit("Error : Reached Maximum Allowed Attempts\n")
    return
            
#Based on arg.action it either starts or stops instances in arg.instanceid
def StartStopInstances(instanceid, action):

    instances = CheckAllInstances() #checks status of all ec2 instances and returns list
    
    arg_ec2_status = []    
    
    for instance in instances:
        for row in instanceid:
            if(instance['instanceid'] == row):
                arg_ec2_status.append(instance)
    
    try:
        for i in arg_ec2_status:
            #To start a instance, send in 'stopped' and instance ID
            if (action == 'start' and i['instancestatus'] == 'stopped'):
                ec2.instances.filter(InstanceIds=[i['instanceid']]).start()
                
            #To stop a instance, send 'running' and instance ID
            elif (action == 'stop' and i['instancestatus'] == 'running'):
                ec2.instances.filter(InstanceIds=[i['instanceid']]).stop()
    except: 
        
        print("Error")
    
def main():
    
    StartStopInstances(args.instanceid, args.action)
    EstablishConnection(args.instanceid)
    
if __name__ == "__main__": # This tells the script to run if it is the main executable - directly executable from command line
  main()
