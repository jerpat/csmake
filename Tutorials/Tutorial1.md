# Tutorial 1: Hello, csmake!

In this tutorial, you'll learn the basics of how csmake operates to construct a desired result.  In order to keep the tutorial easy to follow and execute, some of the finer points for this tutorial are reserved for the appendix at the end.
Goals for this Tutorial

    Gain a basic understanding of how to start a csmake project from scratch
    Understand the basic operation of a csmakefile specification and csmake
    Learn how to set up a basic build using csmake

## Step 1: Ensure csmake is installed
For this tutorial, you only need to have csmake installed.  If you haven't done this yet, please do this now.

## Step 2: Create a new directory to do the tutorial
```
mkdir csmake-tutorial-1
cd csmake-tutorial-1
```

## Step 3: Create a csmakefile
```
vi csmakefile
```
And in the editor enter

```
[Shell@hello]
command= echo "Hello, csmake!"
 
[command@]
0000=hello
```

Save this file as "csmakefile".  This defines a build that executes a shell script that echoes: Hello, csmake!.  See "Understanding the csmakefile" below.

## Step 4: Execute csmake
```
csmake build
```

You should see:
```
___  ______  ______  ______  ______  ______  ______  ______  ______  ___
  __)(__  __)(__  __)(__  __)(__  __)(__  __)(__  __)(__  __)(__  __)(__
 (______)(______)(______)(______)(______)(______)(______)(______)(______)
     Begin csmake - version 1.3.1
------------------------------------------------------------------
` WARNING  : Phase 'build' not delcared in ~~phases~~ section
` WARNING  :   Run: csmake --list-type=~~phases~~ for help
       _   _   _   _   _   _   _   _   _   _   _   _   _   _   _   _
    ,-(_)-(_)-(_)-(_)-(_)-(_)-(_)-(_)-(_)-(_)-(_)-(_)-(_)-(_)-(_)-(_)
    `-' `-' `-' `-' `-' `-' `-' `-' `-' `-' `-' `-' `-' `-' `-' `-'
         BEGINNING PHASE: build
__________________________________________________________________
  (  (  (  (  (  (  (  (  (  (  (  (  (  (  (  (  (  (  (  (  (  (
------------------------------------------------------------------
+ command@      ---  Begin
------------------------------------------------------------------
__________________________________________________________________
  (  (  (  (  (  (  (  (  (  (  (  (  (  (  (  (  (  (  (  (  (  (
------------------------------------------------------------------
++ Shell@hello      ---  Begin
------------------------------------------------------------------
Hello, csmake!
------------------------------------------------------------------
 nununununununununununun   Step: Passed   nununununununununununun
------------------------------------------------------------------
++ Shell@hello      ---  End
------------------------------------------------------------------
__)__)__)__)__)__)__)__)__)__)__)__)__)__)__)__)__)__)__)__)__)__)
------------------------------------------------------------------
 nununununununununununun   Step: Passed   nununununununununununun
------------------------------------------------------------------
+ command@      ---  End
------------------------------------------------------------------
__)__)__)__)__)__)__)__)__)__)__)__)__)__)__)__)__)__)__)__)__)__)
         ENDING PHASE: build
       _   _   _   _   _   _   _   _   _   _   _   _   _   _   _   _
    ,-(_)-(_)-(_)-(_)-(_)-(_)-(_)-(_)-(_)-(_)-(_)-(_)-(_)-(_)-(_)-(_)
    `-' `-' `-' `-' `-' `-' `-' `-' `-' `-' `-' `-' `-' `-' `-' `-'
` WARNING  : Phase 'build' not delcared in ~~phases~~ section
` WARNING  :   Run: csmake --list-type=~~phases~~ for help
   SEQUENCE EXECUTED: build
------------------------------------------------------------------
  .--.      .--.      .--.      .--.      .--.      .--.      .--.      .
:::::.\::::::::.\::::::::.\::::::::.\::::::::.\::::::::.\::::::::.\::::::
'      `--'      `--'      `--'      `--'      `--'      `--'      `--'
     csmake: Passed
------------------------------------------------------------------
     End csmake - version 1.3.1
