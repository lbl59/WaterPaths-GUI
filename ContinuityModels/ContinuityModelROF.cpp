//
// Created by bernardo on 1/26/17.
//

#include <iostream>
#include <algorithm>
#include <fstream>
#include <iomanip>
#include "ContinuityModelROF.h"
#include "../Utils/Utils.h"

ContinuityModelROF::ContinuityModelROF(vector<WaterSource *> water_sources, const Graph &water_sources_graph,
                                       const vector<vector<int>> &water_sources_to_utilities,
                                       vector<Utility *> utilities,
                                       vector<MinEnvFlowControl *> min_env_flow_controls,
                                       const vector<double> &utilities_rdm,
                                       const vector<double> &water_sources_rdm, unsigned long total_weeks_simulation,
                                       const int use_precomputed_rof_tables, const unsigned long realization_id)
        : ContinuityModel(water_sources, utilities, min_env_flow_controls,
                          water_sources_graph, water_sources_to_utilities, utilities_rdm,
                          water_sources_rdm,
                          realization_id),
          n_topo_sources((int) sources_topological_order.size()),
          use_precomputed_rof_tables(use_precomputed_rof_tables) {
    // update utilities' total stored volume
    for (Utility *u : this->continuity_utilities) {
        u->updateTotalAvailableVolume();
        u->setNoFinaicalCalculations();
    }

    for (int u = 0; u < n_utilities; ++u) {
        ut_storage_to_rof_rof_realization.emplace_back(
                (unsigned long) ceil(WEEKS_IN_YEAR),
                (unsigned long) NO_OF_INSURANCE_STORAGE_TIERS + 1);
        if (use_precomputed_rof_tables != IMPORT_ROF_TABLES) {
            ut_storage_to_rof_table.emplace_back(
                    total_weeks_simulation,
                    (unsigned long) NO_OF_INSURANCE_STORAGE_TIERS + 1);
        }
    }

    // Record which sources have no downstream sources.
    storage_wout_downstream = new bool[sources_topological_order.size()];
    for (int ws : sources_topological_order)
        storage_wout_downstream[ws] = downstream_sources[ws] != NON_INITIALIZED;

    // Get next online downstream source for each source.
    online_downstream_sources = getOnlineDownstreamSources();

    // Calculate utilities' base delta storage corresponding to one table
    // tier and status-quo base storage capacity.
    if (use_precomputed_rof_tables == IMPORT_ROF_TABLES) {
        for (int u = 0; u < n_utilities; ++u) {
            utility_base_storage_capacity.push_back(
                    continuity_utilities[u]->getTotal_storage_capacity() *
                    BASE_STORAGE_CAPACITY_MULTIPLIER);
            utility_base_delta_capacity_table.push_back(
                    utility_base_storage_capacity[u] /
                    NO_OF_INSURANCE_STORAGE_TIERS);
        }

        current_and_base_storage_capacity_ratio =
                vector<double>((unsigned long) n_utilities);
        current_storage_table_shift =
                vector<double>((unsigned long) n_utilities);
    }
}

ContinuityModelROF::~ContinuityModelROF() {
    delete[] storage_wout_downstream;
}

/**
 * Runs one the full rof calculations for realization #realization_id for a
 * given week.
 * @param week for which rof is to be calculated.
 */
