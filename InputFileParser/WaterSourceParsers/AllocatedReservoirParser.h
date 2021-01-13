//
// Created by Bernardo on 11/25/2019.
//

#ifndef TRIANGLEMODEL_ALLOCATEDRESERVOIRPARSER_H
#define TRIANGLEMODEL_ALLOCATEDRESERVOIRPARSER_H


#include "ReservoirParser.h"

class AllocatedReservoirParser : public ReservoirParser {
public:
    AllocatedReservoirParser(bool generate_tables);

    WaterSource *
    generateSource(int id, vector<vector<string>> &block, int line_no,
                   int n_realizations, int n_weeks,
                   const map<string, int> &ws_name_to_id,
                   const map<string, int> &utility_name_to_id,
                   map<string, vector<vector<double>>> &pre_loaded_data) override;

    void checkMissingOrExtraParams(int line_no,
                                   vector<vector<string>> &block) override;

    void preProcessBlock(vector<vector<string>> &block, int line_no,
                         const map<string, int> &utility_name_to_id);
};


#endif //TRIANGLEMODEL_ALLOCATEDRESERVOIRPARSER_H
