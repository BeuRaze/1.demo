#include <stdio.h>

int factorial(int n){
     int i;
     int m = 1;
    for(i=1; i<=n; i++){
        m = m*i;

        
    }
    printf("Factorial of %d is %d\n", n, m);

}

int main(){
int n = 5;
factorial(n);
return 0;



}