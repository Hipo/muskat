from docopt import docopt


from ec2 import EC2
import connect

resources = ['EBS','EIP']
regions = connect.get_regions()

def show(resources, verbose=False, region='us-east-1'):
    ec2 = EC2(region)
    if resources == 'EBS':
        unused_volumes = ec2.get_unattached_ebs()
        print len(unused_volumes), "Unused Volumes on", region
        if verbose and unused_volumes:
            print unused_volumes
    if resources == 'EIP':
        addresses = ec2.get_dissassociated_eip()
        print len(addresses), "Disassociated IP's on", region
        if verbose and addresses:
            print addresses
            
def clean(resources, verbose=False, region='us-east-1'):
    ec2 = EC2(region)
    if resources == 'EBS':
        unused_volumes = ec2.get_unattached_ebs()
        ec2.delete_ebs(unused_volumes)
        if verbose:
            print "Deleted %s EBS volumes: %s on %s" % (len(unused_volumes), unused_volumes, region) 
    if resources == 'EIP':
        addresses = ec2.get_dissassociated_eip()
        ec2.delete_eip(addresses)
        if verbose:
            print "Deleted %s Elastic IP's: %s on %s" % (len(addresses), addresses, region)
            
__doc__  = """Muskat

Usage:
    muskat.py show <resource> [<region> --verbose]
    muskat.py clean <resource> [<region> --verbose]
    muskat.py (-h | --help)


Options:
    <resource>   all, %s
    <region>     all, %s

-h --help    Show this screen
    --verbose    Verbose Output


"""%(", ".join(resources), ", ".join(regions)) 

if __name__ == '__main__':
    arg = docopt(__doc__, version='Muskat 0.1')
    if arg['show']:
        do = locals()['show']
    if arg['clean']:
        do = locals()['clean']
        
    if arg['<resource>'] == 'all':
        if arg['<region>'] == 'all':
            for resource in resources:
                for region in regions:
                    do(resource, arg['--verbose'], region)
        else:
            for resource in resources:
                do(resource, arg['--verbose'], arg['<region>'])
    else:
        for region in regions:
            do(arg['<resource>'], arg['--verbose'], region)

