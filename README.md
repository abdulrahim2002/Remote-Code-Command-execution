# Remote Code and Command Execution

A python implementation of remote code/command execution. Using the code you can connect 2 machines and remotely execute commands from one machine to another. Initially implemented as telnet client, It also features live video streaming/screen sharing. Which means that while executing commands on the remote machine you can see what change those executions are making. **Batch scripts are used to file programs within programs**.

# Video Demonstration

Watch on youtube: [youtube link](https://youtu.be/2l4CWBmEw50)

### Part 1
https://github.com/abdulrahim2002/Remote-Code-Command-execution/assets/89011337/362e68f7-d01b-483f-99d9-5988dba84b22

### Part 2
https://github.com/abdulrahim2002/Remote-Code-Command-execution/assets/89011337/18361527-01f2-4a9d-8b83-0edd5ef8cf14


## Features

* **Live screen sharing**
* Remotely **use** **server machine's keyboard**. 
    e.g. usage: you can open a text file on the remote machine. then you can write anything in that text file using !! before your text written in prompt. Once done you can save the file using !ctrl~s Command.

* Authentication. The server machine is secured by **OTP(one time password)** which is generated at runtime randomly.
  
# Working
The client machine sends commands to server machine, where they get executed, and the result is returned. The client machine can also **write something using server's keyboard**. The client's machine can also **send shortcuts** like ctrl+s(save) and win+d(jump to desktop), alt+tab(next program). The possibilities are endless, with what you can do with it.

## Authors

- [@amrindersingh](co20305@ccet.ac.in)
- [@abdulrahim2002](co20301@ccet.ac.in)
