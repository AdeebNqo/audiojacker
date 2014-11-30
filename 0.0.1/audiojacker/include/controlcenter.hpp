#ifndef CONTROLCENTER_H
#define CONTROLCENTER_H

#include<string>
class controlcenter
{
    public:
        controlcenter();
        virtual ~controlcenter();
        bool operator==(const controlcenter);
        void audiojack_connect();
        void audiojack_disconnect();
        void lid_open();
        void lid_close();
    protected:
    private:
};

#endif // CONTROLCENTER_H
