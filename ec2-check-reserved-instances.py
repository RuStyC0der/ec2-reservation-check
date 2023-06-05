import boto3
from prettytable import PrettyTable

# Region is required
# can be set with export AWS_DEFAULT_REGION=<region>

def get_running_instances(ec2_client):

    '''returns list with running instances'''

    response = ec2_client.describe_instances(Filters=[
        {
            'Name': 'instance-state-name',
            'Values': ['pending', 'running']
        }
    ]
    )

    reservationList = response['Reservations']
	
    instanceList = []

    for reservation in reservationList:
         instanceList.extend(reservation['Instances'])

    return instanceList

    
    

def get_reservations(ec2_client):

    '''returns list with reservations'''

    response = ec2_client.describe_reserved_instances(Filters=[
        {
            'Name': 'state',
            'Values': ['active']
        }
    ])

    reservationList = response['ReservedInstances']
    reservationMap = {}

    for reservation in reservationList:
        reservationMap[reservation['ReservedInstancesId']] = reservation

    return reservationMap

if __name__ == '__main__':
    ec2 = boto3.client('ec2')

    runing_instances = get_running_instances(ec2)
        

    reservations = get_reservations(ec2)


    reserved_instance_rows = []
    unreserved_instance_rows = []

    for instance in runing_instances:
        
        # extract instance name from tag
        instance_name_tag = list(filter(lambda x: x['Key'] == 'Name' ,instance['Tags']))
        if (instance_name_tag):
            instance_name = instance_name_tag[0]['Value']
        else:
            instance_name = "UnknownName"

        instance_id = instance['InstanceId']
        instance_type = instance['InstanceType']



        reservation_id = None

        reservation_end = None
        reservation_type = None

        # search for reservation with applicable instance type
        for reservation_map_key in reservations:
            if reservations[reservation_map_key]['InstanceType'] == instance_type:
                reservation_id = reservation_map_key
                reservation_end = reservations[reservation_map_key]['End']
                reservation_type = reservations[reservation_map_key]['OfferingType']

                # decrease reservation instance count as we match instance
                reservations[reservation_map_key]['InstanceCount'] -= 1



                # remove reservation if no instances are available
                if reservations[reservation_map_key]['InstanceCount'] == 0:
                    reservations.pop(reservation_map_key)
                break
        
        if (reservation_id):
            reserved_instance_rows.append([instance_name, instance_id, instance_type, reservation_type, reservation_end])
        else:
            unreserved_instance_rows.append([instance_name, instance_id, instance_type])

    # pretty display the reservation information
    if reserved_instance_rows:
        reserved_table = PrettyTable(['Name', 'InstanceId', 'InstanceType', 'OfferingType', 'ReservedUntil'])
        reserved_table.align = 'l'
        for reserved_instance_row in reserved_instance_rows:
            reserved_table.add_row(reserved_instance_row)

        print("")
        print("Reserved instances")
        print(reserved_table)
    else:
        print("")
        print("No reserved instances found")

    if unreserved_instance_rows:
        unreserved_table = PrettyTable(['Name', 'InstanceId', 'InstanceType'])
        unreserved_table.align = 'l'
        for unreserved_instance_row in unreserved_instance_rows:
            unreserved_table.add_row(unreserved_instance_row)

        print("")
        print("Not reserved instances")
        print(unreserved_table)
    else:
        print("")
        print("No unreserved instances found")

    if reservations:
        unused_reservation_rows = []
        for reservation_id in reservations:
            unused_reservation_rows.append(reservations[reservation_id]['InstanceType'],
                                           reservations[reservation_id]['InstanceCount'],
                                           reservations[reservation_id]['OfferingType'],
                                           reservations[reservation_id]['End'],
                                           )
        unreserved_table = PrettyTable(['InstanceType', 'UnusedCount', 'OfferingType', 'ValidUntil'])
        unreserved_table.align = 'l'
        for unreserved_instance_row in unreserved_instance_rows:
            unreserved_table.add_row(unreserved_instance_row)
        
        print("")
        print("Not reserved instances")
        print(unreserved_table)

    else:
        print("")
        print("No unused reservations found")