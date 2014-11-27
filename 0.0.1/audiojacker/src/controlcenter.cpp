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
void audiojack_connect(){
    std::cout << "audio jack has been connected." << std::endl;
}
void audiojack_disconnect(){
    std::cout << "audio jack has been disconnected." << std::endl;
}
void volume_update(std::string volume){
    std::cout << "volume has been updated to "<< volume << std::endl;
}
