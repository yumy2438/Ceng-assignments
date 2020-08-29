
#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include "Playlist.hpp"
#include "Entry.hpp"

using namespace std;

Playlist::Playlist()
{
    srand(15);
}

int Playlist::getRandomNumber(int i, int n) const
{
    int range=n-i;
    int random = rand() % range + i;
    return random;
}

void Playlist::print()
{
    cout << "[PLAYLIST SIZE=" << entries.getSize() <<"]";
    entries.print();
}
void Playlist::printHistory()
{
    cout<<"[HISTORY]";
    history.print();
}

/* TO-DO: method implementations below */

/*load the list of playlist entries from the given file.*/
void Playlist::load(std::string fileName)
{
    ifstream infile(fileName);
    string line;
    while(std::getline(infile,line))
    {
        string title,genre,year;
        int c = 0;
        char st = line[c];
        string temp;
        int length = line.length();
        for(int tgy=0;tgy<3;tgy++)//titlegenreyear
        {
            while(st!=';' && c != length)
            {
                temp.push_back(st);
                c++;
                st = line[c];
            }
            c++;
            st = line[c];
            if(tgy==0) title = temp;
            else if(tgy==1) genre = temp;
            else year = temp;
            temp = "";
        }
        Entry newEntry(title,genre,year);
        insertEntry(newEntry);
    }
}
/*Inserts a new entry to the end of playlist entries.
 *For UNDO operation, you should save the insert operation.*/
void Playlist::insertEntry(const Entry &e)
{
    this->entries.insertNode(this->entries.getTail(),e);
    HistoryRecord newRecord(INSERT,e);
    this->history.push(newRecord);
}
/*Deletes the entry with given title from the list.
 *If the delete operation is successful (i.e. the entry with given title is in the playlist and deleted successfully)..
 *you should save the this  operation for UNDO operation.*/
void Playlist::deleteEntry(const std::string &_title)
{
    Entry newEntry(_title);
    Node<Entry> *delNode = this->entries.findPrev(newEntry);
    HistoryRecord newRecord(DELETE, entries.findNode(newEntry)->getData());
    history.push(newRecord);
    entries.deleteNode(delNode);
}
/*Moves the entry with given title to the left.*/
void Playlist::moveLeft(const std::string &title)
{
    //NULL DURUMLARA BAKMAMISSIIIN!!!
    Entry newEntry(title);
    Node<Entry> *moving = this->entries.findNode(newEntry);
    Node<Entry> *beforeMoving = this->entries.findPrev(newEntry);
    if (beforeMoving == NULL || moving == NULL)
    {
        return;//handling leftmost.and no entry with the given title.
    }
    Entry beforeEntry = beforeMoving->getData();
    Node<Entry> *beforeBeforeMoving = this->entries.findPrev(beforeEntry);
    beforeMoving->setNext(moving->getNext());
    moving->setNext(beforeMoving);
    if (beforeBeforeMoving == NULL)
    {
        entries.setHead(moving);
    }
    else
    {
        beforeBeforeMoving->setNext(moving);
    }
    if(beforeMoving->getNext() == NULL)
    {
        this->entries.setTail(beforeMoving);
    }
}
/*Moves the entry with given title to the right.*/
void Playlist::moveRight(const std::string &title)
{
    Entry newEntry(title);
    Node<Entry> *moving = this->entries.findNode(newEntry);
    if(moving == NULL) return;//no entry exists.
    Node<Entry> *afterMoving = moving->getNext();
    if(afterMoving == NULL) return; //rightmost
    Node<Entry> *beforeMoving = this->entries.findPrev(newEntry);
    //before movingim null olabilir!!
    moving->setNext(afterMoving->getNext());
    afterMoving->setNext(moving);
    if(beforeMoving == NULL)
    {
        entries.setHead(afterMoving);
    }
    else
    {
        beforeMoving->setNext((afterMoving));
    }
    if(moving->getNext() == NULL ) entries.setTail(moving);
}
/*Reverse the playlist entries.*/
void Playlist::reverse()
{
    MyStack<Entry> stackentries;
    Node<Entry> *currentNode = entries.getHead();
    while(currentNode != NULL)
    {
        stackentries.push(currentNode->getData());
        currentNode=currentNode->getNext();
    }
    entries.clear();
    Node<Entry> *prev = NULL;
    while(!stackentries.isEmpty())
    {
        Entry newEntry = stackentries.Top()->getData();
        entries.insertNode(prev,newEntry);
        stackentries.pop();
        prev = entries.getTail();
    }
    HistoryRecord newHistoryRecord(REVERSE);
    history.push(newHistoryRecord);

}
/*Sort the entries of the playlist from lowest to highest according to their “title”s.*/

