#ifndef MYSTACK_HPP
#define MYSTACK_HPP
#include "Node.hpp"

/*You are free to add private/public members inside this template..*/
template <class T>
class MyStack{
    private:
    Node<T> *top;
    public:
    /*Default constructor*/
    MyStack();
    /*copy constructor*/
    MyStack(const MyStack<T>& rhs);
    /*destructor*/
    ~MyStack();
    /*overloaded = operator*/
    MyStack<T>& operator=(const MyStack<T>& rhs);
    /*returns true if stack is empty*/
    bool isEmpty() const;
    /*push newItem to stack*/
    void push(const T& newItem);
    /*pop item from stack*/
    void pop();
    /*return top item of the stack*/
    Node<T>* Top() const;
	/*Prints the stack entries. This method was already implemented. Do not modify.*/
    void print() const;
};

template <class T>
void MyStack<T>::print() const{
    const Node<T>* node = top;
    while (node) {
        std::cout << node->getData();
        node = node->getNext();
    }
    cout<<std::endl;
}
/* TO-DO: method implementations below */
template <class T>
MyStack<T>::MyStack()
{
    top = NULL;
}

/*copy constructor*/
template <class T>
MyStack<T>::MyStack(const MyStack<T>& rhs)
{
    this->top = NULL;
    *this = rhs;
}

/*destructor*/
template <class T>
MyStack<T>::~MyStack()
{
    while(!isEmpty()) pop();
}

/*overloaded = operator*/
template <class T>
MyStack<T>& MyStack<T>::operator=(const MyStack<T>& rhs)
{
    if(this!=&rhs)
    {
        while(!isEmpty()) pop();
        if(!rhs->Top())
            top = NULL;
        else
        {
            top = new Node<T>(rhs->Top()->getData());
            Node<T> *before = top;
            Node<T> *current = rhs->Top()->getNext();
            while(current != NULL)
            {
                Node<T> *newNode(current->getData());
                before->setNext(newNode);
                before = before->getNext();
                current = current->getNext();
            }
            before->setNext(NULL);
        }
    }
    return *this;
}

/*returns true if stack is empty*/
template <class T>
bool MyStack<T>::isEmpty() const
{
    return top == NULL;
}

/*push newItem to stack*/
template <class T>
void MyStack<T>::push(const T& newItem)
{
    Node<T> *newNode = new Node<T>(newItem);
    newNode->setNext(top);
    top = newNode;
}


/*pop item from stack*/
template <class T>
void MyStack<T>::pop()
{
    if(!isEmpty())
    {
        Node<T> *tmp = top;
        top = top->getNext();
        delete tmp;
    }
}

/*return top item of the stack*/
template <class T>
Node<T>* MyStack<T>::Top() const
{
    return top;
}




#endif
