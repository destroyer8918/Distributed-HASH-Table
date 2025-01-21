Distributed systems play a crucial role in modern computing. They enable
multiple devices to work together to complete tasks efficiently. These systems
are widely used in cloud computing, distributed databases, and peer-to-peer
networks. A key function of distributed systems is the storage and retrieval
of data. A Distributed Hash Table (DHT) is a decentralized mechanism for
storing and retrieving data across multiple devices. Unlike centralized systems,
DHTs do not rely on a single server, which makes them more scalable and
fault-tolerant.
Centralized systems manage data using a single server. While this approach
is simple, it has a major drawback. If the central server fails, the entire system
becomes unavailable. Distributed systems address this issue by distributing
responsibilities across multiple nodes. This improves the system’s reliability.
However, designing distributed systems introduces new challenges. For example,
data must be assigned to nodes in a way that ensures efficient storage and
retrieval. The system must also handle communication between nodes.
The main goal of this project is to create a distributed hash table that can
store and retrieve data efficiently. The system should avoid reliance on a central
server and distribute data evenly across all participating nodes. It should also
handle failures gracefully and ensure that stored data remains accessible. The
project uses hashing techniques to assign data to nodes. Each node follows a
predefined rule to decide which data it will store. These rules ensure that all
data is stored without duplication or loss.
Another goal is to establish communication between the nodes. The system
uses TCP sockets to enable data exchange between nodes. Each node must be
able to send and receive data requests. Communication ensures that the nodes
work together to achieve the system’s overall goals. The design also allows for
adding new nodes in the future. This makes the system scalable and adaptable
to larger datasets.
The project also aims to create a simple and user-friendly interface for inter-
acting with the system. Users should be able to store and retrieve data easily.
The interface will provide feedback to users about the status of their data. This
ensures that the system is accessible to users with minimal technical knowledge.
In summary, this project aims to build a distributed hash table system that
is efficient, scalable, and robust. It focuses on data distribution, inter-node
communication, and user interaction.
