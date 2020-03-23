#include <bits/stdc++.h>
#include <chrono>
using namespace std;

float summ(float n, int N){
    
    stack<float> s;
    stack<float> w;
    for(int i = 0; i < N; i++) s.push(n);

    while(true){
        if(s.size() == 1 and w.empty()) return s.top();
        if(w.size() == 1 and s.empty()) return w.top();
        
        float a;
        float b;

        while(s.size() > 1){
            a = s.top();
            s.pop();
            b = s.top();
            s.pop();
            w.push(a+b);
        }

        while(w.size() > 1){
            a = w.top();
            w.pop();
            b = w.top();
            w.pop();
            s.push(a+b);
        }
    }
}

void zad1(){
    float ans = 0.0;
    auto start = chrono::high_resolution_clock::now();
    for (int i = 0; i < 10000000; i++){
        ans += 0.012;
      //if(i % 25000 == 0) cout << abs((i+1)*0.012 - ans) / (i+1)*0.012 << endl;
    }
    auto stop = chrono::high_resolution_clock::now();
    auto duration = chrono::duration_cast<chrono::microseconds>(stop - start); 

    cout << ans << endl;
    cout << "wzgledny: " << abs(120000.0 - ans) / 120000.4 << endl; 
    cout << "bezwzgledny: " << abs(120000.0 - ans) << endl;
    cout << "czas: " << duration.count() << endl;

    start = chrono::high_resolution_clock::now();
    ans = summ(0.123123123, 10000000);
    stop = chrono::high_resolution_clock::now();
    duration = chrono::duration_cast<chrono::microseconds>(stop - start); 

    cout << ans << endl;
    cout << "wzgledny: " << abs(1231231.23 - ans) / 1231231.23  << endl; 
    cout << "bezwzgledny: " << abs(1231231.23- ans) << endl;
    cout << "czas: " << duration.count() << endl;
}

void zad2(){
    float sum = 0.0f;
    float err = 0.0f;
    int N = 10000000;
    auto start = chrono::high_resolution_clock::now();
    for(int i = 0; i < N; i++){
        float y = 0.012 - err;
        float tmp = sum + y;
        err = (tmp - sum) - y;
        sum = tmp;
    }
    auto stop = chrono::high_resolution_clock::now();
    auto duration = chrono::duration_cast<chrono::microseconds>(stop - start); 
    cout << sum << endl;
    cout << "wzgledny: " << abs(120000.0 - sum) / 120000.4 << endl; 
    cout << "bezwzgledny: " << abs(120000.0 - sum) << endl;
    cout << "czas: " << duration.count() << endl;
}

float riemann_float_forward(float s,int n){
    float sum = 0.0;
    for (int i = 1; i<=n;i++)
        sum += 1/(pow(i,s));
    return sum;
}

double riemann_double_forward(float s,int n){
    double sum = 0.0;
    for (int i = 1; i<=n;i++)
        sum += 1/(pow(i,s));
    return sum;
}

float riemann_float_backward(float s,int n){
    float sum = 0.0;
    for (int i = n; i>0;i--)
        sum += 1/(pow(i,s));
    return sum;
}

float riemann_double_backward(float s,int n){
    double sum = 0.0;
    for (int i = 1; i<=n;i++)
        sum += 1/(pow(i,s));
    return sum;
}

float dir_float_forward(float s,int n){
    float sum = 0.0;
    for(int i =1 ;i<n;i++)
        sum += pow(-1, i-1)*1/(pow(i, s));
    return sum;
}
float dir_double_forward(float s,int n){
    double sum = 0.0;
    for(int i =1 ;i<n;i++)
        sum += pow(-1, i-1)*1/(pow(i, s));
    return sum;
}
float dir_float_backward(float s,int n){
    float sum = 0.0;
    for(int i =n ;i>0;i--)
        sum += pow(-1, i-1)*1/(pow(i, s));
    return sum;
}
float dir_double_backward(float s,int n){
    float sum = 0.0;
    for(int i =1 ;i<n;i++)
        sum += pow(-1, i-1)*1/(pow(i, s));
    return sum;
}

