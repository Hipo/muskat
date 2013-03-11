import connect

class EC2:
    def __init__(self,region_name):
        self.connection = connect.connect_to_region(region_name)
        
    def get_unattached_ebs(self):
        volumes = self.connection.get_all_volumes()
        unattached_volumes = []

        for volume in volumes:
            if volume.attachment_state() == None and volume.status != "deleting": 
                unattached_volumes.append(volume.id)
        return unattached_volumes
    
    def delete_ebs(self,volumes):
        for volume in volumes:
            self.connection.delete_volume(volume)

    def get_dissassociated_eip(self):
        addresses = self.connection.get_all_addresses()
        disassociated_addresses = []
        for address in addresses:
            if address.instance_id is None or address.instance_id is "":
                disassociated_addresses.append(address)
        return disassociated_addresses

    def delete_eip(self,addresses):
        for address in addresses:
            address.delete()

                               