// I assumed that current always comes before from minimum! and minimum cannot be NULL.
void Playlist::swap(Node<Entry> *currentBefore, Node<Entry> *minBefore)
{
    Node<Entry> *current;
    if(currentBefore==NULL) current = entries.getHead();
    else current = currentBefore->getNext();
    Node<Entry> *minimum = minBefore->getNext();
    if(current == minBefore)//adjoining
    {
        current->setNext(minimum->getNext());
        minimum->setNext(current);
        if(currentBefore == NULL)//current is head.
        {
            entries.setHead(minimum);
        }
        else
        {
            currentBefore->setNext(minimum);
        }
    }
    else if(current->getNext() == minBefore)// there is one node between them.
    {
        current->setNext(minimum->getNext());
        minBefore->setNext(current);
        minimum->setNext(minBefore);
        if(currentBefore == NULL)
        {
            entries.setHead(minimum);
        }
        else
        {
            currentBefore->setNext(minimum);
        }
    }
    else//they are in separate places
    {
        // x  x  cb  c  x  x  minbef  min  x  x
        Node<Entry> *currentNext = current->getNext();
        current->setNext(minimum->getNext());
        minBefore->setNext(current);
        minimum->setNext(currentNext);
        if(currentBefore == NULL)
        {
            entries.setHead(minimum);
        }
        else
        {
            currentBefore->setNext(minimum);
        }
    }
    if(current->getNext() == NULL) entries.setTail(current);

}

void Playlist::sort()
{
    Node<Entry> *currentNode = entries.getHead();
    int currentNo = 1;
    while(currentNode!=NULL)
    {
        Node<Entry> *innerNode = currentNode->getNext();
        Node<Entry> *minimum = currentNode;
        while(innerNode != NULL)
        {
            Entry minEntry = minimum->getData();
            string minTitle = minEntry.getTitle();
            Entry innerEntry = innerNode->getData();
            string innerTitle = innerEntry.getTitle();
            if(minTitle.compare(innerTitle)>0)
            {
                minimum = innerNode;
            }

            innerNode = innerNode->getNext();
        }
        //swap
        if(minimum != currentNode) swap(entries.findPrev(currentNode->getData()),entries.findPrev(minimum->getData()));
        currentNode = getNstElement(currentNo);
        currentNo++;
    }
}
/*Merge the sorted lists while keeping the sort order*/
void Playlist::merge(const Playlist & pl)
{
    Node<Entry> *headpl = pl.entries.getHead();
    Node<Entry> *headcur = entries.getHead();
    while(headpl != NULL && headcur != NULL)
    {
        Entry plEntry = headpl->getData();
        Entry curEntry = headcur->getData();
        string plTitle = plEntry.getTitle();
        string curTitle = curEntry.getTitle();
        int compareResult = plTitle.compare(curTitle);
        if(compareResult<0)
        {
            entries.insertNode(entries.findPrev(curEntry),plEntry);
            headpl = headpl->getNext();

        }
        else if(compareResult == 0)
        {
            headcur = headcur->getNext();
            headpl = headpl->getNext();
        }
        else
        {
            headcur = headcur -> getNext();
        }
    }
    while(headpl != NULL)
    {
        entries.insertNode(entries.getTail(),headpl->getData());
        headpl = headpl->getNext();
    }
}

Node<Entry>* Playlist::getNstElement(int n)
{
    if(n<0) return NULL;
    Node<Entry> *current = entries.getHead();
    int cur = 0;
    while(current!=NULL)
    {
        if(cur == n) return current;
        cur++;
        current = current->getNext();
    }
    return NULL;
}
/*Shuffle the playlist entries. Use getRandomNumber function to generate a random number. */
void Playlist::shuffle()
{
    int length = entries.getSize();
    int boundary = length-2;
    int currentNo = 0;
    while(currentNo<boundary)
    {
        int random = getRandomNumber(currentNo,length);
        if(currentNo<random)
        {
            swap(getNstElement(currentNo-1),getNstElement(random-1));
        }
        else if(currentNo>random)
        {
            swap(getNstElement(random-1),getNstElement(currentNo-1));
        }
        currentNo++;
    }
}
/*UNDO the the operations*/
void Playlist::undo()
{
    if(history.Top() == NULL) return;
    HistoryRecord top = history.Top()->getData();
    Operation oper = top.getOperation();
    Entry entry = top.getEntry();
    if(oper == INSERT)
    {
        cout<<"insert undo"<<entry<<endl;
        deleteEntry(entry.getTitle());
    }
    else if(oper == DELETE)
    {
        cout<<"delete undo"<<entry<<endl;
        insertEntry(entry);
    }
    else//reverse
    {
        reverse();
    }
    //i should pop twice, since the functions I called(delete,insert,reverse) adds history entries again.
    history.pop();
    history.pop();
}
