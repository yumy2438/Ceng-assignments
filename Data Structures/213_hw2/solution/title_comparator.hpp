#ifndef _title_h__
#define _title_h__

#include "book.hpp"
#include <cstring>

class TitleComparator
{
    public:
    bool operator( ) (const Book::SecondaryKey & key1,
                      const Book::SecondaryKey & key2) const
    {
        std::string t1 = key1.getTitle();
        std::string t2 = key2.getTitle();
        int i;
        for(i=0;i<t1.length();i++) t1[i] = tolower(t1[i]);
        for(i=0;i<t2.length();i++) t2[i] = tolower(t2[i]);
        if(t1<t2) return true;
        if(t1 == t2)
        {
            std::string a1 = key1.getAuthor();
            std::string a2 = key2.getAuthor();
            for(i=0;i<a1.length();i++) a1[i] = tolower(a1[i]);
            for(i=0;i<a2.length();i++) a2[i] = tolower(a2[i]);
            if(a1<a2) return true;
        }
        return false;
    }
};

#endif
