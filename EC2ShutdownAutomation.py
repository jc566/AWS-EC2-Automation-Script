#amazon web service SDK
import boto3
import sys
import time
import argparse


"""
NOTE!!!
NEVER EVER EVER TERMINATE Instance
Terminate = Permenant Deletion!
"""

#ec2 is to run commands in AWS sdk in relation to ec2
ec2 = boto3.resource('ec2')


#State Instance
instanceState = "running"

#List of Instances to start
InstancesToStart = ['i-e3967655']

#List of Instances to stop
InstancesToStop = ['i-e3967655']

"""
---------------------------------------------------------------
"""
#THIS is a collapsed version of checking instance states.
def CheckInstances(state,instances):
    #This recieves state or 'running' or 'stopped' & instance ID
    print("You requested State : " + str(state) + " & Instance ID : " + str(instances))

    #Check which instances are running
    instances = ec2.instances.filter(
    Filters =[{'Name': 'instance-state-name', 'Values': [state]}])
    

    for instance in instances:
       
       print("Instance ID : " + instance.id, "Instance Type : " + instance.instance_type)

    
    return instances
"""
---------------------------------------------------------------
"""

"""
def CheckRunningInstances():
    print("Currently Running Instances are the Following :\n")
    
    #Check which instances are running
    instances = ec2.instances.filter(
    Filters =[{'Name': 'instance-state-name', 'Values': ['running']}])
    

    for instance in instances:
       
       print("Instance ID : " + instance.id, "Instance Type : " + instance.instance_type)

    
    return instances

def CheckStoppedInstances():
    print("Currently Stopped Instances are the Following :\n")

    #Check which instances are stopped
    
    instances = ec2.instances.filter(
    Filters =[{'Name': 'instance-state-name', 'Values': ['stopped']}])
    
    for instance in instances:
       
       print("Instance ID : " + instance.id, "Instance Type : "
             + instance.instance_type)
    
    return instances
"""

"""
---------------------------------------------------------------
"""
#collapsable version of starting and stopping instances
def StartStopInstances(state,InstanceIds):
    #takes 'running' or 'stopped' and instance ID
    instances = CheckInstances(state,InstanceIds)

    #To start a instance, send in 'stopped' and instance ID
    if(state == 'stopped'):
        for instance in instances:
        #If current instance iterated is in the InstancesToStart tuple, then start current instance
            if(instance.id in InstanceIds):
                #starts the Instances stored inside InstancesToStart tuple
                ec2.instances.filter(InstanceIds=InstanceIds).start()

    #To stop a instance, send 'running' and instance ID
    elif(state == 'running'):
        for instance in instances:
        #If current instance iterated is in the InstancesToStart tuple, then start current instance
            if(instance.id in InstanceIds):

                #starts the Instances stored inside InstancesToStart tuple
                ec2.instances.filter(InstanceIds=InstanceIds).stop()
"""
---------------------------------------------------------------
"""

"""
def StartInstances(InstancesToStart):
    instances = CheckStoppedInstances()

    for instance in instances:
        #If current instance iterated is in the InstancesToStart tuple, then start current instance
        if(instance.id in InstancesToStart):

            #starts the Instances stored inside InstancesToStart tuple
            ec2.instances.filter(InstanceIds=InstancesToStart).start()



def StopInstances(InstancesToStop):
    instances = CheckRunningInstances()

    for instance in instances:
        #If current instance iterated is in the InstancesToStop tuple, then stop current instance
        if(instance.id in InstancesToStop):

            #stops the Instances stored inside InstancesToStop tuple
            ec2.instances.filter(InstanceIds=InstancesToStop).stop()
"""
            
def CheckStatusOfInstances(InstanceID):

    client = boto3.client('ec2') #optionally use 'ec2.meta.client'
    
    StatusString = ''    
    #Check Health Status of Instances
    for status in client.describe_instance_status()['InstanceStatuses']:

        
        

                
        #if InstanceID matches we are looking for        
        if((status["InstanceId"]) in  InstanceID):
            StatusString = status["SystemStatus"]["Details"][0]["Status"]
            break
        else:
            #does Not match
            StatusString = "Stopped or N/A"

    #if it doesnt match, it will return nothing
    return str(StatusString)
    """
    Alternatively I can print just status to see all the other health factors
    """

def RunOtherScript(InstanceID):
    
    
    

    #variable with number of retry attempts
    Num_Of_Retries = 0
    Max_Retries = 50

    #Both methods work below, but not sure of try/except method

   #method with try/except
    
    while (Num_Of_Retries < Max_Retries):
        #this will store the instance state, could potentially be nothing
        StateOF = str(CheckStatusOfInstances(InstanceID))
        print("\nThis is Attempt " +str(Num_Of_Retries + 1))
            
        try:
            print("The Status is currently " + str(StateOF))
            if(StateOF == 'passed'):
                import DummyScript
                print(DummyScript.ReturnAValue(StateOF))
                
                break
            elif(StateOF != 'passed'):
                
                1/0

            
     
            
        except:
            #Increase counter, sleep for X time, allow it to retry connection
            print("\nError. Trying again in 30 seconds.\n")
            Num_Of_Retries += 1
            time.sleep(30)
        if(Num_Of_Retries == Max_Retries):
            sys.exit("Error : Reached Maximum Allowed Attempts\n")
    
    #method with regular while loop
    """
    StateOF = str(CheckStatusOfInstances(InstanceID))
    while (Num_Of_Retries < Max_Retries and StateOF != 'passed'):
        print("\nThis is Attempt " +str(Num_Of_Retries + 1))
        print("The Status is currently " + str(StateOF))
        
        print("\nError. Trying again in 30 seconds.\n")
        Num_Of_Retries += 1
        time.sleep(30)
        StateOF = str(CheckStatusOfInstances(InstanceID))
        if(Num_Of_Retries == Max_Retries):
            sys.exit("Error : Reached Maximum Allowed Attempts\n")

    import DummyScript
    print(DummyScript.ReturnAValue(StateOF))

    """
    
   
 
def main():
    getInfo()
#CheckInstances(instanceState,InstancesToStart)
#StartStopInstances(instanceState,InstancesToStart)


#CheckRunningInstances()
#CheckStatusOfInstances(InstancesToStart)
#RunOtherScript(InstancesToStart)
#StartInstances(InstancesToStart)
#StopInstances(InstancesToStop)


main()


"""
Every collection exposes a filter method that allows you to pass additional
parameters to the underlying API operation.
The EC2 instances collection takes a parameter called Filters,
which is a list of names and values.
"""


