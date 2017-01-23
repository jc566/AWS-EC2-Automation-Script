import boto3
import argparse
"""
Send parameters in command line
Either Start or Stop
Followed by Instance ID(s)
"""
#Validate Credentials
session = boto3.session.Session(aws_access_key_id='YOUR ACCESS KEY ID',
                  aws_secret_access_key='YOUR SECRET ACCESS KEY',
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

#Based on arg.action it either starts or stops instances in arg.instanceid
def StartStopInstances(instanceid, action):

    instances = CheckAllInstances() #checks status of all ec2 instances and returns list
    
    arg_ec2_status = []    
    
    for instance in instances:
        for row in instanceid:
            if(instance['instanceid'] == row):
                arg_ec2_status.append(instance)

    for i in arg_ec2_status:
        #To start a instance, send in 'stopped' and instance ID
        if (action == 'start' and i['instancestatus'] == 'stopped'):
            ec2.instances.filter(InstanceIds=[i['instanceid']]).start()
            
        #To stop a instance, send 'running' and instance ID
        elif (action == 'stop' and i['instancestatus'] == 'running'):
            ec2.instances.filter(InstanceIds=[i['instanceid']]).stop()
    
    
def main():

    StartStopInstances(args.instanceid, args.action)
    
if __name__ == "__main__": # This tells the script to run if it is the main executable - directly executable from command line
  main()
