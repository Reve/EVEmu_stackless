# EVEmu_stackless

# What are the benefits of this Python variant?

A small advantage is that recursions are no longer limited by the size of the C stack, but only by the amount of available heap memory. But that's not the major point.

Stackless Python allows you to run hundreds of thousands of tiny tasks, called "tasklets", in a single main thread. These tasklets can run completely decoupled, or they can communicate via "channels". Channels take all the responsibility to control suspension and resuming of tasklets in a very easy-to-manage manner.

Furthermore, the concept of small, communicating tasklets can lead you to a new, very simple way of formulating your problems. [--much more to be said here--]

# How does this work?

Without delving into the (complicated) implementation details, the following is relevant: The Python interpreter is recursive. That is, for every invocation of a Python function or method, another incarnation of the interpreter is called from C code. By decoupling the execution of Python code from the C stack, it is possible to change the order of execution. In particular, this allows to switch between multiple concurrent running "threads" of Python code, which are no threads in the sense of the operating system, but so-called "green threads".

Although in alpha state, Stackless is being heavily used by commercial applications. One outstanding example is the Massive MultiPlayer Online Game EVE http://www.eve-online.com/ which is completely based upon Stackless technology.

# And is this efficient?

Oh well! As a measure of efficiency, here a couple of numbers:

With today's most efficient operating system threads on a specially modified Linux variant and 1 GB main memory, it is possible to run about 100.000 Threads. The switching rate is somewhere better than 1 million per second..

With its tiny Python tasklets, Stackless accomplishes similar performance within only 100 MB, but creating a million tasklets.

In conclusion, Stackless Python is very efficient and especially suited for simulations with very many autonomous tiny objects.

# Is Stackless different from Standard Python?

Stackless is completely compatible with Standard Python, it just adds some functionality. The interpreter is changed internally, but there is no change of behavior, unless the Stackless features are used.

# Need I say more? ...tought so

## EVEmu server written in it's original language.

## No functionality at the moment. Stay tuned...
