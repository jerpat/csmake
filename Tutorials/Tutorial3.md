Tutorial 3: Using Aspects

In this tutorial, you will learn:

    Basics of how aspects work in csmake
    Basics of how flow control advice works in csmake
    How to use csmake to help work around otherwise unfixable failures

This tutorial requires a 64-bit Linux (amd64) debian-based distro operating system.

It is assumed that you have some familiarity with the concept of Aspect-Oriented Programming (AOP)

If you would like to learn a little about AOP, this Wikipedia article is a good place to start.
Aspect-Oriented Concepts in csmake

Generally, there are a couple of ways to weave in cross-cutting concerns into the execution of a program.  csmake exclusively uses explicit pointcuts, that is, there are no conditional query types of pointcuts implemented by csmake. Aspects in csmake attach to various predefined pointcuts by implementing joinpoints that are executed when advised.  The weaving is dynamic weaving, i.e., done at execution time.  Modules in csmake can expand the set of pointcuts to suit the needs of its execution to be modified by cross cutting concerns.  Some of these expansions also allow for a limited form of a pointcut query by, for example, only advising joinpoints if the step is processing a specific type of file, like in the Packager module.

A lesser known concept of flow control advice provides a way for the aspects to provide advice to give back to the main concern of execution for how it should proceed after the aspects complete handling the joinpoint advice.  This allows an aspect to decide if, for example, a module should skep execution altogether, try execution again, etc.  Specific modules may also expand the kinds of advice an aspect can give back to the main concern - for example, in a DIB build of an image, an aspect can advise that a specific script be skipped or repeated.

Now, let's dig in to aspects in csmake!
Step 1: Ensure csmake is installed

This exercise uses csmake.  If you do not have version 1.3.2 or later of csmake, please install that now
Step 2: Create a New Directory for the Tutorial
mkdir Tutorial3
cd Tutorial3
Step 3: Create a csmakefile that Intentionally Fails

Create a csmakefile under Tutorial3 directory 
# First define a simple shell behavior that will fail without an intervention
[Shell@a-step]
command= set -eux
  ls file.doesnt.exist
 
[command@]
00=a-step

 Now watch it fail:
$ csmake build
 ___  ______  ______  ______  ______  ______  ______  ______  ______  ___
  __)(__  __)(__  __)(__  __)(__  __)(__  __)(__  __)(__  __)(__  __)(__
 (______)(______)(______)(______)(______)(______)(______)(______)(______)
 
     Begin csmake - version 1.3.2
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
++ Shell@a-step      ---  Begin
------------------------------------------------------------------
+ ls file.doesnt.exist
ls: cannot access file.doesnt.exist: No such file or directory
------------------------------------------------------------------
 .:*~*:._.:*~*:._.:*~*:.   Step: Failed   .:*~*:._.:*~*:._.:*~*:.
------------------------------------------------------------------
++ Shell@a-step      ---  End
------------------------------------------------------------------
__)__)__)__)__)__)__)__)__)__)__)__)__)__)__)__)__)__)__)__)__)__)
 
command@: ERROR    : Step 'a-step' FAILED
------------------------------------------------------------------
 .:*~*:._.:*~*:._.:*~*:.   Step: Failed   .:*~*:._.:*~*:._.:*~*:.
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
` ERROR    : csmake exited with code 1
------------------------------------------------------------------
  __   __   __   __   __   __   __   __   __   __   __   __   __   __   __
 _\/_ _\/_ _\/_ _\/_ _\/_ _\/_ _\/_ _\/_ _\/_ _\/_ _\/_ _\/_ _\/_ _\/_ _\/_
 \/\/ \/\/ \/\/ \/\/ \/\/ \/\/ \/\/ \/\/ \/\/ \/\/ \/\/ \/\/ \/\/ \/\/ \/\/
     csmake: Failed
------------------------------------------------------------------
     End csmake - version 1.3.2
------------------------------------------------------------------
 ___  ______  ______  ______  ______  ______  ______  ______  ______  ___
  __)(__  __)(__  __)(__  __)(__  __)(__  __)(__  __)(__  __)(__  __)(__
 (______)(______)(______)(______)(______)(______)(______)(______)(______)
Step 4: Add an Aspect that Runs on Failure, Fixes the Issue and Re-runs the Step

Modify your csmakefile to have the following contents 
[Shell@a-step]
command= set -eux
  ls file.doesnt.exist
 
[&ShellAspect@a-step]
command(failed__build)= set -eux
   touch file.doesnt.exist
advise(failed__build#1)=tryAgain:True
command(passed__build)= set -eux
   rm file.doesnt.exist
 
[command@]
00=a-step
 

 Now, try executing the build again:
$ csmake build
 ___  ______  ______  ______  ______  ______  ______  ______  ______  ___
  __)(__  __)(__  __)(__  __)(__  __)(__  __)(__  __)(__  __)(__  __)(__
 (______)(______)(______)(______)(______)(______)(______)(______)(______)
 
     Begin csmake - version 1.3.2
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
++ Shell@a-step      ---  Begin
------------------------------------------------------------------
+ ls file.doesnt.exist
ls: cannot access file.doesnt.exist: No such file or directory
    ___________________________________________________
    \  Begin Joinpoint: failed   
     ```````````````````````````````````````````````````
       _________________________________________
      |--               Aspect                --|
       \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
        ``````````````````````````````````````````
        &ShellAspect@a-step         ...  Begin
        ------------------------------------------
