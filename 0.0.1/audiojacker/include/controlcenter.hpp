#ifndef CONTROLCENTER_H
#define CONTROLCENTER_H

#include<string>
class controlcenter
{
    public:
        controlcenter();
        virtual ~controlcenter();
        void audiojack_connect();
        void audiojack_disconnect();
        void volume_update(std::string volume);
    protected:
    private:
};

#endif // CONTROLCENTER_H
