#ifndef STRING_HELPERS_H
#define STRING_HELPERS_H

#include <string>
#include <algorithm>
#include <cctype>

namespace StringHelpers {

    inline void ltrim(std::string &s) {
        s.erase(s.begin(), std::find_if(s.begin(), s.end(), [](unsigned char ch) {
            return !std::isspace(ch);
        }));
    }

    inline void rtrim(std::string &s) {
        s.erase(std::find_if(s.rbegin(), s.rend(), [](unsigned char ch) {
            return !std::isspace(ch);
        }).base(), s.end());
    }

    inline void trim(std::string &s) {
        ltrim(s);
        rtrim(s);
    }

    inline std::string ltrim_copy(std::string s) {
        ltrim(s);
        return s;
    }

    inline std::string rtrim_copy(std::string s) {
        rtrim(s);
        return s;
    }


    inline std::string trim_copy(std::string s) {
        trim(s);
        return s;
    }

} 

#endif // STRING_HELPERS_H