vector<double> ContinuityModelROF::calculateLongTermROF(int week) {
    // vector where risks of failure will be stored.
    vector<double> risk_of_failure((unsigned long) n_utilities, 0.0);
    vector<double> year_failure((unsigned long) n_utilities, 0.0);

    // checks if new infrastructure became available and, if so, set the
    // corresponding realization
    // infrastructure online.
    updateOnlineInfrastructure(week);

    // perform a continuity simulation for NUMBER_REALIZATIONS_ROF (50) yearly
    // realization.
    for (int yr = 0; yr < NUMBER_REALIZATIONS_ROF; ++yr) {
        // reset current reservoirs' and utilities' storage and combined
        // storage, respectively, in the corresponding realization simulation.
        resetUtilitiesAndReservoirs(LONG_TERM_ROF);

        for (int w = 0; w < WEEKS_ROF_LONG_TERM; ++w) {
            // one week continuity time-step.
            continuityStep(w + week, yr, APPLY_DEMAND_BUFFER);

            // check total available storage for each utility and, if smaller
            // than the fail ration, increase the number of failed years of
            // that utility by 1 (FAILURE).
            for (int u = 0; u < n_utilities; ++u)
                if (continuity_utilities[u]->getStorageToCapacityRatio() <=
                    STORAGE_CAPACITY_RATIO_FAIL || continuity_utilities[u]->getUnrestrictedDemand() > 0.9 * continuity_utilities[u]->getTotal_treatment_capacity()) {
                    year_failure[u] = FAILURE;
                }
        }

        // Count failures and reset failures counter.
        for (int uu = 0; uu < n_utilities; ++uu) {
            risk_of_failure[uu] += year_failure[uu];
            year_failure[uu] = NON_FAILURE;
        }
    }

    // Finish ROF calculations
    for (int i = 0; i < n_utilities; ++i) {
        risk_of_failure[i] /= NUMBER_REALIZATIONS_ROF;
    }

    return risk_of_failure;
}

vector<double> ContinuityModelROF::calculateShortTermROF(int week,
                                                         int import_export_rof_tables) {
    vector<double> risk_of_failure;
    if (import_export_rof_tables == IMPORT_ROF_TABLES) {
        return ContinuityModelROF::calculateShortTermROFTable(week,
                                                              realization_utilities,
                                                              utility_base_storage_capacity,
                                                              ut_storage_to_rof_table,
                                                              current_storage_table_shift);
    } else {
        return ContinuityModelROF::calculateShortTermROFFullCalcs(week);
    }
}

/**
 * Runs one the full rof calculations for realization #realization_id for a
 * given week.
 * @param week for which rof is to be calculated.
 */
vector<double> ContinuityModelROF::calculateShortTermROFTable(int week,
                                                              vector<Utility *> utilities,
                                                              vector<double> utilities_base_storage_capacity,
                                                              const vector<Matrix2D<double>> &ut_storage_to_rof_table,
                                                              vector<double> current_storage_table_shift) {
    // vector where risks of failure will be stored.
    auto n_utilities = utilities.size();
    vector<double> risk_of_failure(n_utilities, 0.0);
    double m;
    for (int u = 0; u < n_utilities; ++u) {
        // Get current stored volume for utility u.
        double utility_storage =
                utilities[u]->getTotal_stored_volume();
        // Ratio of current and status-quo utility storage capacities
        //        double m = current_and_base_storage_capacity_ratio[u];
        m = utilities[u]->getTotal_storage_capacity() /
            utilities_base_storage_capacity[u];
        // Calculate base table tier that contains the desired ROF by
        // shifting the table around based on new infrastructure -- the
        // shift is made by the part (m - 1) * STORAGE_CAPACITY_RATIO_FAIL *
        // utility_base_storage_capacity[u] - current_storage_table_shift[u]
        double storage_convert = utility_storage +
                                 STORAGE_CAPACITY_RATIO_FAIL *
                                 utilities_base_storage_capacity[u] *
                                 (1. - m) + current_storage_table_shift[u];
        int tier = (int) (storage_convert * NO_OF_INSURANCE_STORAGE_TIERS /
                          utilities_base_storage_capacity[u]);
        // Mean ROF between the two tiers of the ROF table where
        // current storage is located.
//        risk_of_failure[u] = ut_storage_to_rof_table[u](week, tier);
        risk_of_failure[u] = (ut_storage_to_rof_table[u](week, tier) +
                              ut_storage_to_rof_table[u](week, tier + 1)) / 2;
    }

    return risk_of_failure;
}

/**
 * Runs one the full rof calculations for realization #realization_id for a
 * given week.
 * @param week for which rof is to be calculated.
 */
