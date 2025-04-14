# Project 4: Secure Log File
## CMSC368 Spring 2025

Part 1 (Build it) Due April 24
Part 2 (Break it) Due May 1


Overview
--------

In this project, you will implement a *secure log* to describe the *state of an art gallery*: the guests and employees who have entered and left, and individuals that are in various rooms. The log will be used by *two programs*. One program, `logappend`, will append new information to this file, and the other, `logread`, will read from the file and display the state of the art gallery according to a given query over the log. Both programs will use an authentication token, supplied as a command-line argument, to authenticate each other. Specifications for these two programs and the security model are described in more detail below.

You will build the most secure implementation you can; then you will have the opportunity to attack other teams' implementations.

You may work in teams of up to three people. Choose a team name and then complete the "pre-assignment" on Gradescope to let Erica know who is on your team. Make sure you include both your team name and the names of all team members in your writeups.

You can choose to write your implementation in C or Python. There is some basic starter code available in C.

Important note: This project is based on a secure programming contest called Build it, Break it, Fix It, which was developed at UMD. Your grade for the project is separate from the original contest scoring system. In particular, during the Break It phase, finding an attack on your classmates' projects has no effect on their project grade. My goal is to foster a friendly spirit of competition --- you are free to attack your friends' implementations without worrying that you might negatively affect their project grade.

Deliverables
------------
**Part 1: Build it**

For this part of the project, you will submit:  

+ Your implementation, including all your code files and your makefile.
+ A **design document** (PDF) in which you:
    + Describe your overall system design, in sufficient detail for a reader to understand your approach without reading the source code directly. This must include a description of the format of your log file.
    + List four specific attacks you have considered, and describe how your implementation counters these threats. (Please note the relevant lines of code for your defense.) If you were not able to completely (or at all) prevent a threat you identified, you may still mention it; in that case, describe any partial mitigation you implemented and explain anything you wanted to implement but were for whatever reason unable to. Please be clear about distinguishing what you have implemented vs. what you _would have_ implemented.

**Part 2: Break it**

You will be assigned three teams' implementations to examine. You should submit:  

+ A vulnerability analysis document (PDF). Choose *one* of your assigned implementations and describe:
    + Any attacks you found, including a high-level summary and enough detail for someone to replicate the attack.
    + Any vulnerabilities you found but were unable to exploit for whatever reason.
    + If you did not find any attacks or vulnerabilities, describe how you looked for attacks. 
+ Any code you wrote to implement your attack. Make sure the vulnerability analysis explains how to use your code to launch the attack.

If you demonstrate a working security break, then your vulnerability analysis document only needs to include your description of that one vulnerability, you don't need to go any further.

Please note: you can report correctness bugs for fun and bragging rights, but they do not count for your vulnerability analysis -- for this analysis, you must identify security-relevant issues.

If one of your assigned implementations is not complete or well-functioning enough for meaningful analysis, you may request an alternate implementation from an instructor.

Grading
-------

**Part 1** (submitted as a group) will be worth 100 points:

+ 30 points for (hidden) correctness tests.
+ 70 points for your design document: 
    + 10 points for your description of your approach 
    + 15 points for each of the four specific vulnerabilities you defend against. For maximum points, your defense should be correct, fully implemented, and well explained. Well explained attacks that are not fully implemented will receive partial credit.
    + Extra credit will be given for up to one extra attack/countermeasure beyond the original four.

You are encouraged to keep performance in mind while building your implementation, but performance does not explicitly factor into your grade (except that the correctness tests in my grading scripts will time out after 30 minutes). 

**Part 2** (again submitted as a group) will be worth 25 points:

+ A successful attack with a well written explanation of the vulnerability and attack will receieve full credit.
+ If you do not have a successful attack, then you must write a complete vulnerability analysis for **one** of the three implementations you were assigned. This analysis must explain either why you could not implement an attack you identified, or provide a convincing argument that there were no exploitable vulnerabilities.

**Part 3** is a short written reflection (written and submitted individually) worth 10 points:

+ 5 points for a ~1 paragraph summary of your individual contributions to the project (this can include features you implemented, taking the lead on scheduling, etc.). Administrative duties like scheduling are valuable contributions, and can definitely be included in your summary! However, it is expected that each group member will actively take part in the core project tasks (building and breaking), and that groups will aim to split the project workload relatively evenly among group members.
+ 5 points for a thoughtful ~1 paragraph reflection of one thing you would fix or change in your project, given more time. (Or, if there's nothing you would fix or change, describe one of the decisions you made that led to a faultless end product!)

Programs
--------
Your team will design a log format and implement both `logappend` and
`logread` to use it. Full descriptions for each program appear `LOGAPPEND.md` and `LOGREAD.md`, respectively.

 * The `logappend` program appends data to a log.
 * The `logread` program reads and queries data from the log.

Look at the Examples section for examples of using the `logappend` and `logread` tools together. 

Security Model
--------------
The system as a whole must guarantee the privacy and integrity of the log in the presence of an adversary that does not know the authentication token. This token is used by both the `logappend` and `logread` tools, and is passed as an argument on the command line. *Without knowledge of the token*, an attacker should *not* be able to:

* Query the logs via `logread` or otherwise learn facts about the names of guests, employees, room numbers, or times by inspecting the log itself.
* Modify the log via `logappend`.
* Fool `logread` or `logappend` into accepting a bogus log file. (In particular, modifications made to the log by means other than correct use of `logappend` should be detected by subsequent calls to `logread` or `logappend` when the correct token is supplied.)


Build-it Round Submission
-------------------------
You will submit your code for this project on Gradescope.

Please note: you **must not share your implementation outside of current 368 faculty and students.** By following this policy, you are preserving the integrity (and I hope, the joy!) of this project for future generations of students at Reed (and other institutions that run these projects). If you have any questions or concerns about this policy, please don't hesitate to reach out to me.

To submit your code: put all your code in a top-level directory called `build`. Your submission will be scored after every push to the repository.

When I grade your submission, I will invoke `make` (without arguments) in the `build` directory of your submission. The only requirements on `make` are that it  must function without internet connectivity, it must return within ten minutes, and it must build from source (for this project, committing binaries/executables only is not acceptable). We will provide a sample makefile for C.

Once `make` finishes running, `logread` and `logappend` should be executable files within the `build` directory. My testing scripts will invoke them with a variety of options and measure their responses. **The executables must be able to be run from any working directory.** 

Break-it Round Submission
-------------------------

For the break-it round, you will be providing test cases that provide evidence of a bug in one of your assigned target implementations. Bugs can include correctness violations, crashes,  integrity violations, and confidentiality violations. Further details will be forthcoming when we get closer to the beginning of the break-it round.
