from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

import random

# Initializes an empty node
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class CircularLinkedList: 
    def __init__(self):
        self.head = None
        
    # Adds a node to the circular linked list
    def append(self, data): 
        new_node = Node(data)
        if not self.head:
            # If the list is empty, the new node points to itself
            self.head = new_node
            self.head.next = self.head
        else:
            # If the list is not empty, traverse to the last node
            temp = self.head
            while temp.next != self.head:
                temp = temp.next
            # Insert new node at the end and make it point to head
            temp.next = new_node
            new_node.next = self.head

    # Creates an array containing all nodes
    def makeArray(self):
        arr = []
        if not self.head:
            return 0
        temp = self.head
        while True:
            arr.append(temp.data)
            temp = temp.next
            if temp == self.head:
                return arr
    
    # Removes a node from the circular linked list
    def remove(self, data): 
        if not self.head:
            return
        
        # Checks if the head needs to be removed
        if self.head.data == data:
            if self.head.next == self.head:
                # Only one node in the list
                self.head = None
            
            # More than one node in the list
            temp = self.head
            while temp.next != self.head:
                temp = temp.next
            temp.next = self.head.next  
            # Last node points to the new head
            self.head = self.head.next
            dialogBox.insert(END, f'Eliminated Player {data}.\n')
            return

        # Removes a non-head node
        prev = self.head
        current = self.head.next
        while current != self.head:
            if current.data == data:
                prev.next = current.next
                dialogBox.insert(END, f'Eliminated Player {data}.\n')
                return
            prev = current
            current = current.next

root = Tk()
root.title('Counting Out Game')
root.geometry('400x315') # Sets the window size of the program

# Shows error window when invalid N or K values are given
def invalid_NK():
    messagebox.showerror("Invalid", "Allowed Values:\n1 < N < 12\nK >= 1")

# Clears UI entry and dialog boxes in preparation for a new game
def newGame():
    removeNode(K_entry.get())
    N.delete(0, END)
    K.delete(0,END)
    dialogBox.delete(1.0, END)

# Starts game based on N and K values
def startGame(nodeQuantity):
    if nodeQuantity <= 1 or nodeQuantity >= 12: # Checks if N value is valid
        raise invalid_NK()
    if K_entry.get() < 1: # Checks if K value is valid
        raise invalid_NK()
    dialogBox.insert(END, f'Game Started. N = {N_entry.get()} K = {K_entry.get()}\n')
    for i in range(0, nodeQuantity): # Creates node icons
        cll.append(i)
        Button(root, text=str(i)).grid(row=3,column=i+3, padx=3, pady=1) 

# Removes node icon
def removeNode(deadNode):
    for node in root.grid_slaves(): 
            if int(node.grid_info()["column"]) == deadNode + 3:
                node.grid_forget()

# Eliminates random node from circular linked list
def elimination(safeNum): 
    cllArr = cll.makeArray() # Creates array
    if safeNum in cllArr: 
        cllArr.remove(safeNum) # Removes K value from the array
    deadNode = random.choice(cllArr) # Randomly chooses a number in the array 
    if deadNode == safeNum:
        elimination(safeNum)
    elif deadNode not in cllArr:
        elimination(safeNum)
    else:
        removeNode(deadNode)
        cllArr.remove(deadNode) #Removes the randomly selected number) from the array
        cll.remove(deadNode) # Removes the player 
        if cllArr == []: # Game ends here
            messagebox.showinfo("Winner", f"Winner: Player {K_entry.get()}")
            newGame()
            

Label(root, text='N').grid(row=1,column=0) # N value label
N_entry = IntVar() 
N = Entry(root, textvariable=N_entry, width=5) # N value entry box
N.grid(row=1,column=1)
N.delete(0, END)

Label(root, text='K').grid(row=2,column=0) # K value label
K_entry = IntVar()
K = Entry(root, textvariable=K_entry, width=5) # K value entry box
K.grid(row=2,column=1)
K.delete(0,END)

start = Button(root, text='Start',command=lambda: startGame(N_entry.get())).grid(row=4,column=0) # On click start game
eliminate = Button(root, text='Eliminate',command=lambda: elimination(K_entry.get())).grid(row=5,column=0) # On click eliminates a player and their icon

dialogBox = Text(root, height=11) # Creates a dialog box for displaying game events
dialogBox.place(x=0,y=130)

cll = CircularLinkedList() 

root.mainloop()