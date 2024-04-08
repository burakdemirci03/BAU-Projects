#include <iostream>
#include <fstream>
#include <string>
#include <regex>
#include <vector>
#include <algorithm>
#include <ctime>
#include <unordered_map>

using namespace std;

void addElement(const string& filename, unordered_map<string, int>& dataMap){
    auto it = dataMap.find(filename);
    if (it != dataMap.end()) {
        it->second++;
    }
    else {
        dataMap.insert({filename, 1});
    }
}

void MapToVec(const unordered_map<string, int>& dataMap, vector<unordered_map<string, int>>& vect) {
    for (const auto& mapped : dataMap) {
        vect.push_back({{mapped.first, mapped.second}});
    }
}

bool compareMaps(const unordered_map<string, int>& dataMap1, const unordered_map<string, int>& dataMap2) {
    return dataMap1.begin()->second > dataMap2.begin()->second;
}


int main() {
    cout<<endl;
    unordered_map<string, int> mapSearch;
    clock_t start;
    ifstream in_file("test.txt");
    
    if (!in_file) {
        cout << "Problem opening file." << endl;
        return 1;
    }

    string line;
    smatch m;

    start = clock();
    int count = 0;
    while (count != 800'000 && getline(in_file, line)) {
        if (regex_search(line, m, regex("\\w+\\.[a-z]+"))) {
            addElement(m[0], mapSearch);
        }
        count++;
    }
    float mapTime = (clock() - start) / (float) CLOCKS_PER_SEC;

    vector<unordered_map<string, int>> vect;
    MapToVec(mapSearch, vect);

    sort(vect.begin(), vect.end(), compareMaps);

    float sortTime = ((clock() - start) / (float) CLOCKS_PER_SEC) - mapTime;

    for (int i = 0; i < 10; ++i) {
        for (const auto& entry : vect[i]) {
            cout << entry.first << ": " << entry.second << endl;
        }
    }
    cout << endl;
    float duration = (clock() - start) / (float) CLOCKS_PER_SEC;

    cout << "Time for mapping: " << mapTime << " seconds" << endl;
    cout << "Time for sorting: " << sortTime << " seconds" << endl;
    cout << "TOTAL TIME: " << duration << " seconds" << endl;

    in_file.close();
    return 0;
}