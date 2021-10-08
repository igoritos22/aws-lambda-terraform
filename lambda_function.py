import datetime, boto3, os, json
from botocore.exceptions import ClientError

ec2 = boto3.resource('ec2')
client = boto3.client('ec2')

def lambda_handler(event, context):
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
                        snsClient.get_topic_attributes( TopicArn= "arn:aws:sns:sa-east-1:354355251500:SecOpsTopic" )
                        snsClient.publish(TopicArn = "arn:aws:sns:sa-east-1:354355251500:SecOpsTopic", Message = json.dumps(remediateSgs, indent=4) )

                    except ClientError as e:
                        remediateSgs = {'SGRemediadosViaLambda':[]}
                    
                    return response["SecurityGroups"][i]["GroupName"]