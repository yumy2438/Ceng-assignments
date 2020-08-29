#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include "Playlist.hpp"
#include "MyStack.hpp"
using namespace std;

template <class T>
LinkedList<T>* initialize_linked_list(vector<T> &v)
{
    LinkedList<T> *ll = new LinkedList<T>();
    Node<T> *currentNode = NULL;
    for (T item: v)
    {
        ll->insertNode(currentNode,item);
        currentNode = ll->getTail();
    }
    return ll;
}

template <class T>
bool compare(const LinkedList<T>* ll, vector<T> &v)
{
    Node<T> *currentNode = ll->getHead();
    int ari = 0;
    while (currentNode != NULL)
    {
        if (currentNode->getData() != v[ari])
            return false;
        currentNode = currentNode->getNext();
        ari+=1;
    }
    return true;
}

template <class T>
void test_insertion_linked_list(LinkedList<T>* ll,vector<T> &v)
{
    Node<T>* current = ll->getHead();
    //insertion at the beginning:
    ll->insertNode(NULL,0);
    typename std::vector<T>::iterator it;
    it = v.begin();
    v.insert(it,0);
    //insertion at the end:
    ll->insertNode(ll->getTail(),11);
    v.push_back(11);
    //insertion at the middle:
    ll->insertNode(ll->findPrev(5),-8);
    ll->insertNode(ll->findPrev(9),-11);
    it = v.begin();
    v.insert(it+5, -8);
    it = v.begin();
    v.insert(it+10, -11);
    if (compare(ll, v))
    {
        cout << "Insertion tests is successful." << endl;
    }
}
template <class T>
void test_deletion_linked_list(LinkedList<T>* ll, vector<T> &v)
{
    Node<T>* current = ll->getHead();
    ll->deleteNode(NULL);
    //delete from beginning:
    typename std::vector<T>::iterator it = v.begin();
    v.erase(it);
    //delete from the middle:
    ll->deleteNode(ll->findPrev(-8));
    ll->deleteNode(ll->findPrev(-11));
    it = v.begin();
    v.erase(it+4);
    v.erase(it+8);
    // delete from the end:
    ll->deleteNode(ll->findPrev(11));
    v.pop_back();
    if (compare(ll,v))
    {
        cout << "Deletion test is successful." << endl;
    }

}
template <class T>
void test_findPrev_linked_list(LinkedList<T>& ll, vector<T> &v)
{
    T prev = NULL;
    int ari = 0;
    for(T item: v)
    {
        Node<T> *tmp = ll.findPrev(item);
        if (tmp == NULL)
        {

        }
        else
        {
            if (prev != tmp->getData())
            {
                cout << prev << " " << tmp->getData() << endl;
                cout << "Unsuccessful findPrev" << endl;
                return;
            }
        }
        prev = v[ari];
        ari+=1;
    }
    cout << "Succesful findPrev" << endl;
}


template <class T>
void test_findNode_linked_list(LinkedList<T>& ll, vector<T> &v)
{
    for(T item: v)
    {
        Node<T> *tmp = ll.findNode(item);
        if (tmp == NULL)
        {
            cout << "Unsuccessful findNode" << endl;
            return;
        }
        else
        {
            if (item != tmp->getData())
            {
                cout << "Unsuccessful findNode" << endl;
                return;
            }
        }
    }
    cout << "Succesful findNode" << endl;
}


template <class T>
void test_copycons_assignment_linked_list(LinkedList<T>& ll, vector<T> &v)
{
    LinkedList<T> tmp = ll;
    if (compare(&tmp,v))
    {
        cout << "Successful copy cons" << endl;
    }
}
template <class T>
void print_v(vector<T> &v)
{
    typename vector<T>::iterator it;
    for(it=v.begin(); it != v.end(); ++it)
    {
        cout << *it;
    }
    cout << endl;
}


template <class T>
MyStack<T>* initialize_stack(vector<T> &v)
{
    MyStack<T> *st = new MyStack<T>();
    for(T item: v)
    {
        st->push(item);
    }
    return st;
}
template <class T>
bool compare(const MyStack<T>* mys, vector<T> &v)
{
    typename vector<T>::iterator it = v.end()-1;
    Node<T> *current = mys->Top();
    for(;it!=v.begin();--it)
    {
        if (current != NULL)
        {
            if (current->getData() != *it)
            {
                return false;
            }
            current = current->getNext();
        }
        else
        {
            if (v.size() != 0)
                return false;
        }
    }
    return true;
}


template <class T>
void test_pop(MyStack<T>* mys,int stackSize)
{
    while(stackSize>0)
    {
        mys->pop();
        stackSize--;
    }
    if (mys->isEmpty() == true)
    {
        cout << "pop and isempty is successful.";
    }
    else
    {
        cout << "unsuccessful pop and isempty operation.";
    }
}

int main()
{
    //  ---   LINKED LIST TESTER   ---
    vector<int> vect{1,2,3,4,5,6,7,8,9,10};
    LinkedList<int> *ll = initialize_linked_list(vect);
    cout << "1" << endl;
    test_insertion_linked_list(ll, vect);
    test_deletion_linked_list(ll,vect);
    test_findPrev_linked_list(*ll,vect);
    ll->print();
    print_v(vect);
    test_findNode_linked_list(*ll,vect);
    test_copycons_assignment_linked_list(*ll,vect);

    //  --- STACK TESTER ---
    cout << "STACK TESTER" << endl;
    print_v(vect);
    MyStack<int> *myStack = initialize_stack(vect);
    cout << compare(myStack,vect) << endl;
    test_pop(myStack,vect.size());


    //  --- PLAYLIST TESTER ---
    Playlist *pl = new Playlist();
    pl->load("file.txt");
    pl->print();
    cout <<"--------------------------"<<endl;
    pl->deleteEntry("Rihanna Talk That Talk");//delete head
    pl->deleteEntry("Rihanna Umbrella");//delete tail
    pl->deleteEntry("Billie Jean");//delete from middle
    pl->print();
    cout <<"--------------------------"<<endl;
    pl->insertEntry(Entry("Rihanna Talk That Talk"));
    pl->insertEntry(Entry("Rihanna Umbrella"));
    pl->insertEntry(Entry("Billie Jean"));
    pl->print();
    cout <<"--------------------------"<<endl;
    pl->reverse();
    pl->print();
    cout <<"--------------------------"<<endl;
    pl->sort();
    pl->print();
    cout <<"--------------------------"<<endl;
    cout<<"history!!"<<endl;
    pl->printHistory();
    cout<<"history!!"<<endl;
    pl->undo();
    pl->print();
    pl->printHistory();
    cout <<"--------------------------"<<endl;
    pl->undo();
    pl->print();
    pl->printHistory();
    cout <<"--------------------------"<<endl;

    pl->moveLeft("Whitney Houston I Wanna Dance with Somebody");
    pl->moveLeft("Hooverphonic The Night Before");
    pl->print();
    pl->moveRight("Whitney Houston I Wanna Dance with Somebody");
    pl->moveRight("{Nocturne in F major");
    pl->print();
    pl->shuffle();
    pl->print();
    pl->printHistory();

    Playlist *pl2 = new Playlist();
    pl2->load("file.txt");
    cout<<"--------------------------PL2-------------------------"<<endl;
    pl2->sort();
    pl2->print();
    cout<<"------------------------------------------------------------------\n-----------------------------------------"<<endl;
    pl->sort();
    cout<<"--------------------------PL1--------------------------"<<endl;
    pl->print();
    pl->merge(*pl2);
    cout<<"-------------------------"<<endl;
    pl->print();

}