vector<double> ContinuityModelROF::calculateShortTermROFFullCalcs(int week) {
    // vector where risks of failure will be stored.
    vector<double> risk_of_failure((unsigned long) n_utilities, 0.0);
    vector<double> year_failure((unsigned long) n_utilities, 0.0);
    double to_full[n_sources];

    // Empty volumes are later used to update ROF tables.
    calculateEmptyVolumes(realization_water_sources, to_full);

    int week_of_the_year = Utils::weekOfTheYear(week);

    // checks if new infrastructure became available and, if so, set the
    // corresponding realization infrastructure online.
    updateOnlineInfrastructure(week);

    // perform a continuity simulation for NUMBER_REALIZATIONS_ROF (50)
    // yearly realization.
    for (int yr = 0; yr < NUMBER_REALIZATIONS_ROF; ++yr) {
        // Reset realization temp tables
        for (auto &t : ut_storage_to_rof_rof_realization)
            t.reset(NON_FAILURE);

        // reset current reservoirs' and utilities' storage and combined
        // storage, respectively, in the corresponding realization simulation.
        resetUtilitiesAndReservoirs(SHORT_TERM_ROF);

        for (int w = 0; w < WEEKS_ROF_SHORT_TERM; ++w) {
            // one week continuity time-step.
            continuityStep(w + week, yr, !APPLY_DEMAND_BUFFER);

            // check total available storage for each utility and, if smaller
            // than the fail ration, increase the number of failed years of
            // that utility by 1 (FAILURE).
            for (int u = 0; u < n_utilities; ++u)
                if (continuity_utilities[u]->getStorageToCapacityRatio() <=
                    STORAGE_CAPACITY_RATIO_FAIL || continuity_utilities[u]->getUnrestrictedDemand() > 0.9 * continuity_utilities[u]->getTotal_treatment_capacity()) {
                    year_failure[u] = FAILURE;
                }

            // calculated week of storage-rof table
            updateStorageToROFTable(INSURANCE_SHIFT_STORAGE_CURVES_THRESHOLD,
                                    week_of_the_year, to_full);
        }

        // Record ROF realization results into final ROF table for that week.
        recordROFStorageTable(ut_storage_to_rof_rof_realization,
                              ut_storage_to_rof_table,
                              n_utilities, week, week_of_the_year);

        // Count failures and reset failures counter.
        for (int uu = 0; uu < n_utilities; ++uu) {
            risk_of_failure[uu] += year_failure[uu];
            year_failure[uu] = NON_FAILURE;
        }
    }

    setInitialTableTier(week, n_utilities, ut_storage_to_rof_table,
                        beginning_tier);

    // Finish ROF calculations
    for (int u = 0; u < n_utilities; ++u) {
        risk_of_failure[u] /= NUMBER_REALIZATIONS_ROF;
        if (std::isnan(risk_of_failure[u])) {
            string error_m = "nan rof imported tables. Realization " +
                             to_string(realization_id) + ", week " +
                             to_string(week) + ", utility " + to_string(u);
            printf("%s", error_m.c_str());
            throw_with_nested(logic_error(error_m.c_str()));
        }
    }

    return risk_of_failure;
}

/**
 * Updates approximate ROF table based on continuity realization ran for
 * simulation based ROF calculations.
 * @param storage_percent_decrement
 * @param week_of_the_year
 * @param to_full empty volume of all reservoir in ID order.
 */
