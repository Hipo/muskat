import boto.ec2 as ec2

def get_regions():
    ec2_regions = ec2.regions()
    regions = []
    for region in ec2_regions:
        regions.append(region.name)
    return regions
    

def connect_to_generic():
    try:
        connection = ec2.connection.EC2Connection()
    except:
        raise Exception("Connection", "Unable to connect")

    return connection


def connect_to_region(region_name):
    try:
        connection = ec2.connect_to_region(region_name)
    except:
        raise Exception("Connection", "Unable to connect to " + region_name)

    return connection
