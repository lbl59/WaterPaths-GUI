//
// Created by bernardo on 2/3/17.
//

#ifndef TRIANGLEMODEL_RESTRICTIONS_H
#define TRIANGLEMODEL_RESTRICTIONS_H


#include "../SystemComponents/Utility/Utility.h"
#include "Base/DroughtMitigationPolicy.h"

class Restrictions : public DroughtMitigationPolicy {

private:
    double current_multiplier = 0;
    vector<vector<double>> restricted_weekly_average_volumetric_price;

    vector<double> stage_multipliers;
    vector<double> stage_triggers;

public:
    Restrictions(const int id, const vector<double> &stage_multipliers,
                 const vector<double> &stage_triggers);

    Restrictions(
            const int id, const vector<double> &stage_multipliers,
            const vector<double> &stage_triggers,
            const vector<vector<double>> *typesMonthlyDemandFraction,
            const vector<vector<double>> *typesMonthlyWaterPrice,
            const vector<vector<double>> *priceMultipliers);

    Restrictions(const Restrictions &reservoir);

    void applyPolicy(int week) override;

    void addSystemComponents(vector<Utility *> systems_utilities,
                                 vector<WaterSource *> water_sources,
                                 vector<MinEnvFlowControl *> min_env_flow_controls) override;

    double getCurrent_multiplier() const;

    ~Restrictions();

    void calculateWeeklyAverageWaterPrices(
            const vector<vector<double>> *typesMonthlyDemandFraction,
            const vector<vector<double>> *typesMonthlyWaterPrice,
            const vector<vector<double>> *priceMultipliers);

    void setRealization(unsigned long realization_id, const vector<double> &utilities_rdm,
                        const vector<double> &water_sources_rdm, const vector<double> &policy_rdm) override;

    void setupTriggers(const vector<double> &stage_multipliers,
                       const vector<double> &stage_triggers);

    const vector<double> &getStageMultipliers() const;

    const vector<double> &getStageTriggers() const;
};


#endif //TRIANGLEMODEL_RESTRICTIONS_H
