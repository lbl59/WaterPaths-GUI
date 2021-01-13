//
// Created by Bernardo on 5/10/2020.
//

#include <iomanip>
#include "TransfersBilateralDataCollector.h"


TransfersBilateralDataCollector::TransfersBilateralDataCollector(
        TransfersBilateral *transfer_policy, unsigned long realization)
        : DataCollector(transfer_policy->id, "", realization,
                        BILATERAL_TRANSFERS, NON_INITIALIZED),
          transfer_policy(transfer_policy),
          utilities_ids(transfer_policy->getUtilities_ids()) {
}

string TransfersBilateralDataCollector::printTabularString(int week) {

    stringstream outStream;

    for (double &a : demand_offsets.at((unsigned int) week))
        outStream << setw(COLUMN_WIDTH) << setprecision(COLUMN_PRECISION) << a;

    return outStream.str();
}

string TransfersBilateralDataCollector::printCompactString(int week) {

    stringstream outStream;

    for (double &a : demand_offsets.at((unsigned int) week))
        outStream << a << ",";

    return outStream.str();
}

string TransfersBilateralDataCollector::printTabularStringHeaderLine1() {

    stringstream outStream;

    for (unsigned long id = 0; id < utilities_ids.size(); ++id)
        outStream << setw(COLUMN_WIDTH) << "Transf.";

    return outStream.str();
}

string TransfersBilateralDataCollector::printTabularStringHeaderLine2() {

    stringstream outStream;

    for (int buyer_id : utilities_ids)
        outStream << setw(COLUMN_WIDTH) << "Alloc. " + to_string(buyer_id);

    return outStream.str();
}

string TransfersBilateralDataCollector::printCompactStringHeader() {
    stringstream outStream;

    for (int &a : utilities_ids)
        outStream << a << "transf" << ",";

    return outStream.str();
}

void TransfersBilateralDataCollector::collect_data() {
    demand_offsets.push_back(transfer_policy->getTransferedVolumes());
}
