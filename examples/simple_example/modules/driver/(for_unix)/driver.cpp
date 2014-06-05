#include ".madz/cpp/.wrap-cpp/madz.h" //"madz.h" would also work.

void MADZOUT::_init() {

}

// Using proc cpuinfo strategy detailed here:
// stackoverflow.com/questions/9629850/how-to-get-cpu-info-in-c-on-linux-such-as-number-of-cores
void MADZOUT::_f::do_driver() {
       FILE *cpuinfo = fopen("/proc/cpuinfo", "rb");
   char *arg = 0;
   size_t size = 0;
   while(getdelim(&arg, &size, 0, cpuinfo) != -1)
   {
      puts(arg);
   }
   free(arg);
   fclose(cpuinfo);

}
