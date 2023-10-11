#!/usr/bin/python3
import cmd
import inspect
import models
from models.base_model import *
from models.engine.file_storage import FileStorage


class HBNBCommand(cmd.Cmd):
    """Inherits Cmd"""

    # override the default prompt
    prompt = '(hbnb) '

    def do_quit(self, line) -> None:
        """Quit command to exit the program
        """
        exit(1)

    def do_EOF(self, line) -> bool:
        """Return True
        """
        return True

    def emptyline(self) -> None:
        """
        Overrides emptyline in the super class so that
        an empty line + ENTER shouldn’t execute anything
        """
        pass

    def do_create(self, line) -> None:
        """
        Creates a new instance of BaseModel,
        saves it (to the JSON file) and prints the id
            Example:
                $ create BaseModel
        """
        # get all the classes defined in the base_model module
        classes = [cls for name, cls in inspect.getmembers(
            models.base_model, inspect.isclass)]
        # get the names of all the classes
        class_names = [cls.__name__ for cls in classes]

        if line is not None and len(line) != 0:
            if line in class_names:
                instance = eval(line + '()')
                instance.save()

                print(instance.id)
            else:
                print("** class doesn't exist **")
        else:
            print('** class name missing **')

    def do_show(self, line):
        """
        prints the string representation of an instance based
        on the class name and id
            Examle:
                $ show BaseModel 1234-1234-1234
        """
        args_list = line.split()
        if len(args_list) == 2:
            models.storage.reload() # get all data stored in a file
            obj = models.storage.all() # get the dict of contents of the file invoked above
            key = args_list[0] + '.' + args_list[1]
            if key in obj:
                print(obj.get(key))
            else:
                print('** no instance found **')
        elif len(args_list) < 1:
            print('** class name missing **')
        else:
            print('** instance id missing **')

    def do_destroy(self, line) -> None:
        """
        Deletes an instance based on the
        class name and id (save the change into the JSON file).
            Example:
                $ destroy BaseModel 1234-1234-1234
        """
        args_list = line.split()
        if len(args_list) == 2:
            models.storage.reload()
            obj = models.storage.all()
            key = f"{args_list[0]}'.'{args_list[1]}"
            if key in obj:
                del obj[key]
                models.storage.save()
            else:
                print('** no instance found **')
        elif len(args_list) < 1:
            print('** class name missing **')
        else:
            print('** instance id missing **')

    def do_all(self, line) -> None:
        """
        Prints all string representation of
        all instances based or not on the class name
            Example:
                $ all BaseModel
                $ all
        """
        models.storage.reload()
        obj = models.storage.all()
        if line is not None and len(line) != 0:

            for key in obj:
                if line in key:
                    print(obj.get(key))
                else:
                    print('** class doesn\'t exist **')
        else:
            for key in obj:
                print(obj.get(key))

    def do_update(self, line) -> None:
        """
        Updates an instance based on the class name and id by adding or \
            updating attribute (save the change into the JSON file).
        Only one attribute can  be updated at the time
            Example:
                $ update BaseModel 1234-1234-1234 email "aibnb@mail.com"
            Usage: update <class name> <id> <attribute name> "<attribute value>"
        """
        args_list = line.split()
        if len(args_list) > 4:
            del args_list[4:]
        elif len(args_list) == 0:
            print('** class name missing **')
        else:
            models.storage.reload()
            obj = models.storage.all()


        match len(args_list):
            case 0:
                
            # case 1:
            #     print('** instance id missing **')
            case 2:
                print('** attribute name missing **')
            case 3:
                print('** value missing **')
            case 4:

                
                for key in obj.keys():

                    if not (args_list[0] in key):
                        print('** class doesn\'t exist ** ')
                    else:

                        match len(args_list):
                            case 4:
                                key = f"{args_list[0]}.{args_list[1]}"
                                if key in obj:
                                    instance = obj[key]
                                    setattr(instance, args_list[2], args_list[3])
                                    instance.save()
                                else:
                                    print('** no instance found **')
                


if __name__ == '__main__':
    HBNBCommand().cmdloop()
