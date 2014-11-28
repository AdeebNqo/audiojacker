#ifndef HEADSETEVENTS_H
#define HEADSETEVENTS_H

#include <vector>
#include <thread>
#include <cerrno>
#include <unistd.h>
#include "controlcenter.hpp"
#include <algorithm>
/*
 * Le header file ine-declarations zeklasi umsebenzi wayo
 * kukolinda ii-iventsi ezenziwa yiaudio jack xa ikhutshwa
 * okanye ifakwa.
 *
 * @umbhali Zola Mahlaza <adeebnqo@gmail.com>
 * @umhla 26 eyeNkanga 2014 (26 November 2014)
 */

namespace audiojacker{
class headsetevents{
  public:
    headsetevents(){

    }
    ~headsetevents(){

    }

    void start(){
        activated = true;
        auto func = [this] (){

                    std::string command = "acpi_listen";
                    FILE *pipe;
                    char buff[512];
                    if ( !(pipe = popen( command.c_str(), "r")) ) return false;

                    int d = fileno(pipe);
                    while ( this->activated )
                    {

                        ssize_t r = read(d, buff, sizeof(buff));
                        if (r == -1 && errno == EAGAIN) // really need errno?
                            continue;
                        else if (r > 0){
                            std::string buffstring = std::string(buff);
                            /*
                            Options:

                            1. button/volumeup VOLUP 00000080 00000000 K
                            2. button/volumedown VOLDN 00000080 00000000 K
                            3. jack/headphone HEADPHONE plug
                            4. jack/headphone HEADPHONE unplug
                            5. jack/headphone MICROPHONE plug
                            6. jack/headphone MICROPHONE unplug

                            */
                            std::string volup("button/volumeup VOLUP 00000080 00000000 K");
                            std::string voldn("button/volumedown VOLDN 00000080 00000000 K");
                            std::string headplug("jack/headphone HEADPHONE plug");
                            std::string headunplug("jack/headphone HEADPHONE unplug");
                            std::string micplug("jack/headphone MICROPHONE plug");
                            std::string micunplug("jack/headphone MICROPHONE unplug");

                            if (buffstring.compare(0, volup.length(), volup) == 0){

                            }
                            else if(buffstring.compare(0, voldn.length(), voldn) == 0){

                            }
                            else if(buffstring.compare(0, headplug.length(), headplug) == 0){
                                    //audiojack_connect()
                                    auto it = listeners.begin();
                                    auto endP = listeners.end();
                                    for (; it!=endP; ++it){
                                        it->audiojack_connect();
                                    }
                            }
                            else if(buffstring.compare(0, headunplug.length(), headunplug) == 0){
                                    //void audiojack_disconnect()
                                    auto it = listeners.begin();
                                    auto endP = listeners.end();
                                    for (; it!=endP; ++it){
                                        it->audiojack_disconnect();
                                    }
                            }
                            else if(buffstring.compare(0, micplug.length(), micplug) == 0){

                            }
                            else if(buffstring.compare(0, micunplug.length(), micunplug) == 0){

                            }
                            std::cout << buffstring << std::endl;
                        }
                        else
                            break;
                    }
                    pclose(pipe);
                };
        worker = std::thread(func);
    }

    void stop(){
        activated = false;
    }

    /*
     * The following methods should be used to register objects which
     * want to be alerted of various events made by the audio jack and other
     * associated parts e.g volume increase/decrease
     *
     * Methods to be implemented by the objects which want to be alerted are:
     *
     * 1. void audiojack_connect()
     * 2. void audiojack_disconnect()
     * 3. void volume_update(string volume)
     *
     */
    void registerlistener(controlcenter listener){
        listeners.push_back(listener);
    }
    void unregisterlistener(controlcenter listener){
        listeners.erase(std::find(listeners.begin(), listeners.end(), listener));
    }

    std::vector<controlcenter> listeners; //list of objects which have subscribed to the event handler.

   private:
    bool activated = true;
    std::thread worker;
};

}

#endif
