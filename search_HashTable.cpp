#include <iostream>
#include <fstream>
#include <string>
#include <regex>
#include <vector>
#include <algorithm>
#include <ctime>

using namespace std;

class Node {
public:
    int value;
    string filename;
    Node(int value = 0, string filename = "") {
        this->value = value;
        this->filename = filename;
    }
};

class HashTable {
private:  
    static const int SIZE = 10000;
    vector<vector<Node>> dataTable;

public:
    HashTable(){
        for(int i{0}; i < SIZE; i++)
            dataTable.push_back({});
    }

    int hashfunc(string key) {
        smatch m; 
        if(regex_search(key, m, regex("\\d+")))
            return stoi(m[0]) % SIZE;
        return 0; 
    }
    
    void addElement(const string& filename) {
        int index = hashfunc(filename);
        bool found = false;

        for (auto& element : dataTable[index]) {
            if (element.filename == filename) {
                element.value++;
                found = true;
                break;
            }
        }

        if (!found) {
            Node newNode(1, filename);
            dataTable[index].emplace_back(newNode);
        }
    }
    
    void heapify(vector<Node>& a, int n, int i) {
        int smallest = i;
        int left = 2 * i + 1;
        int right = 2 * i + 2;
        if (left < n && a[left].value < a[smallest].value)
            smallest = left;
        if (right < n && a[right].value < a[smallest].value)
            smallest = right;
        if (smallest != i) {
            swap(a[i], a[smallest]);
            heapify(a, n, smallest);
        }
    }

    void heapSort(vector<Node>& a, int n) {
        for (int i = n / 2 - 1; i >= 0; i--)
            heapify(a, n, i);

        for (int i = n - 1; i >= 0; i--) {
            swap(a[0], a[i]);
            heapify(a, i, 0);
        }
    }
    
    void sort(){
        int length = dataTable.size();
        vector<Node> v;
        int a = 0;
        int j = 0;
        while (a != length) {
            int l = dataTable[a].size() - 1;
            if (j <= l) {
                v.push_back(dataTable[a][j]);
                j++;
            } else {
                j = 0;
                a++;
            }
        }
        heapSort(v, v.size());

        int count = 0;
        for (auto x : v){
            if(count < 10)
                cout << x.filename << ": " << x.value << endl;
            count++;
        }
    }
};

int main() {
    clock_t start;
    ifstream in_file("test.txt");
    
    if (!in_file) {
        cout << "Problem opening file." << endl;
        return 1;
    }

    string line;
    smatch m;
    HashTable* hashSearch = new HashTable();

    start = clock();

    int count = 0;
    while (count != 800'000 && getline(in_file, line)) {
        if (regex_search(line, m, regex("\\w+\\.[a-z]+"))){
            hashSearch->addElement(m[0]);
        }
        count++;
    }
    float hashTime = (clock() - start) / (float) CLOCKS_PER_SEC;

    hashSearch->sort();
    float sortTime = ((clock() - start) / (float) CLOCKS_PER_SEC) - hashTime;

    cout << endl;
    float duration = (clock() - start) / (float) CLOCKS_PER_SEC;

    cout << "Time for hashing: " << hashTime << " seconds" << endl;
    cout << "Time for sorting: " << sortTime << " seconds" << endl;
    cout << "TOTAL TIME: " << duration << " seconds" << endl;
    
    in_file.close();
    return 0;
}