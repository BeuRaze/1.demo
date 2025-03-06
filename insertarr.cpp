#include <iostream>
using namespace std;


struct Array{
    int *A;
    int size;
    int length;
};

int main()
{
    struct Array arr;
    cout<<"Enter the size of the array:"<<endl;
    cin>>arr.size;
    arr.A= new int[arr.size];
    arr.length = 0;
    int n;
    cout<<"Enter the number of elements:"<<endl;
    cin>>n;
    cout<<"Enter the elements:"<<endl;
    for (int i = 0; i<n; i++){
       cin>>arr.A[i];
    }
    
    return 0;
}