void zad3(){

    float S[6] = {2,3,6667,5,7.2,10};
    int N[5] = {50,100,200,500,1000};

    cout << "Reimann \n";

    cout << "Forward: \n";
    for(auto x : S){
        for(auto y : N){
        cout << "Float(" << x << ", " << y << ": "<< riemann_float_forward(x, y)<< endl;
        cout << "Double(" << x << ", " << y << ": "<< riemann_double_forward(x, y)<< endl;
        cout << "wzgledny " << abs(riemann_float_forward(x, y)- riemann_double_forward(x, y)) << endl << endl;
        }
    }
    cout << "Backward: \n";
    for(auto x : S){
        for(auto y : N){
        cout << "Float(" << x << ", " << y << ": "<< riemann_float_backward(x, y)<< endl;
        cout << "Double(" << x << ", " << y << ": "<< riemann_double_backward(x, y)<< endl;
        cout << "wzgledny " << abs(riemann_float_backward(x, y)- riemann_double_backward(x, y)) << endl << endl;
        }
    }

    cout << "Dirichlet \n";

    cout << "Forward: \n";
    for(auto x : S){
        for(auto y : N){
        cout << "Float(" << x << ", " << y << ": "<< dir_float_forward(x, y)<< endl;
        cout << "Double(" << x << ", " << y << ": "<< dir_double_forward(x, y)<< endl;
        cout << "wzgledny " << abs(dir_float_forward(x, y)- dir_double_forward(x, y)) << endl << endl;
        }
    }

    cout << "Backward: \n";
    for(auto x : S){
        for(auto y : N){
        cout << "Float(" << x << ", " << y << ": "<< dir_float_backward(x, y)<< endl;
        cout << "Double(" << x << ", " << y << ": "<< dir_double_backward(x, y)<< endl;
        cout << "wzgledny " << abs(dir_float_backward(x, y)- dir_double_backward(x, y))<<endl << endl;
        }
    }
}

void zad4(float r){

    float X[1] = {0.5};
    float X_VAL[5][100];
    for(int j = 0; j< 1; j++){
        X_VAL[j][0] = X[j];
        for(int i = 0; i < 99; i++){
            X_VAL[j][i+1] = r*X_VAL[j][i]*(1-X_VAL[j][i]);
            //cout << r << " " <<  X_VAL[j][i+1] << "|";
            if( i % 10 == 0)
                cout << X_VAL[j][i+1] << endl;
        }
    }
    cout << endl;
}

void zad4(double r){

    double X[3] = {0.33, 0.5, 0.00005};
    double X_VAL[5][100];
    int counter = 0;
    for(int j = 0; j < 3; j++){
        X_VAL[j][0] = X[j];
        for(int i = 0; i < 99; i++){
            X_VAL[j][i+1] = r*X_VAL[j][i]*(1-X_VAL[j][i]);
            //cout << r << " " <<  X_VAL[j][i+1] << "|";
            //if( i % 10 == 0)
            //    cout << X_VAL[j][i+1] << endl;
        }
        counter = 0;
        float val = X[j];
        while(val != 0){
            counter++;
            val = r*val*(1-val);
        }
        cout << X[j] << " iteracje " << counter << endl;
    }
    
    cout << endl;
}

int main(){
    
    //int N = 1000000;
    //cout << "Zad1 \n";
    //zad1();
    //cout << "Zad2 \n";
    //zad2();
    //cout << "Zad3 \n";
    //zad3();
    //for(float r = 2; r<=4; r+=0.01)
    //    zad4(r);
    //
    //for(float r = 3.75; r <= 3.8; r+= 0.01)
    //    zad4(r);
    //
    //cout << "double" << endl;
    //
    //for(double r = 3.75; r <= 3.8; r+= 0.01)
    //    zad4(r);
    zad4(4.0);
    return 0;
}
