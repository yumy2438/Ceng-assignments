#include "Article.h"
using namespace std;
/*#############################
#               NOTE!         #
#    Please don't forget to   #
#     check PDF. Fuctions     #
#    may have more detailed   #
#     tasks which are not     #
#       mentioned here.       #
#############################*/

Article::Article( int table_size,int h1_param, int h2_param )
{
    /*#############################
    #            TO-DO            #
    # Write a default constructor #
    #   for the Article Class     #
    #############################*/
    this->h1_param = h1_param;
    this->h2_param = h2_param;
    this->table_size = table_size;
    this->table = new pair<std::string,int>[table_size];
    this->n = 0;
    for(int i=0;i<table_size;i++)
    {
        this->table[i] = make_pair(EMPTY_KEY,EMPTY_INDEX);
    }
}

Article::~Article()
{
    /*#############################
    #             TO-DO           #
    #  Write a deconstructor for  #
    #     the Article Class       #
    #############################*/
    delete [] table;
    table = NULL;
}

int Article::get( std::string key, int nth, std::vector<int> &path ) const
{
    /*#############################################
    #                    TO-DO                    #
    #      Your get function should return        #
    # the original index (index in the text file) #
    #    of the nth 'key' in the hash table.      #
    #    If there is no such a key, return -1     #
    #    If there is, return the original index   #
    #     In both cases, you need to push each    #
    #          visited index while probing        #
    #           that you calculated until         #
    #      finding the key, to the path vector.   #
    #############################################*/
    int tableIndex = 0, i = 0, n_control = 1;
    while(i<table_size)
    {
        tableIndex = hash_function(key,i);
        //cout<<"tableind:"<<tableIndex<<endl;
        if (i != 0) path.push_back(tableIndex);
        if(table[tableIndex].second == EMPTY_INDEX)
        {
            break;
        }
        if(table[tableIndex].first == key)
        {
            if(nth == 1 && n_control==1) return table[tableIndex].second;
            //add to the vector.
            if(nth==n_control)
            {
                return table[tableIndex].second;
            }
            n_control++;
        }
        i++;
    }
    return -1;
}

int Article::insert( std::string key, int original_index )
{
    /*#########################################
    #                 TO-DO                   #
    #      Insert the given key, with the     #
    # original index value (at the text file) #
    #           to the hash table.            #
    #  Return the total number of probes you  #
    #      encountered while inserting.       #
    #########################################*/
    int i = 0,probing_count = 0, probing_flag = true;
    if(getLoadFactor() > MAX_LOAD_FACTOR)
    {
        expand_table();
    }
    while(1)
    {
        int hashing_key = hash_function(key,i);
        if(table[hashing_key].first == EMPTY_KEY)
        {
            table[hashing_key] = make_pair(key,original_index);
            break;
        }
        else
        {
            if(table[hashing_key].first == key)
            {
                int index_already_added = table[hashing_key].second;
                if (index_already_added > original_index)
                {
                    //if key is not unique uncomment the comment ones.
                    //std::string added_key = table[hashing_key].first;
                    int added_index = table[hashing_key].second;
                    //table[hashing_key].first = key;
                    table[hashing_key].second = original_index;
                    //key = added_key;
                    original_index = added_index;
                    probing_flag = false;
                }
            }
            if (probing_flag) probing_count++;
        }
        i++;
    }
    n++;

    return probing_count;

}


int Article::remove( std::string key, int nth )
{
    /*#########################################
    #                  TO-DO                  #
    #      Remove the nth key at the hash     #
    #                  table.                 #
    #  Return the total number of probes you  #
    #      encountered while inserting.       #
    #   If there is no such a key, return -1  #
    #     If there, put a mark to the table   #
    #########################################*/
    int probing_count=0,i=0,n_control=1,finished_condition=false;
    while(1)
    {
        int hashing_key = hash_function(key,i);
        if(table[hashing_key].first == key)
        {
            if(n_control == nth)
            {
                table[hashing_key].first = EMPTY_KEY;
                table[hashing_key].second = MARKED_INDEX;
                n--;
                return probing_count;
            }
            n_control++;
        }
        probing_count++;
        if(i > table_size) finished_condition = true;
        if(finished_condition) break;
        i++;
    }
    return -1;

}

double Article::getLoadFactor() const
{
    /*#########################################
    #                TO-DO                    #
    #      Return the load factor of the      #
    #                table                    #
    #########################################*/
    return double(n)/double(table_size);
}

void Article::getAllWordsFromFile( std::string filepath )
{
    /*#########################################
    #                  TO-DO                  #
    #       Parse the words from the file     #
    #      word by word and insert them to    #
    #                hash table.              #
    #   For your own inputs, you can use the  #
    #  'inputify.py' script to fix them to    #
    #            the correct format.          #
    #########################################*/
    ifstream myfile(filepath);
    string line;
    int original_index = 1;
    string word;
    if (myfile.is_open())
    {
        while(getline(myfile,line))
        {
            word = "";
            for(char ch: line)
            {
                if(ch != ' ')
                {
                    word += ch;
                }
                else
                {
                    insert(word,original_index);
                    original_index++;
                    word = "";
                }

            }
        }
        insert(word,original_index);
        myfile.close();
    }
}

void Article::expand_table()
{
    /*#########################################
    #                  TO-DO                  #
    #   Implement the expand table function   #
    #   in order to increase the table size   #
    #   to the very first prime number after  #
    #      the value of (2*table size).       #
    #         Re-hash all the data.           #
    #       Update h2_param accordingly.      #
    #########################################*/
    int old_tablesize = table_size;
    table_size = nextPrimeAfter(2*old_tablesize);
    h2_param = firstPrimeBefore(table_size);
    std::pair<std::string, int>* old_table = this->table;
    table = new pair<std::string,int>[table_size];
    n = 0;
    for(int i = 0; i<table_size;i++) table[i] = make_pair(EMPTY_KEY,EMPTY_INDEX);
    for(int i = 0; i<old_tablesize; i++)
    {
        if(old_table[i].first != EMPTY_KEY) insert(old_table[i].first, old_table[i].second);
    }
    delete [] old_table;
}

int Article::hash_function( std::string& key, int i ) const
{
    /*#########################################
    #                TO-DO                    #
    #       Implement the main hashing        #
    #    function. Firstly, convert key to    #
    #    integer as stated in the homework    #
    #      text. Then implement the double    #
    #            hashing function.            #
    #      use convertStrToInt function to    #
    #      convert key to a integer for       #
    #         using it on h1 and h2           #
    #               reminder:                 #
    #            you should return            #
    #    ( h1(keyToInt) + i*h2(keyToint) )    #
    #            modulo table_size            #
    #########################################*/
    int key_int = convertStrToInt(key);
    int h1_val = h1(key_int);
    int h2_val = h2(key_int);
    return (h1_val+(i*h2_val))%table_size;
}


int Article::h1( int key ) const
{
    /*###############################
    #              TO-DO            #
    #      First Hash function      #
    # Don't forget to use h1_param. #
    ###############################*/
    int popcount = 0;
    while(key != 0)
    {
        if(key%2 == 1) popcount++;
        key = key/2;
    }
    return popcount*h1_param;

}

int Article::h2( int key ) const
{
    /*###############################
    #              TO-DO            #
    #     Second Hash function      #
    # Don't forget to use h2_param. #
    ###############################*/
    int modulo = key % h2_param;
    return h2_param-modulo;
}
