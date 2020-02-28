# cfgur
Generic configuration framework UI

# FAQ
## What is cfgur?
This software seeks to solve configuration difficulties by creating an easy-to-use documentation organiser and config
simulator. It consists of three parts:
 - The parser, which takes in PDF-format manuals and converts them to a mutable database
 - The UI, which presents CLI information in an organised way and shows command availability and syntax
 - The simulator, which scans a configuration file and displays the net configuration result
 
## What is the parser?
The parser is a small, custom module used to parse documentation. A parser module must be written for each manual to 
be parsed. It uses syntax matching, formatting, and regular expressions to find the information it needs. It then 
converts it and places it into an in-memory CommandTree. From there, errata can be fixed, and the entire CommandTree
instance can be exported to a database, which can be imported by the UI.

## What can I do with the UI?
It's gtk. It's semi-fancy. You might like it!
You can see a list of every command parsed from the documentation, organised by whatever criteria you like.
You can see an explanation of the command, its syntax, security level, and any other piece of information parsed
from its respective doc.
You can type a commands into the simulator to see if the syntax is correct.

## What can I do with the simulator?
The simulator is a part of the UI which, at its core, simulates the machine you are trying to configure. You can check
the syntax of a command by typing it in - and discarding changes - or have the simulator save each command to export into
a complete configuration file. This file can then be loaded onto the actual machine Without Any Errors Whatsoever(tm).

## What's the license for this software?
The software itself is GPL. The parsed documentation is unrelated to the software and may have any licensing. You may not
be allowed to save some documentation as a database, or you may not be allowed to share the database with others. Fixing
errata may not be allowed as well. Please speak with the documentation authors for your machine for more details.

# Internals
## What is the CommandTree class?
The CommandTree is the root class which represents the CLI of the machine you're configuring. It contains the entire tree
of command modes, with one CommandMode class for each. These modes are accessible via dictionary keys. For example, if you
had a CommandTree called cmd_tree, and you wanted to access a mode called "User Mode", just do cmd_tree["User Mode"].
The CommandTree class contains a member called root_mode which it uses to represent the first mode accessible by a user 
when they log in.

## What is the CommandMode class?
The CommandMode is a representation of the state of the CLI at any given point. For example, if you're an unprivileged user
in your edge router, there is a CommandMode that represents that, and contains all the commands you're allowed to run within
that mode. Switching to privileged EXEC will change the mode, and give you a new (or extended) set of commands that you can
run. The privileged mode will have its own class instance, but may share Commands with other CommandModes.

## What is the Command class?
The Command class is just that - a class which represents a command. It will have some documentation, and a function to
determine whether an input string is a syntactically accurate execution of the command.
