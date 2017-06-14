Tutorial 4: Environment Variables

In this tutorial, you will learn:

    How to use environment variables in csmake

This tutorial requires a 64-bit :inux (amd64) debian-based distro operating system
Step 1: Ensure csmake is installed

This exercise uses csmake.  If you do not have version 1.3.2 or later of csmake, please install that now.
Step 2: Create a New Directory for the Tutorial
mkdir Tutorial4
cd Tutorial4
Step 3: Create a csmakefile with an environment variable and use it

Create a csmakefile under the Tutorial4 directory
[command@]
00=setup-env, use-env
 
[environment@setup-env]
a=%(c)s-list
c=my
 
[Shell@use-env]
command= echo %(a)s

Here we create two variables 'a' and 'c' and then just echo them out to stdout in a Shell. 

Notice that 'a' can refer to 'c'. Provided no circular references are created or references that require more than two levels of indirection to resolve, environment sections can refer to their own variables.

The "percent-sign, open, variable, close, 's'", %(a)s for example, is the way to refer to environment variables in csmake, and follows the pythonic dictionary name substitution syntax

Let's see the result using --quiet so we can just see the output of the steps:
$ csmake --quiet build
my-list

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

