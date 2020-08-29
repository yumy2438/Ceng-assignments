#include "bookstore.hpp"

BookStore::BookStore( ) //implemented, do not change
{
}

void
BookStore::insert(const Book & book)
{
    primaryIndex.insert(book.getISBN(),book);
    BSTP::Iterator book_it = primaryIndex.find(book.getISBN());
    const Book *b1 = &(*(book_it));
    SKey skbook(book);
    secondaryIndex.insert(skbook, b1);//AUTHOR
    Book *b2 = &(*(book_it));
    ternaryIndex.insert(skbook, b2);//TITLE
}

void
BookStore::remove(const std::string & isbn)
{
    BSTP::Iterator book_it = primaryIndex.find(isbn);
    if (&(*book_it))
    {
        SKey skbook(*book_it);
        secondaryIndex.remove(skbook);
        ternaryIndex.remove(skbook);
        primaryIndex.remove(isbn);
    }
}

void
BookStore::remove(const std::string & title,
                  const std::string & author)
{
    SKey key(title,author);
    BSTT::Iterator book_it = ternaryIndex.find(key);
    Book *b2 = *(book_it);
    if(b2)
    {
        secondaryIndex.remove(key);
        ternaryIndex.remove(key);
        primaryIndex.remove(b2->getISBN());
    }

}

void
BookStore::removeAllBooksWithTitle(const std::string & title)
{
    std::list<BSTT::Iterator> lst = ternaryIndex.find(SKey(title,"a"),SKey(title,"z"));
    std::list<BSTT::Iterator>::const_iterator it;
    for(it = lst.begin(); it != lst.end(); ++it)
    {
        Book *b = (*(*it));
        const std::string isbn = b->getISBN();
        remove(isbn);
    }

}

void
BookStore::makeAvailable(const std::string & isbn)
{
    BSTP::Iterator book_it = primaryIndex.find(isbn);
    if(&(*book_it))
    {
        Book b = (*book_it);
        b.setAvailable();
    }
}

void
BookStore::makeUnavailable(const std::string & title,
                           const std::string & author)
{
    BSTT::Iterator book_it = ternaryIndex.find(SKey(title,author));
    if(&(*book_it))
    {
        Book *b = *(&(*book_it));
        b->setUnavailable();
    }
}

void
BookStore::updatePublisher(const std::string & author,
                           const std::string & publisher)
{
    std::list<BSTS::Iterator> lst = secondaryIndex.find(SKey("a",author),SKey("{",author));
    std::list<BSTS::Iterator>::const_iterator it;
    for(it = lst.begin(); it != lst.end(); ++it)
    {
        const Book *b = (*(*it));
        BSTT::Iterator book_it = ternaryIndex.find(SKey(b->getTitle(),b->getAuthor()));
        Book *b2 = *(book_it);
        b2->setPublisher(publisher);
    }
}

void
BookStore::printBooksWithISBN(const std::string & isbn1,
                              const std::string & isbn2,
                              unsigned short since) const
{
    std::list<BSTP::Iterator> lst = primaryIndex.find(isbn1,isbn2);
    std::list<BSTP::Iterator>::const_iterator it;
    for (it = lst.begin(); it != lst.end(); ++it)
    {
        if ((*(*it)).getYear() >= since)
        {
            std::cout << *(*it) << std::endl;
        }

    }
}

void
BookStore::printBooksOfAuthor(const std::string & author,
                              const std::string & first,
                              const std::string & last) const
{
    std::list<BSTT::Iterator> lst = ternaryIndex.find(SKey(first,""),SKey(last,""));
    std::list<BSTT::Iterator>::const_iterator it;
    for(it = lst.begin(); it != lst.end(); ++it)
    {
        Book *b = *(*it);
        std::string getAuthor = b->getAuthor();
        std::string author_lower = "";
        for(int i=0;i<getAuthor.length();i++) getAuthor[i] = tolower(getAuthor[i]);
        for(int i=0;i<author.length();i++) author_lower += tolower(author[i]);
        if (getAuthor == author_lower)
            std::cout << *(*(*it)) << std::endl;
    }
}

void //implemented, do not change
BookStore::printPrimarySorted( ) const
{
    BSTP::Iterator it;

    for (it=primaryIndex.begin(); it != primaryIndex.end(); ++it)
    {
        std::cout << *it << std::endl;
    }
}

void //implemented, do not change
BookStore::printSecondarySorted( ) const
{
    BSTS::Iterator it;

    for (it = secondaryIndex.begin(); it != secondaryIndex.end(); ++it)
    {
        std::cout << *(*it) << std::endl;
    }
}

void //implemented, do not change
BookStore::printTernarySorted( ) const
{
    BSTT::Iterator it;

    for (it = ternaryIndex.begin(); it != ternaryIndex.end(); ++it)
    {
        std::cout << *(*it) << std::endl;
    }
}


