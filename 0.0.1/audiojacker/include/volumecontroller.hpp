#ifndef VOLUMECONTROLLER_H
#define VOLUMECONTROLLER_H

#include <string>
namespace volumecontroller{
    static bool togglevolume(){
        std::string command = "amixer -D pulse set Master Playback Switch toggle";
        FILE *pipe;
        //char buff[512];
        if ( !(pipe = popen( command.c_str(), "r")) ) return false;
        return true;
    }
}

#endif // VOLUMECONTROLLER_H
