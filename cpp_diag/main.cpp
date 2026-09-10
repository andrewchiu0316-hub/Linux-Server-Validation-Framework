#include <fstream>
#include <iostream>
#include <string>

int main() {
    std::ifstream cpu("/proc/cpuinfo"), mem("/proc/meminfo"), load("/proc/loadavg");
    if (!cpu || !mem || !load) { std::cerr << "This probe requires Linux /proc files\n"; return 2; }
    std::string line; int cores = 0; long long memory_kb = 0; double load_average = 0.0;
    while (std::getline(cpu, line)) if (line.rfind("processor", 0) == 0) ++cores;
    while (std::getline(mem, line)) if (line.rfind("MemTotal:", 0) == 0) { sscanf(line.c_str(), "MemTotal: %lld", &memory_kb); break; }
    load >> load_average;
    if (cores <= 0 || memory_kb <= 0) { std::cerr << "Unable to parse /proc data\n"; return 3; }
    std::cout << "{\"cpu_cores\":" << cores << ",\"memory_total_kb\":" << memory_kb
              << ",\"load_average\":" << load_average << ",\"status\":\"OK\"}\n";
}
