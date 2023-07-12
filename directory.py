class Directory:

    def __init__(self, name):
        self.name = name
        self.children = []

    def add_child(self, directory):
        self.children.append(directory)

    def find_child(self, name):
        for child in self.children:
            if child.name == name:
                return child
        return None

    def remove_child(self, directory):
        self.children.remove(directory)

    def list_contents(self, indent, path=''):
        print((' ' * indent) + path + self.name)
        for child in self.children:
            child.list_contents(indent + 1, path=self.name)

    # def list_contents(self, path='',indent=0):
    #     print('  ' * indent + path + self.name)
    #     for child in self.children:
    #         child.list_contents(self.name, indent + 1)


    def __repr__(self):
        return self.name


def process_commands(commands):
    root = Directory(' ')

    for command in commands:
        parts = command.split()

        if parts[0] == 'CREATE':
            current_dir = root
            for part in parts[1:]:
                child_dir = current_dir.find_child(part)
                if child_dir is None:
                    new_dir = Directory(part)
                    current_dir.add_child(new_dir)
                    current_dir = new_dir
                else:
                    current_dir = child_dir
            
            print(f"CREATE {'/'.join(parts[1:])}")

        elif parts[0] == 'MOVE':
            source_parts = parts[1].split('/')
            destination_parts = parts[2].split('/')

            source_parent = root
            for part in source_parts[:-1]:
                source_parent = source_parent.find_child(part)

                if source_parent is None:
                    break

            source_dir = source_parent.find_child(source_parts[-1])
            if source_dir is None:
                print(f"Cannot move {parts[1]} - directory does not exist")
                continue

            destination_parent = root
            for part in destination_parts[:-1]:
                destination_parent = destination_parent.find_child(part)

                if destination_parent is None:
                    break
            
            if destination_parent is None:
                print(f"Cannot move {parts[1]} - destination directory does not exist")
                continue

            destination_parent.add_child(source_dir)
            source_parent.remove_child(source_dir)

            print(f"MOVE {parts[1]} {parts[2]}")

        elif parts[0] == 'DELETE':
            delete_parts = parts[1].split('/')
            delete_parent = root
            for part in delete_parts[:-1]:
                delete_parent = delete_parent.find_child(part)

                if delete_parent is None:
                    break

            if delete_parent is None:
                print(f"Cannot delete {parts[1]} - {parts[1]} does not exist")
                continue

            delete_dir = delete_parent.find_child(delete_parts[-1])
            if delete_dir is None:
                print(f"Cannot delete {parts[1]} - {parts[1]} does not exist")
                continue

            delete_parent.remove_child(delete_dir)

            print(f"DELETE {parts[1]}")

        elif parts[0] == 'LIST':
            print("LIST")
            root.list_contents()

        else:
            print(f"Invalid command: {command}")

        print()


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
