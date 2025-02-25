#include <iostream>
#include <cmath>

using namespace std;

int eex(int x, int n){
   static int p = 1, f = 1;
    int r;
    if(n==0){
        return 1;
    }
else {}
    r = eex(x, n-1);
    p = p*x;
    f = f*n;
    return r + p/f;

}

int main(){
    int x = 8;
    int n = 20;
    cout << eex(x, n) << endl;
    
}