#pragma GCC optimize("O3")
void ContinuityModelROF::updateStorageToROFTable(
        double storage_percent_decrement, int week_of_the_year,
        const double *to_full) {
    double available_volumes[n_sources];
    for (int ws = 0; ws < n_sources; ++ws) {
        available_volumes[ws] =
                continuity_water_sources[ws]->getAvailableSupplyVolume();
    }

    // loops over the percent storage levels to populate table. The loop
    // begins from one level above the level  where at least one failure was
    // observed in the last iteration. This saves a lot of computational time.
    for (int s = beginning_tier; s <= NO_OF_INSURANCE_STORAGE_TIERS; ++s) {
        // calculate delta storage for all reservoirs and array that will
        // receive the shifted storage curves.
        double percent_decrement_storage_level =
                (double) s * storage_percent_decrement;
        double delta_storage[n_sources];
        double available_volumes_shifted[n_sources];
        memcpy(available_volumes_shifted, available_volumes,
               sizeof(double) * n_sources);

        // calculate the difference between the simulated available water and
        // the one for the table calculated above based on the percent
        // decrement.
        for (int wss = 0; wss < n_sources; ++wss) {
            delta_storage[wss] = to_full[wss] - water_sources_capacities[wss] *
                                                percent_decrement_storage_level;
        }

        // Shift storages.
        shiftStorages(available_volumes_shifted, delta_storage);

        // Checks for utilities failures.
        int count_fails = 0;
        for (int u = 0; u < n_utilities; ++u) {
            double utility_storage = 0;
            // Calculate combined stored volume for each utility based on
            // shifted storages.
            for (int ws : water_sources_online_to_utilities[u])
                utility_storage += available_volumes_shifted[ws] *
                                   continuity_water_sources[ws]->getSupplyAllocatedFraction(
                                           u) *
                                    (realization_utilities[u]->hasTreatmentConnected(ws)
                                    &&
                                    realization_water_sources[ws]->isOnline());
            // Register failure in the table for each utility meeting
            // failure criteria.
            if (utility_storage / utilities_capacities[u] <
                STORAGE_CAPACITY_RATIO_FAIL) {
                ut_storage_to_rof_rof_realization[u](week_of_the_year,
                                                     NO_OF_INSURANCE_STORAGE_TIERS -
                                                     s) = FAILURE;
                count_fails++;
            }
        }

        // If all utilities have failed, stop dropping storage level and label
        // all storage levels below failures.
        if (count_fails == n_utilities) {
            for (int ss = s; ss <= NO_OF_INSURANCE_STORAGE_TIERS; ++ss) {
                for (unsigned long u = 0;
                     u < (unsigned long) n_utilities; ++u) {
                    ut_storage_to_rof_rof_realization[u](week_of_the_year,
                                                         NO_OF_INSURANCE_STORAGE_TIERS -
                                                         ss)
                            = FAILURE;
                }
            }
            break;
        }
    }
}

//FIXME: MAKE THIS MORE EFFICIENT. THIS METHOD IS THE MOST EXPENSIVE ONE IN THE CODE.
#pragma GCC optimize("O3")
void ContinuityModelROF::shiftStorages(
        double *available_volumes_shifted,
        const double *delta_storage) {
    // Add deltas to all sources following the topological order, so that
    // upstream is calculated before downstream.
    for (int ws : sources_topological_order) {
        // calculate initial estimate for shifted
        available_volumes_shifted[ws] += delta_storage[ws];

        double available_volume_to_full = water_sources_capacities[ws] -
                                          available_volumes_shifted[ws];

        // if not full, retrieve spill to downstream source.
        if (available_volume_to_full > 0) {
            // Calculate spilled water. Since the curves are shifted as the
            // weeks of the rof realizations are calculated, the minimum
            // environmental outflows below will be the ones at the time when
            // the storage is being shifted.
            double spillage =
                    continuity_water_sources[ws]->getTotal_outflow() -
                    continuity_water_sources[ws]
                            ->getMin_environmental_outflow();

            double spillage_retrieved = min(available_volume_to_full, spillage);

            available_volumes_shifted[ws] += spillage_retrieved;

            if (online_downstream_sources[ws] > 0)
                available_volumes_shifted[online_downstream_sources[ws]] -=
                        spillage_retrieved;
        } else {
            double spillage = -available_volume_to_full;
            if (online_downstream_sources[ws] > 0) {
                available_volumes_shifted[ws] -= spillage;
                available_volumes_shifted[online_downstream_sources[ws]] +=
                        spillage;
            }
        }
    }
}


/**
 * Prints a binary file with the rof_table for a given realization in a
 * given week.
 * @param week
 */
