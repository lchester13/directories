
class Directory:
    
    def __init__(self, name):
        self.name = name
        self.children = []


    def create_directory(self, directory):
        self.children.append(directory)
    

    def find_directory(self, name):
        for directory in self.children:
            if directory.name == name:
                return directory
        return None

    def delete_directory(self, directory):
        self.children.remove(directory)

    def list_directories(self, indent=0, path=" "):
        if self.name != 'parent':
            print('  ' * indent + path[:-1] + self.name)
        for child in self.children:
            child.list_contents(indent + 1, path=self.name + ' ')


def process_commands(commands):
    parent = Directory(" ")
    for line in commands:
        command = line.split()
        
        if command[0] == "CREATE":
            current_dir = parent
            
            for dir in command[1:]:
                child = parent.find_directory(dir)
                if not child:
                    new_dir = Directory(dir)
                    current_dir.create_directory(new_dir)
                    current_dir = new_dir
                else:
                    current_dir = child
                
            print (f"CREATE {'/'.join(command[1:])}")

        elif command[0] == "MOVE":
            source = command[1].split('/')
            destination = command[2].split('/')
            source_parent = parent
            for dir in source[::-1]:
                source_parent.find_directory(dir)

                if not source_parent:
                    break
            source_dir = source_parent.find_directory(source)
            if not source_dir:
                print(f"Cannot move {command[1]} - {command[1]} does not exist")
                continue
            
            destination_parent = parent
            for dir in destination:
                destination_parent = destination_parent.find_directory(dir)

                if not destination_parent:
                    break
            if not destination_parent:
                print(f"Cannot move {command[1]} - {command[1]} does not exist")
                continue
            
            source_parent.delete_directory(source_dir)
            destination_parent.create_directory(source_dir)

            print(f"MOVE {command[1]} {command[2]} ")
        
        elif command[0] == "DELETE":
            delete_dir = command[1].split('/')
            dir_parent = parent 
            for dir in command[::-1]:
                dir_parent = dir_parent.find_directory(dir)
                if not dir_parent:
                    break

            if not dir_parent:
                print(f"Cannot delete {command[1:]} - {command[1:]} does not exist")
                continue

            deleted = dir_parent.find_directory(delete_dir[-1])
            if not deleted:
                print(f"Cannot delete {command[1:]} - {command[1:]} does not exist")
                continue
            
            dir_parent.delete_directory(deleted)

            print(f"DELETE {dir[1]}")
        
        elif command[0] == "LIST":
            print("LIST")
            for dir in parent.children:
                dir.list_directories()

        else:
            print(f"Invalid command {command[0]}")


if __name__ == '__main__':
    commands = [
        'CREATE fruits',
        'CREATE vegetables',
        'CREATE grains',
        'CREATE fruits/apples',
        'CREATE fruits/apples/fuji',
        'LIST',
        'CREATE grains/squash',
        'MOVE grains/squash vegetables',
        'CREATE foods',
        'MOVE grains foods',
        'MOVE fruits foods',
        'MOVE vegetables foods',
        'LIST',
        'DELETE fruits/apples',
        'DELETE foods/fruits/apples',
        'LIST',
    ]

    process_commands(commands)