+ touch file.doesnt.exist
        ------------------------------------------
         ~~~~~~       Aspect: Passed       ~~~~~~     
        ------------------------------------------
        &ShellAspect@a-step         ...  End
        ------------------------------------------
        _________________________________________
       //////////////////////////////////////////
      |--             End Aspect              --|
       ``````````````````````````````````````````
 
     __________________________________________________
    /  End Joinpoint: failed
    ``````````````````````````````````````````````````
+ ls file.doesnt.exist
file.doesnt.exist
    ___________________________________________________
    \  Begin Joinpoint: passed   
     ```````````````````````````````````````````````````
       _________________________________________
      |--               Aspect                --|
       \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
        ``````````````````````````````````````````
        &ShellAspect@a-step         ...  Begin
        ------------------------------------------
+ rm file.doesnt.exist
        ------------------------------------------
         ~~~~~~       Aspect: Passed       ~~~~~~     
        ------------------------------------------
        &ShellAspect@a-step         ...  End
        ------------------------------------------
        _________________________________________
       //////////////////////////////////////////
      |--             End Aspect              --|
       ``````````````````````````````````````````
 
     __________________________________________________
    /  End Joinpoint: passed
    ``````````````````````````````````````````````````
 
------------------------------------------------------------------
 nununununununununununun   Step: Passed   nununununununununununun
------------------------------------------------------------------
++ Shell@a-step      ---  End
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
     End csmake - version 1.3.2
------------------------------------------------------------------
 ___  ______  ______  ______  ______  ______  ______  ______  ______  ___
  __)(__  __)(__  __)(__  __)(__  __)(__  __)(__  __)(__  __)(__  __)(__
 (______)(______)(______)(______)(______)(______)(______)(______)(______)
 

 Here we see that we can add an aspect to the failing step to patch up what is wrong if the step fails.  Let's walk through the syntax and what is going on with the ShellAspect
Aspect Declaration[&ShellAspect@a-step]

The section header has two qualities that makes it work as an aspect.  First, it the section name starts with an ampersand '&', this tells csmake (and human observers) to treat this section as an aspect (it is possible to have section types that can operate both as a regular section and as an aspect). 

The second thing to notice is that the section has the same id - this tells csmake to advise the aspect for the regular section with the same id.

You could read this section: "Tie the ShellAspect module into the a-step execution" (or "And do ShellAspect as part of a-step") if it's helpful to see why the syntax was chosen.

NOTE: it's possible to want to tie multiple instances of the same module in for a section.  If you do this, you have to give each aspect section its own unique id so that csmake will recognize that the sections are unique.  For example:
[&ShellAspect@a-step repairfile]
command(failed__build)= set -eux
    touch file.doesnt.exist
advise(failed__build#1)=tryAgain:True
 
[&ShellAspect@a-step cleanup-file]
command(passed__build)= set -eux  
    rm file.doesnt.exist

 If you replaced the original aspect section above with these two sections, you would have the exact same behavior, but across two different aspect sections.  If these aspect sections did not contain an "aspect id" of repairfile and cleanup-file respectively, then one would override the other (which is bad form, but that is the way INI style files work).
Aspect joinpoints - command(failed__build), command(passed__build)

The nice thing about the ShellAspect is that the joinpoints are exposed in the csmakefile which makes it easier to explain what is going on for, say, a tutorial!  Most aspect implementations will have specific behaviors for the joinpoints they want to implement and then document the behavior.  To see the full documentation for ShellAspect, do csmake --list-type=ShellAspect

(ShellAspect is a core module delivered with a csmake installation)

command(failed__build) - that's failed, double underscore, build - will execute when "failed" is advised by the main concern (i.e., the executing module fails) during a "build" phase.  If we said "command(execption__xyzzy)", for example, then the shell command would only execute if the main concern hits an exception during the xyzzy phase.  We can also just say "command(passed)" which would execute every time its main concern passes regardless of what phase is being executed.  For most aspect implementations, they would actually define methods with these kinds of names as opposed to having options.

So, for our ShellAspect section above, when the main concern (a-step) fails, which it will unless we start with a file.doesnt.exist file already in our current working directory, the command(failed__build) shell script will execute creating the file we want - it's that simple.

passed__build is just like failed__build except it will execute when the main concern passes its execution instead of fails.

 
Flow Control Advice - advise(failed__build#1)=tryAgain:True

This is admittedly a little cryptic, but it can be powerful.  This option in the ShellAspect section allows the section to give advice back to the main concern.  In this case, we want the main concern to try again once our step is completed.  If you look at the output above, or from your execution of the tutorial, you'll see the Shell section attempts its "ls" a second time, and succeeds.

Just as with the "command", the "advise" option can be placed on a specific joinpoint.  In a regular implementation of an aspect, you would vote or advise using a FlowControl object.

The '#1' at the end of the specific join point "failed__build" declares that this advice should only be given on the first time the main concern fails, so you could see:

advise(failed__build#1)=tryAgain:True
advise(failed__build#2)=tryAgain:True 
advise(failed__build#3)=tryAgain:True  

for example, which would tell the main concern to try again on the first, second, and third times it fails.

One thing you could do to see this would be to change the csmakefile so that the ShellAspect doesn't actually fix the problem and watch the main concern, a-step, fail twice.

After you do that, next try adding a "advise(failed__build#2)=tryAgain:True" and watch it fail 3 times. 
Learn More on Aspects in csmake

The man pages cover the topic of aspects in greater detail:

man csmake

talks about how aspects work in the "PHASES" section

man csmakefile

talks about aspects in the "ASPECTS" section

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

