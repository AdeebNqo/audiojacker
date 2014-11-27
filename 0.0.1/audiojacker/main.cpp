#include <iostream>
#include "headsetjackhandler.hpp"
#include "controlcenter.hpp"
using namespace std;
using namespace audiojacker;

int main()
{
    controlcenter controller;
     cout << "0.Hello world!" << endl;
    headsetevents<controlcenter> events;
     cout << "1.Hello world!" << endl;
    events.registerlistener(controller);
     cout << "2.Hello world!" << endl;
    events.start();
    cout << "3.Hello world!" << endl;
    while(true){
    }
    return 0;
}