void ContinuityModelROF::printROFTable(const string &folder) {
    for (int u = 0; u < n_utilities; ++u) {

        string file_name =
                folder + "tables_r" + to_string(realization_id) + "_u" +
                to_string(u) + ".csv";
        ofstream output_file(file_name);

        auto num_weeks = ut_storage_to_rof_table[u].get_i();
        for (int w = 0; w < num_weeks; ++w) {
            auto data = ut_storage_to_rof_table[u].getPointerToElement(w, 0);
            std::ostringstream week_table;
            week_table << std::fixed;
            week_table << std::setprecision(2);
            for (int t = 0; t < NO_OF_INSURANCE_STORAGE_TIERS; ++t) {
                week_table << to_string(data[t]) + ",";
            }

            string line = week_table.str();
            line.pop_back();
            output_file << line;
            if (w < num_weeks - 1)
                output_file << endl;
        }

        output_file.close();
    }
}

/**
 * reset reservoirs' and utilities' storage and last release, and
 * combined storage, respectively, they currently have in the
 * corresponding realization simulation.
 */
void ContinuityModelROF::resetUtilitiesAndReservoirs(int rof_type) {
    // update water sources info. If short-term rof, return to current
    // storage; if long-term, make them full.
    if (rof_type == SHORT_TERM_ROF)
        for (int i = 0; i < n_sources; ++i) {   // Current available volume
            continuity_water_sources[i]->setAvailableAllocatedVolumes
                    (realization_water_sources[i]
                             ->getAvailable_allocated_volumes(),
                     realization_water_sources[i]->getAvailableVolume());
            continuity_water_sources[i]->setOutflow_previous_week(
                    realization_water_sources[i]->getTotal_outflow());
        }
    else
        for (int i = 0; i < n_sources; ++i) {   // Full capacity
            continuity_water_sources[i]->setFull();
            continuity_water_sources[i]->setOutflow_previous_week(
                    realization_water_sources[i]->getTotal_outflow());
        }

    // update utilities combined storage.
    for (Utility *u : continuity_utilities) {
        u->updateTotalAvailableVolume();
    }
}

/**
 * Pass to the rof continuity model the locations of the utilities
 * of the realization it calculated rofs for.
 * @param realization_water_sources
 */
void ContinuityModelROF::connectRealizationWaterSources(
        const vector<WaterSource *> &realization_water_sources) {
    ContinuityModelROF::realization_water_sources =
            realization_water_sources;
}

/**
 * Pass to the rof continuity model the locations of the utilities
 * of the realization it calculated rofs for.
 * @param realization_utilities
 */
void ContinuityModelROF::connectRealizationUtilities(
        const vector<Utility *> &realization_utilities) {
    ContinuityModelROF::realization_utilities = realization_utilities;
}

/**
 * Checks if new infrastructure became online.
 */
void ContinuityModelROF::updateOnlineInfrastructure(int week) {
    for (unsigned long ws = 0; ws < (unsigned long) n_sources; ++ws) {
        // Check if any infrastructure option is online in the
        // realization model and not in the ROF model.
        if (realization_water_sources.at(ws)->isOnline() &&
            !continuity_water_sources.at(ws)->isOnline()) {
            // If so, set it online in the ROF calculation model.
            for (int uu : utilities_to_water_sources[ws]) {
                auto u = (unsigned long) uu;
                water_sources_online_to_utilities.at(u).push_back((int) ws);
                continuity_utilities.at(u)
                        ->setWaterSourceOnline((int) ws, week);


                // Update the shift in storage to be used to calculate the
                // tier in precomputed ROF tables corresponding to the
                // current storage of a given utility.
                if (use_precomputed_rof_tables == IMPORT_ROF_TABLES)
                    current_storage_table_shift.at(u) += table_storage_shift.at(
                                    u)
                            .at(ws);
            }

            // Update water source capacities in case a reservoir expansion
            // was built.
            water_sources_capacities.at(ws) =
                    continuity_water_sources.at(ws)->getSupplyCapacity();
        }
    }

    // Update utilities' storage capacities and their ratios to status-quo
    // capacities in case new infrastructure has been built.
    if (Utils::isFirstWeekOfTheYear(week) || week == 0) {
        for (unsigned long u = 0; u < (unsigned long) n_utilities; ++u) {
            utilities_capacities.at(u) =
                    continuity_utilities.at(u)->getTotal_storage_capacity();
        }

        if (use_precomputed_rof_tables == IMPORT_ROF_TABLES) {
            for (unsigned long u = 0; u < (unsigned long) n_utilities; ++u) {
                current_and_base_storage_capacity_ratio.at(u) =
                        utilities_capacities.at(u) /
                        utility_base_storage_capacity.at(u);
            }
        }
    }

    // Update list of downstream sources of each source.
    online_downstream_sources = getOnlineDownstreamSources();
}

