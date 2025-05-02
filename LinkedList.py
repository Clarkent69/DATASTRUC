from node import Node
node1 = Node('A')

print(f"node1 data: {node1.data}")
print(f"node1 link: {node1.link}")

node1 = A
node1 = None

node2 = Node('B')
print(f"node2 data: {node2.data}")
print(f"node2 link: {node2.link}")

node3 = Node('M')
node4 = Node('P')

node1.link = node2

print (node1.link.data)
