//
// Created by bernardoct on 8/26/17.
//

#include <sstream>
#include <iomanip>
#include "AllocatedReservoirDataCollector.h"

AllocatedReservoirDataCollector::AllocatedReservoirDataCollector(AllocatedReservoir *allocated_reservoir,
                                                                 unsigned long realization)
        : ReservoirDataCollector(allocated_reservoir, ALLOCATED_RESERVOIR, (7 + (int) allocated_reservoir->
                getAvailable_allocated_volumes().size()) * COLUMN_WIDTH, realization),
          allocated_reservoir(allocated_reservoir),
          utilities_with_allocations
                  (allocated_reservoir->getUtilitiesWithAllocations()) {
}

string AllocatedReservoirDataCollector::printTabularString(int week) {
    string output = ReservoirDataCollector::printTabularString(week);

    stringstream out_stream;

    out_stream << output;

    for (int u : utilities_with_allocations)
        out_stream << setw(COLUMN_WIDTH) << setprecision(COLUMN_PRECISION)
                   << allocated_stored_volumes[week][u];

    return out_stream.str();
}

string AllocatedReservoirDataCollector::printCompactString(int week) {
    string output = ReservoirDataCollector::printCompactString(week);

    stringstream out_stream;

    out_stream << output;

    for (int u : utilities_with_allocations) {
        out_stream << allocated_stored_volumes[week][u] << ",";
        out_stream << allocated_treatment_cap[week][u] << ",";
    }

    return out_stream.str();
}

string AllocatedReservoirDataCollector::printTabularStringHeaderLine1() {
    string output = ReservoirDataCollector::printTabularStringHeaderLine1();

    stringstream out_stream;

    out_stream << output;

    for (unsigned long u = 0; u < allocated_reservoir->getUtilitiesWithAllocations().size(); ++u)
        out_stream << setw(COLUMN_WIDTH) << "Stored V.";

    return out_stream.str();
}

string AllocatedReservoirDataCollector::printTabularStringHeaderLine2() {
    string output = ReservoirDataCollector::printTabularStringHeaderLine2();

    stringstream out_stream;

    out_stream << output;

    for (const int &u : allocated_reservoir->getUtilitiesWithAllocations())
        out_stream << setw(COLUMN_WIDTH) << "Alloc. " + to_string(u);

    return out_stream.str();
}

string AllocatedReservoirDataCollector::printCompactStringHeader() {

    stringstream out_stream;

    for (int u : utilities_with_allocations) {
        out_stream << id << "valloc_" + to_string(u) << ",";
        out_stream << id << "talloc_" + to_string(u) << ",";
    }
    return ReservoirDataCollector::printCompactStringHeader() + out_stream.str();
}

void AllocatedReservoirDataCollector::collect_data() {
    ReservoirDataCollector::collect_data();
    vector<double> alloc_vol_vector = allocated_reservoir->getAvailable_allocated_volumes();
    allocated_stored_volumes.push_back(alloc_vol_vector);
    auto alloc_treat_vector = allocated_reservoir->getAllocatedTreatmentCapacities();
    allocated_treatment_cap.push_back(alloc_treat_vector);
}