------------------------------------------------------------------
 ___  ______  ______  ______  ______  ______  ______  ______  ______  ___
  __)(__  __)(__  __)(__  __)(__  __)(__  __)(__  __)(__  __)(__  __)(__
 (______)(______)(______)(______)(______)(______)(______)(______)(______)
```

If you execute csmake with the --quiet option, like this:
```
csmake --quiet build
```

Then you will see:
```
Hello, csmake!
```

The --quiet option suppresses the csmake output that provides guideposts for what the tool is doing.  While it can be quite verbose, the purpose is to help navigate and understand exactly what the tool is doing for complex builds (like DIB appliance builds, for example).  The output is designed to provide quick visual queues to sort through tremendous amounts of otherwise un-human-parsable output to find and pinpoint problems quickly.  There are times, however, when it is useful to strip this output away so that the actual results of performing the steps can be seen together, –quiet will help a user see this.  --quiet along with --dev-output can be helpful as well for tracking down issues when csmake performs a step or fails to perform a step that you thought it should not or should.

### Tutorial 1 Appendix

This appendix is designed to help gain a finer understanding of the reasons why the above steps worked, and what you can do to get a better understanding of how csmake operates.

#### Understanding the csmakefile

The csmakefile is basically a modified "INI" style file.  Just like with an INI file, a csmakefile has sections and key-value pairs for each section.  The csmakefile has a slightly more specific format than a regular "INI" file. For example, each section definition is of the form:
```
[<section type>@<id>]
```

The \<section type\> is implemented by a specific kind of python module that has been defined in a CsmakeModules directory (later tutorials will explore how CsmakeModules directories work).  The \<id\> is simply just a handle to allow you to distinguish between sections of identical type and for ease of reference.

You may note that csmakefiles are declarative, that is, their purpose (like with SQL, for example) is simply to state what should happen.  This may feel somewhat cumbersome at times, because you must fully declare what you expect the build to do.  Everything you see in the specification has been defined as a module, even clear down to the control sections such as "command" that you see above.

The key-value pairs provided under a given section are consumed by the section type module implementation.  These key-value pairs are extremely free-form, which makes it easy to express just about anything that is necessary to express in a csmakefile.  This, however, can also make csmakefiles feel complex and unwieldy as it appears that the form, structure, and syntax of a csmakefile will flow in almost a natural language feel because each section can define the kind of syntax it can take in (while keeping with the "INI" type key-value basic syntax). The values of a csmakefile key-value pair can also be multiline.  In an INI file a key must start in the first column, not contain spaces, and be followed by an '=' (equals) sign.  If any one of these conditions are not met, the line in the csmakefile specification will be part of the previous key.  For example:
```
[MySectionType@my]
single_line=This is a value passed in for 'my'
multi_line= This is
 another=value
 *   passed in
 to the section 'my'
```
The single\_line result that the section implementation sees is literally "This is a value passed in for 'my'"

The multi\_line result that the section implementation sees is literally:
```
 "This is\nanother=value\n*   passed in\nto the section 'my'"
```
Notice first, that any leading and trailing white space for a multiline value is discarded.  There are times when the whitespace can be meaningful, so use of a delimiter like '\*' as seen above, is used to keep the left side spacing correct (putting a patch inline or, say, python code in a build specification may require the use of a left-hand-side (lhs) delimiter to denote where the left hand side of the lines start and  process the contents based on this as necessary.

Because of the possibility of various input styles for a given section, a given csmakefile can appear hard to read, disjoint, and vary in syntax.  As mentioned above, the syntax of the file itself is very regular and specific, but is extremely flexible, allowing for bash scripts, next to simple string input, next to some python code.  Every section specified in the csmakefile has documentation associated with it that can be accessed using --list-type.  For example:
csmake --list-type=Shell

Will list the documentation for the "Shell" module.  You can also list all of the available types using "--list-types".  The documentation for the sections available from the current working directory will be output in (ASCII) alphabetical order, meaning capital lettered sections will be listed before lower case sections.  This is actually helpful here because by convention, the "core" or "special" csmake sections should all start lowercase.  Some examples of these special sections include: command, subcommand, include, metadata, versioning, etc.

Here's a full example of requesting the documentation for one of the most key modules, command:

#### command Documentation Example
```
$ csmake --list-type=command

___________________________________________________
Section Type: command
Path:         /usr/lib/python2.7/dist-packages/Csmake/CsmakeModules
----Info----
Library: csmake
Purpose: Execute a series of build steps - the initial step is
         a command seeded by the command line input (see --command)
Phases: *any*
Options: The keys are used to order the steps lexicographically
       1, 10, 2, 20, 200, 3, A, a (suggestion use 00-99)
       The values are atomic groups of steps
          , - denotes step follows the next
          & - denotes steps that can be run in parallel
Example:
    [command@build]
    description = "This will build a small pond"
    00 = init
    01 = repo1 & repo2 & repo3, repo4
    02 = createPond
    03 = stockFish
```
Understanding the csmake command line

The basic csmake command line structure is:
csmake <flags> <phases>

where <flags> are the list of flags that is listed by doing --help and <phases> is one or more build phases.
--command

The most important flag is --command.  This flag tells csmake where to begin building.  If this is unspecified, csmake will look for a command section to execute starting with looking for "command@" (that is a command section in the csmakefile with no id), failing this, it will look for "command@default" and failing this, it will grab the first command section it finds (which may or may not be the topmost command section in the csmakefile - remember that csmakefiles are declarative and use an INI format, which means that ordering of processing is not guaranteed to be in file order.  This is why, for example, the keys for the options to a command that execute other csmake sections are specified to be executed in alpha-numeric order. Likewise, the keys in each section are not  necessarily processed from top to bottom.

Commands that are available to use with --command may be listed by using --list-commands with csmake.  Here's an example from our CloudSystem appliance build repository (cloudsystem-appliance-build):
--list-commands Example
$ cd path/to/your/cloudsystem-appliance-build
$ csmake --list-commands
 
================= Defined commands =================
    local - Setup a local build - must be used with an appliance build
e.g., --command=local, base-foundation
    jenkins - Setup a jenkins build - must be used with an appliance build
e.g., --command=jenkins, base-foundation
    rc - Setup an rc build - must be used with an appliance build
    pr - Setup a partner release build - must be used with an appliance build
    base-mgmt - Create a first phase base image for the management appliance
    base-foundation - Create a first phase base image for the foundation appliance
    base-enterprise - Create a first phase base image for the enterprise appliance
    partner-enterprise - Create a second (partner) phase image for the enterprise appliance
    base-swift - Create a first phase base image for the swift appliance
    base-monasca - Create a first phase base image for the monasca appliance
    base-update - Create a first phase base image for the update appliance
    base-sdn - Create a first phase base image for the sdn appliance
    mgmt - Create a management appliance from a base management image
    foundation - Create a foundation appliance from a base foundation image
    enterprise - Create a enterprise appliance from a base enterprise image
    swift - Create a swift appliance from a base swift image
    monasca - Create a monasca appliance from a base monasca image
    update - Create an update appliance from a base swift image
    sdn - Create an sdn appliance from a base swift image
    local-base-mgmt - (Local) Create a first phase base image for the management appliance
    local-base-foundation - (Local) Create a first phase base image for the foundation appliance
    local-base-enterprise - (Local) Create a first phase base image for the enterprise appliance
    local-partner-enterprise - (Local) Create a second (partner) phase image for the enterprise appliance
    local-base-swift - (Local) Create a first phase base image for the swift appliance
    local-base-monasca - (Local) Create a first phase base image for the monasca appliance
    local-base-update - (Local) Create a first phase base image for the update appliance
    local-base-sdn - (Local) Create a first phase base image for the sdn appliance
    local-mgmt - (Local) Create a management appliance from a base management image
    local-foundation - (Local) Create a foundation appliance from a base foundation image
    local-enterprise - (Local) Create a enterprise appliance from a base enterprise image
    local-swift - (Local) Create a swift appliance from a base swift image
    local-monasca - (Local) Create a monasca appliance from a base monasca image
    local-update - (Local) Create a update appliance from a base update image
    local-sdn - (Local) Create a sdn appliance from a base sdn image
============= Suggested Multicommands ==============
    local, <appliance>: builds a local build of the appliance
    : NOTE: edit csmakefile to point to your cloudsystem
    jenkins, <appliance>: does a jenkins build of the appliance
    rc, <appliance>: does an rc versioned build of the appliance
    pr, rc, <appliance>: does a partner release release candidate
    pr, <appliance>: does a final partner release
    <appliance>: does a final release

The documentation associated with the commands are provided from the actual command sections from the "description" option of the command
Phases

Phases are used to control the actions or set of actions each module will take based on what is called out in the csmakefile.  When a phase is specified on the csmake command line, csmake will dispatch that message to the implementation of every build section from the --command specified in csmake.  So, for example," csmake build" will tell csmake to send "build" to every section's implementation instance when executing. "csmake clean" would send "clean" to every section implementation.  "csmake clean build" would send "clean" to every section specified in the default command, followed by sending "build" to the same sections.

Optionally, a csmakefile may contain a "~~phases~~" section which is a built in csmake module.  The documentation for the section may be obtained in the standard way described above: csmake --list-type=~~phases~~.  Phases will give a short description of all the valid phases, combination of phases, the default sequence of phases, and any suggested multicommands (a "multicommand" is when several commands are given to --command, e.g., csmake --command=local,foundation.  The information contained in the ~~phases~~ section can be accessed from the command line using "--list-phases".  Here is an example of list-phases from the cloudsystem-appliance-build repository:
--list-phases Example
$ cd /path/to/cloudsystem-appliance-build
$ csmake --list-phases
 
=================== Valid Phases ===================
clean_build: Cleans just the build directory for the given appliance build
build: Builds an appliance based on the given command(s)
clean: Cleans all build artifacts from the given command
clean_results: Cleans the given appliance build and results directories
=============== Valid Phase Sequences ==============
clean_results -> build:  Generates a clean build of an appliance
clean_results -> build -> clean_build:  Keeps only the results
Default sequence: clean_results -> build -> clean_build
   (Executed when phase(s) not given on command line)
============= Suggested Multicommands ==============
    local, <appliance>: builds a local build of the appliance
    : NOTE: edit csmakefile to point to your cloudsystem
    jenkins, <appliance>: does a jenkins build of the appliance
    rc, <appliance>: does an rc versioned build of the appliance
    pr, rc, <appliance>: does a partner release release candidate
    pr, <appliance>: does a final partner release
    <appliance>: does a final release

The command line can feel a bit overwhelming at first because the output for --help is currently very verbose.  However, csmake is designed to be executed with a minimum amount of flags and phases by defining defaults, while allowing users to customize specific builds by using other flags or specifying specific phases to execute. 

Several of the flags provide help:
--help - gives the flags available for use with csmake
--list-type=<module type> - provides help for a single section module type
--list-types - provides the help for all available section module types
--list-commands - provides a list of valid commands and multicommands (if specified in ~~phases~~) that can be used with a build
--list-phases - provides a list of valid phases, combinations of phases, the default combination of phases, and multicommands
                (if provided by a ~~phases~~ section)
--help-all - will dump all available information about what can be given on the command line to operate csmake for the current directory.

Some of the flags provide control over how much output csmake will provide. 

By default, csmake will provide all its visual cues and any WARNINGs and ERRORs (and CRITICALs and EXCEPTIONs) that a build produces. 

Here is a list of the flags that will help control levels of output:
--verbose - will also allow "INFO" sections.
--debug - will also allow "INFO" and "DEBUG" sections.
          This will also turn on any stack traces produced from a failed build or exception.
--quiet - Turn off all visual cues, Turn off all WARNING and ERROR messages.
--dev-output - will turn on very verbose output that describes the specific workflow csmake is executing,
               including decisions about when to, or to not execute a section, whether the dispatch of the phase
               to a section was successful (and what specifically was successful), the current operating environment
               before each section is executed, and any other information specified in a section's module
               implementation pertaining to what a module developer might need to understand
               why their module isn't working as expected.
               (the --dev-output flag operates independently of --quiet, --verbose, and --debug
                ... --quiet --dev-output together can sometimes be helpful to see only the csmake execution flow, for example)
--log - will send the csmake output to the path specified for --log.

The rest of the flags are used to control some aspect of the execution flow of csmake itself and are used less often in the course of doing everyday builds with csmake.  The documentation for these flags can be found by invoking --help.

<sub>This material is under the GPL v3 license:

<sub>(c) Copyright 2017 Hewlett Packard Enterprise Development LP

<sub>This program is free software: you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the
Free Software Foundation, either version 3 of the License, or (at your
option) any later version.

<sub>This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
Public License for more details.

<sub>You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

