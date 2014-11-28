#include "controlcenter.hpp"
#include<iostream>
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
    std::cout << "audio jack has been disconnected." << std::endl;
}
void controlcenter::volume_update(std::string volume){
    std::cout << "volume has been updated to "<< volume << std::endl;
}
