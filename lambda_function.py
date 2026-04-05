import boto3
import json

ec2 = boto3.client('ec2')

# Replace with your isolation security group ID
ISOLATION_SG_ID = 'sg-xxxxxxxxxxxxxxxxx'

def lambda_handler(event, context):
    try:
        # Get instance ID from event
        instance_id = event['detail']['instance-id']
        print(f"[INFO] Starting forensic process for {instance_id}")

        # Step 1: Get instance details
        response = ec2.describe_instances(InstanceIds=[instance_id])
        
        instance = response['Reservations'][0]['Instances'][0]
        volume_id = instance['BlockDeviceMappings'][0]['Ebs']['VolumeId']

        print(f"[INFO] Volume ID: {volume_id}")

        # Step 2: Create snapshot
        snapshot = ec2.create_snapshot(
            VolumeId=volume_id,
            Description=f"Forensic snapshot for {instance_id}"
        )

        snapshot_id = snapshot['SnapshotId']
        print(f"[INFO] Snapshot created: {snapshot_id}")

        # Step 3: Tag snapshot
        ec2.create_tags(
            Resources=[snapshot_id],
            Tags=[
                {'Key': 'Name', 'Value': 'ForensicSnapshot'},
                {'Key': 'InstanceId', 'Value': instance_id}
            ]
        )

        # Step 4: Isolate instance (replace SG)
        ec2.modify_instance_attribute(
            InstanceId=instance_id,
            Groups=[ISOLATION_SG_ID]
        )

        print(f"[INFO] Instance {instance_id} isolated successfully")

        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Forensic process completed',
                'instance_id': instance_id,
                'snapshot_id': snapshot_id
            })
        }

    except Exception as e:
        print(f"[ERROR] {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps('Error in forensic process')
        }
