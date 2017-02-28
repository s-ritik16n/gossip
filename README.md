# gossip
###Dining Philosophers Problem Simulation using Gossip Protocol

**Dining Philosophers Problem** is a standard model of synchronization of
processes running simultaneously on the same machine. The Philosophers
sit around a table with rice bowls, and there is a chopstick between every
two philosophers. The philosopher thinks, and then eats. When he picks up
the chopsticks next to him to eat, the two neighboring philosophers cannot
eat because one of the chopsticks on the side of each philosopher is used
by the philosopher eating. This represents the process synchronization
model where other processes have to wait if a process is in its critical
section.


**Gossip protocol** is a protocol which is based on peer-to-peer technology.
There a ​n nodes which are working together on a network. Each node ​X is
connected to one or ​ more other nodes. Node ​X can communicate with its
connected nodes to perform an action or to report an activity. It is useful in
many scenarios. Suppose, a firm has three servers A, B & C which share a
common database. A, B and C act as three nodes. A is connected to B and
C, B is connected to A and C, C is connected to A and B. When a user
performs transactions on server A, it sends signal to the other two servers(B
and C) to update according to the transaction performed by the user.
The project simulates the problem by representing philosophers as nodes.
Each philosopher can communicate with its neighbours to know if the
chopstick is under usage or free. Each node runs a timer for 5 seconds, as
hard coded in the program code to simulate the usage of chopsticks by
philosopher(s) while eating. After 5 seconds the philosopher releases the
chopsticks so that its neighbours can pick them to eat.
