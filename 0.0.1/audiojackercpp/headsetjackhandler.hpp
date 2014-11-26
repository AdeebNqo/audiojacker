#ifndef HEADSETEVENTS_H
#define HEADSETEVENTS_H

#include <vector>
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
    headsetevents();
    ~headsetevents();

    void start(){

    }
    void stop(){

    }

    /*
     * The following methods should be used to register objects which
     * want to be alerted of various events made by the audio jack and other
     * associated parts e.g volume increase/decrease
     *
     * Methods to be implemented by the objects which want to be alerted are:
     *
     * 1. audiojack_connect()
     * 2. audiojack_disconnect()
     * 3. volume_update(string volume)
     *
     */
    template <class T> void registerlistener(T listener){
        listeners.push_back(listener);
    }
    template <class T> void unregisterlistener(T listener){
        listeners.erase(std::find(listeners.begin(), listeners.end(), listener));
    }

    template <class T> std::vector<T> listeners; //list of objects which have subscribed to the event handler.
};

}

#endif
