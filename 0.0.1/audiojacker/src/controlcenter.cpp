#include "controlcenter.hpp"
#include<iostream>
#include "volumecontroller.hpp"
controlcenter::controlcenter()
{
    //ctor
}

controlcenter::~controlcenter()
{
    //dtor
}
bool controlcenter::operator==(const controlcenter){
    return true;
}
void controlcenter::audiojack_connect(){

}
void controlcenter::audiojack_disconnect(){
    volumecontroller::togglevolume();
}

void controlcenter::lid_open(){
    volumecontroller::togglevolume();
}
void controlcenter::lid_close(){
    volumecontroller::togglevolume();
}
