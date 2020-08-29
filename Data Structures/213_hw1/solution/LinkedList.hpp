#ifndef _LINKEDLIST_H_
#define _LINKEDLIST_H_

#include <iostream>
#include "Node.hpp"

using namespace std;

/*....DO NOT EDIT BELOW....*/
template <class T>
class LinkedList {
    private:
        Node<T>* head;
        Node<T>* tail;
        size_t  size;
    public:

        LinkedList();
        LinkedList(const LinkedList<T>& ll);
        LinkedList<T>& operator=(const LinkedList<T>& ll);
        ~LinkedList();

        /* Return head of the linked-list*/
        Node<T>* getHead() const;
        /* Set head of the linked-list*/
        void setHead(Node<T>* n);
        /* Return tail of the linked-list*/
        Node<T>* getTail() const;
        /* Set tail of the linked-list*/
        void setTail(Node<T>* n);
        /* Get the previous node of the node that contains the data item.
         * If the head node contains the data item, this method returns NULL.*/
        Node<T>* findPrev(const T& data) const;
        /* Get the node that stores the data item.
         * If data is not found in the list, this function returns NULL.*/
        Node<T>* findNode(const T& data) const;
        /* Insert a new node to store the data item.
         * The new node should be placed after the “prev” node.
         * If prev is NULL then insert new node to the head.*/
        void insertNode(Node<T>* prev, const T& data);
        /* This method is used to delete the node that is next to “prevNode”.
         * PS:prevNode is not the node to be deleted. */
        void deleteNode(Node<T>* prevNode);
        /* This method is used to clear the contents of the list.*/
        void clear();
        /* This method returns true if the list empty, otherwise returns false.*/
        bool isEmpty() const;
        /* This method returns the current size of the list. */
        size_t getSize() const;
        /*Prints the list. This method was already implemented. Do not modify.*/
        void print() const;//done
};

template <class T>
void LinkedList<T>::print() const{
    const Node<T>* node = head;
    while (node) {
        std::cout << node->getData();
        node = node->getNext();
    }
    cout<<std::endl;
}

/*....DO NOT EDIT ABOVE....*/

/* TO-DO: method implementations below */
template <class T>
LinkedList<T>::LinkedList()
{
    cout<<"cons"<<endl;
    head = NULL;
    tail = NULL;
    size = 0;
}
template <class T>
LinkedList<T>::LinkedList(const LinkedList<T>& ll)
{
    cout<<"copycons"<<endl;
    this->head = NULL;
    this->tail = NULL;
    this->size = 0;
    //call copy constructor
    cout<<"copy finished."<<endl;
    *this = ll;

}
template <class T>
LinkedList<T>& LinkedList<T>::operator=(const LinkedList<T>& ll)
{
    cout<<"operator="<<endl;
    if(this != &ll)//if they point the same place, no need to copy.
    {
        this->clear();
        head = new Node<T>(ll.getHead()->getData());//not like this, we need to create new ll->getHead();
        tail = new Node<T>(ll.getTail()->getData());
        size = ll.getSize();
        Node<T> *before = head;
        Node<T> *current = ll.getHead()->getNext();
        while(current != NULL)
        {
            Node<T> *temp = new Node<T>(current->getData());
            before->setNext(temp);
            before = before->getNext();
            current = current->getNext();
        }
        before->setNext(NULL);
    }
    return *this;
}
template <class T>
LinkedList<T>::~LinkedList()
{
    clear();
}

/* Return head of the linked-list*/
template <class T>
Node<T>* LinkedList<T>::getHead() const
{
    return head;
}

/* Set head of the linked-list*/
template <class T>
void LinkedList<T>::setHead(Node<T>* n)
{
    head = n;
}
/* Return tail of the linked-list*/
template <class T>
Node<T>* LinkedList<T>::getTail() const
{
    return tail;
}
/* Set tail of the linked-list*/
template <class T>
void LinkedList<T>::setTail(Node<T>* n)
{
    tail = n;
}
/* Get the previous node of the node that contains the data item.
 * If the head node contains the data item, this method returns NULL.*/
template <class T>
Node<T>* LinkedList<T>::findPrev(const T& data) const
{
    Node<T> *current = this->getHead();
    if (current == NULL)
            return NULL;
    if(current->getData() == data) return NULL;
    while(current->getNext()!=NULL)
    {
        if(current->getNext()->getData() == data)
            break;
        current = current->getNext();
    }
    return current;
}
/* Get the node that stores the data item.
 * If data is not found in the list, this function returns NULL.*/
template <class T>
Node<T>* LinkedList<T>::findNode(const T& data) const
{
    Node<T> *current = this->getHead();
    while(current!=NULL)
    {
        if(current->getData() == data)
            break;
        current = current->getNext();
    }
    return current;
}


/* Insert a new node to store the data item.
* The new node should be placed after the “prev” node.
* If prev is NULL then insert new node to the head.*/
template <class T>
void LinkedList<T>::insertNode(Node<T>* prev, const T& data)
{
    if(prev == NULL)
    {
        Node<T> *newNode = new Node<T>(data);
        newNode->setNext(head);
        head = newNode;
        if (tail == NULL)
        {
            tail = head;
        }
    }
    else
    {
        Node<T> *newNode = new Node<T>(data);
        if(prev == tail)
        {
            prev->setNext(newNode);
            tail = newNode;
        }
        else
        {
            newNode->setNext(prev->getNext());
            prev->setNext(newNode);
        }
    }
    size+=1;
}
/* This method is used to delete the node that is next to “prevNode”.
* PS:prevNode is not the node to be deleted. */
template <class T>
void LinkedList<T>::deleteNode(Node<T>* prevNode)
{
    if(prevNode == NULL)
    {
        //headi silcez
        Node<T> *temp = getHead();
        head = temp->getNext();
        if (head == NULL)//in case of head=tail
        {
            tail = NULL;
        }
        delete temp;
        size-=1;
        return;
    }
    if(prevNode->getNext() == tail)
    {
        tail = prevNode;
    }
    Node<T> *temp = prevNode->getNext();
    prevNode->setNext(temp->getNext());
    delete temp;
    size-=1;
}
/* This method is used to clear the contents of the list.*/
template <class T>
void LinkedList<T>::clear()
{
    if(isEmpty()) return;
    while(!isEmpty())
    {
        deleteNode(NULL);
    }
}
/* This method returns true if the list empty, otherwise returns false.*/
template <class T>
bool LinkedList<T>::isEmpty() const
{
    return head == NULL;
}
/* This method returns the current size of the list. */
template <class T>
size_t LinkedList<T>::getSize() const
{
    return this->size;
}




#endif
