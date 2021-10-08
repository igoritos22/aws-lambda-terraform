import datetime, boto3, os, json
from botocore.exceptions import ClientError

ec2 = boto3.resource('ec2')
client = boto3.client('ec2')

globalVars  = {}
globalVars['SecOpsTopicArn']        = ""

def lambda_handler(event, context):
    globalVars['SecOpsTopicArn']=str(os.getenv('SecOpsTopicArn'))
    response = client.describe_security_groups()
    #print(response)
    snsClient = boto3.client('sns')
    vulnerabele_sgs = []
    remediateSgs = {'SGRemediadosViaLambda':[]}
    
    for i in range(len(response["SecurityGroups"])):
        for j in range(len(response["SecurityGroups"][i]["IpPermissions"])):
            for k in range(len(response["SecurityGroups"][i]["IpPermissions"][j]["IpRanges"])):
                if (
                    response["SecurityGroups"][i]["IpPermissions"][j].get('IpProtocol') == '-1' and
                    response["SecurityGroups"][i]["IpPermissions"][j]["IpRanges"][k]["CidrIp"] == '0.0.0.0/0'):
                    response["SecurityGroups"][i]["GroupId"]
                    #print(response["SecurityGroups"][i]["GroupName"])
                    security_group = ec2.SecurityGroup(response["SecurityGroups"][i]["GroupId"])
                    
                    #remove as regras dos grupos que passaram pelo grande filtro
                    rm_ingress_rule = security_group.revoke_ingress(
                        GroupId=response["SecurityGroups"][i]["GroupId"],
                        IpPermissions=[ {'IpProtocol': '-1','IpRanges':[{'CidrIp': '0.0.0.0/0'}]}])
                    
                    vulnerabele_sgs.append(response["SecurityGroups"][i]["GroupName"])
                    remediateSgs['SGRemediadosViaLambda'].append(response["SecurityGroups"][i]["GroupName"])
                    
                    try:
                        snsClient.get_topic_attributes( TopicArn= globalVars['SecOpsTopicArn'] )
                        snsClient.publish(TopicArn = globalVars['SecOpsTopicArn'], Message = json.dumps(remediateSgs, indent=4) )

                    except ClientError as e:
                        remediateSgs = {'SGRemediadosViaLambda':[]}
                    
                    return response["SecurityGroups"][i]["GroupName"]