void ContinuityModelROF::setROFTablesAndShifts(
        const vector<Matrix2D<double>> &storage_to_rof_table,
        const vector<vector<double>> &table_storage_shift) {
    this->ut_storage_to_rof_table = storage_to_rof_table;
    this->table_storage_shift = table_storage_shift;
}


void ContinuityModelROF::tableROFExceptionHandler(double m, int u, int week) {
    string error;
    if (m > 1.) {
        error = "ROF tables being extrapolated  because current "
                "capacity is greater than table base capacity."
                " Utility " + to_string(u) + ", m=" +
                to_string(m) + ". You should try regenerating "
                               "tables with a higher value for constant "
                               "BASE_STORAGE_CAPACITY_MULTIPLIER  and higher"
                               " number of table tiers";
        throw_with_nested(logic_error(error.c_str()));
    } else {
        error = "Exception happened in week " + to_string(week) +
                " for utility " + to_string(u) + "\n";
        throw_with_nested(runtime_error(error.c_str()));
    }
}

vector<Matrix2D<double>> &ContinuityModelROF::getUt_storage_to_rof_table() {
    return ut_storage_to_rof_table;
}

/**
 * Set first tier for ROF table calculation close to where the first
 * failure was observed for last week's table, so to save computations
 * @param week
 * @param n_utilities
 * @param ut_storage_to_rof_table
 * @param beginning_tier
 */
void ContinuityModelROF::setInitialTableTier(int week, const int &n_utilities,
                                             vector<Matrix2D<double>> &ut_storage_to_rof_table,
                                             int &beginning_tier) {
    for (int s = 0; s < NO_OF_INSURANCE_STORAGE_TIERS; ++s) {
        int count_failures = 0;
        for (int u = 0; u < n_utilities; ++u) {
            if (ut_storage_to_rof_table[u](week,
                                           NO_OF_INSURANCE_STORAGE_TIERS - s) >
                0.) {
                ++count_failures;
            }
        }
        if (count_failures == 0)
            beginning_tier = max(0, s - 1);
        else
            break;
    }
}

/**
 * Records failure results for one ROF realization in overall ROF table for that week.
 * @param ut_storage_to_rof_rof_realization
 * @param ut_storage_to_rof_table
 * @param n_utilities
 * @param week
 * @param week_of_the_year
 */
void ContinuityModelROF::recordROFStorageTable(
        vector<Matrix2D<double>> &ut_storage_to_rof_rof_realization,
        vector<Matrix2D<double>> &ut_storage_to_rof_table,
        const int &n_utilities, int &week, int &week_of_the_year) {
    for (int u = 0; u < n_utilities; ++u) {
        double *rof_data = (ut_storage_to_rof_rof_realization[u] /
                            NUMBER_REALIZATIONS_ROF).
                getPointerToElement(week_of_the_year, 0);
        ut_storage_to_rof_table[u].add_to_position(
                week, 0, rof_data, NO_OF_INSURANCE_STORAGE_TIERS
        );
    }


}

/**
 * Calculate empty volume in storage-based water sources. This information is later used for updating the ROF tables.
 * @param realization_water_sources
 * @param to_full
 */
void ContinuityModelROF::calculateEmptyVolumes(
        vector<WaterSource *> &realization_water_sources, double *to_full) {
    for (int ws = 0; ws < n_sources; ++ws) {
        if (realization_water_sources[ws]->isOnline()) {
            to_full[ws] = realization_water_sources[ws]->getSupplyCapacity() -
                          realization_water_sources[ws]->getAvailableSupplyVolume();
        } else {
            to_full[ws] = 0;
        }
    }
}
