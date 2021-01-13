//
// Created by bernardo on 1/12/17.
//

#include <iostream>
#include "Reservoir.h"

using namespace std;

/**
 * Constructor for when Reservoir is built and operational.
 * @param name
 * @param id
 * @param min_environmental_outflow
 * @param catchments
 * @param capacity
 * @param max_treatment_capacity
 * @param source_type
 */
Reservoir::Reservoir(
        string name, const int id,
        const vector<Catchment *> &catchments, const double capacity,
        const double max_treatment_capacity,
        EvaporationSeries &evaporation_series,
        DataSeries &storage_area_curve, int source_type) :
        WaterSource(name, id, catchments, capacity, max_treatment_capacity,
                    source_type),
        storage_area_curve(storage_area_curve),
        fixed_area(false), evaporation_series(evaporation_series) {

    if (storage_area_curve.getSeries_x().back() != capacity) {
	char error[1024];
        sprintf(error,
                "Error Reservoir %d: Last storage of data series must be"
                " equal to reservoir capacity.",
                id);
        throw invalid_argument(error);
    }
}

/**
 * Constructor for when Reservoir is built and operational.
 * @param name
 * @param id
 * @param min_environmental_outflow
 * @param catchments
 * @param capacity
 * @param max_treatment_capacity
 * @param source_type
 */
Reservoir::Reservoir(
        string name, const int id,
        const vector<Catchment *> &catchments, const double capacity,
        const double max_treatment_capacity,
        EvaporationSeries &evaporation_series, double storage_area,
        int source_type) :
        WaterSource(name, id, catchments, capacity, max_treatment_capacity,
                    source_type),
        area(storage_area), fixed_area(true), evaporation_series(evaporation_series) {}

/**
 * Constructor for when Reservoir does not exist in the beginning of the simulation.
 * @param name
 * @param id
 * @param min_environmental_outflow
 * @param catchments
 * @param capacity
 * @param max_treatment_capacity
 * @param source_type
 * @param construction_rof_or_demand
 * @param construction_time_range
 * @param construction_price
 */
Reservoir::Reservoir(string name, const int id,
                     const vector<Catchment *> &catchments,
                     const double capacity,
                     const double max_treatment_capacity,
                     EvaporationSeries &evaporation_series,
                     DataSeries &storage_area_curve,
                     vector<int> construction_prerequisites,
                     const vector<double> &construction_time_range,
                     double permitting_period, Bond &bond, int source_type) :
        WaterSource(name, id, catchments, capacity, max_treatment_capacity, vector<int>(), source_type,
                    construction_time_range, permitting_period, bond),
        storage_area_curve(storage_area_curve), fixed_area(false),
        evaporation_series(evaporation_series) {

    if (storage_area_curve.getSeries_x().back() != capacity) {
	char error[1024];
    	sprintf(error, "Error Reservoir %d: Last storage of data series must be equal to reservoir capacity.", id);
        throw invalid_argument(error);
    }
}

/**
 * Constructor for when Reservoir does not exist in the beginning of the simulation.
 * @param name
 * @param id
 * @param min_environmental_outflow
 * @param catchments
 * @param capacity
 * @param max_treatment_capacity
 * @param source_type
 * @param construction_rof_or_demand
 * @param construction_time_range
 * @param construction_price
 */
Reservoir::Reservoir(string name, const int id,
                     const vector<Catchment *> &catchments,
                     const double capacity,
                     const double max_treatment_capacity,
                     EvaporationSeries &evaporation_series,
                     double storage_area,
                     vector<int> construction_prerequisites,
                     const vector<double> &construction_time_range,
                     double permitting_period,
                     Bond &bond, int source_type) :
        WaterSource(name, id, catchments, capacity, max_treatment_capacity, vector<int>(), source_type,
                    construction_time_range, permitting_period, bond),
        area(storage_area), fixed_area(true),
        evaporation_series(evaporation_series) {}

/**
 * Constructor for when Reservoir is built and operational.
 * @param name
 * @param id
 * @param min_environmental_outflow
 * @param catchments
 * @param capacity
 * @param max_treatment_capacity
 * @param source_type
 */
Reservoir::Reservoir(
        string name, const int id,
        const vector<Catchment *> &catchments, const double capacity,
        const double max_treatment_capacity,
        EvaporationSeries &evaporation_series,
        DataSeries &storage_area_curve,
        vector<double> allocated_treatment_fractions,
        vector<double> allocated_fractions,
        vector<int> utilities_with_allocations, int source_type) :
        WaterSource(name, id, catchments, capacity, max_treatment_capacity, vector<int>(), source_type,
                    allocated_treatment_fractions, allocated_fractions, utilities_with_allocations),
        storage_area_curve(storage_area_curve), fixed_area(false),
        evaporation_series(evaporation_series) {

    if (source_type != ALLOCATED_RESERVOIR)
        throw invalid_argument("Attempting to directly use reservoir "
                               "constructor auxiliary to allocated reservoir "
                               "class. You should either use the allocated "
                               "reservoir class or a different reservoir "
                               "constructor.");

    if (storage_area_curve.getSeries_x().back() != capacity) {
	char error[1024];
    	sprintf(error, "Error Reservoir %d: Last storage of data series must be equal to reservoir capacity.", id);
        throw invalid_argument(error);
    }
}

/**
 * Constructor for when Reservoir is built and operational.
 * @param name
 * @param id
 * @param min_environmental_outflow
 * @param catchments
 * @param capacity
 * @param max_treatment_capacity
 * @param source_type
 */
Reservoir::Reservoir(
        string name, const int id,
        const vector<Catchment *> &catchments, const double capacity,
        const double max_treatment_capacity,
        EvaporationSeries &evaporation_series, double storage_area,
        vector<double> allocated_treatment_fractions,
        vector<double> allocated_fractions,
        vector<int> utilities_with_allocations, int source_type) :
        WaterSource(name, id, catchments, capacity, max_treatment_capacity,
                    vector<int>(), source_type,
                    allocated_treatment_fractions, allocated_fractions,
                    utilities_with_allocations),
        area(storage_area), fixed_area(true),
        evaporation_series(evaporation_series) {

    if (source_type != ALLOCATED_RESERVOIR)
        throw invalid_argument("Attempting to directly use reservoir "
                               "constructor auxiliary to allocated reservoir "
                               "class. You should either use the allocated "
                               "reservoir class or a different reservoir "
                               "constructor.");
}

/**
 * Constructor for when Reservoir does not exist in the beginning of the simulation.
 * @param name
 * @param id
 * @param min_environmental_outflow
 * @param catchments
 * @param capacity
 * @param max_treatment_capacity
 * @param source_type
 * @param construction_rof_or_demand
 * @param construction_time_range
 * @param construction_price
 */
Reservoir::Reservoir(string name, const int id,
                     const vector<Catchment *> &catchments,
                     const double capacity,
                     const double max_treatment_capacity,
                     EvaporationSeries &evaporation_series,
                     DataSeries &storage_area_curve,
                     vector<int> construction_prerequisites,
                     vector<double> allocated_treatment_fractions,
                     vector<double> allocated_fractions,
                     vector<int> utilities_with_allocations,
                     const vector<double> &construction_time_range, double permitting_period,
                     Bond &bond, int source_type) :
        WaterSource(name, id, catchments, capacity, max_treatment_capacity, vector<int>(), source_type,
                    allocated_treatment_fractions, allocated_fractions, utilities_with_allocations,
                    construction_time_range, permitting_period, bond),
        storage_area_curve(storage_area_curve), fixed_area(false),
        evaporation_series(evaporation_series) {

    if (storage_area_curve.getSeries_x().back() != capacity) {
	char error[1024];
    	sprintf(error, "Error Reservoir %d: Last storage of data series must be equal to reservoir capacity.", id);
        throw invalid_argument(error);
    }
}

/**
 * Constructor for when Reservoir does not exist in the beginning of the simulation.
 * @param name
 * @param id
 * @param min_environmental_outflow
 * @param catchments
 * @param capacity
 * @param max_treatment_capacity
 * @param source_type
 * @param construction_rof_or_demand
 * @param construction_time_range
 * @param construction_price
 */
Reservoir::Reservoir(string name, const int id,
                     const vector<Catchment *> &catchments,
                     const double capacity,
                     const double max_treatment_capacity,
                     EvaporationSeries &evaporation_series,
                     double storage_area,
                     vector<int> construction_prerequisites,
                     vector<double> allocated_treatment_fractions,
                     vector<double> allocated_fractions,
                     vector<int> utilities_with_allocations,
                     const vector<double> &construction_time_range, double permitting_period,
                     Bond &bond, int source_type) :
        WaterSource(name, id, catchments, capacity, max_treatment_capacity, vector<int>(), source_type,
                    allocated_treatment_fractions, allocated_fractions, utilities_with_allocations,
                    construction_time_range, permitting_period, bond),
        area(storage_area), fixed_area(true),
        evaporation_series(evaporation_series) {}

/**
 * Copy constructor.
 * @param reservoir
 */
Reservoir::Reservoir(const Reservoir &reservoir) : WaterSource(reservoir),
                                                   storage_area_curve(reservoir.storage_area_curve),
                                                   area(reservoir.area),
                                                   fixed_area(reservoir.fixed_area),
                                                   evaporation_series(
                                                           reservoir.evaporation_series) {
    evaporation_series = EvaporationSeries(evaporation_series);
}

/**
 * Copy assignment operator
 * @param reservoir
 * @return
 */
Reservoir &Reservoir::operator=(const Reservoir &reservoir) {
    storage_area_curve = DataSeries(reservoir.storage_area_curve);
    evaporation_series = EvaporationSeries(reservoir.evaporation_series);
    WaterSource::operator=(reservoir);
    return *this;
}

/**
 * Destructor.
 */
Reservoir::~Reservoir() = default;

/**
 * Reservoir mass balance. Gets releases from upstream reservoirs, demands from
 * connected utilities, and combines them with its catchments inflows.
 * @param week
 * @param upstream_source_inflow
 * @param demand_outflow
 */
void Reservoir::applyContinuity(int week, double upstream_source_inflow,
                                double wastewater_inflow,
                                vector<double> &demand_outflow) {

    double total_upstream_inflow = upstream_source_inflow +
                                   wastewater_inflow;

    total_demand = 0;
    for (int i = 0; i < (int) demand_outflow.size(); ++i) {
        total_demand += demand_outflow[i];
    }

    /// Calculate total runoff inflow reaching reservoir from its watershed.
    double catchment_inflow = 0;
    for (Catchment &c : catchments) {
        catchment_inflow += c.getStreamflow(week);
    }

    /// Calculates water lost through evaporation.
    if (fixed_area)
        evaporated_volume = area * evaporation_series.getEvaporation(week);
    else {
        area = storage_area_curve.get_dependent_variable(available_volume);
        evaporated_volume = area *
                evaporation_series.getEvaporation(week);
    }

    /// Calculate new stored volume and outflow based on continuity.
    double stored_volume_new = available_volume
                               + total_upstream_inflow + catchment_inflow
                               - total_demand - min_environmental_outflow
                               - evaporated_volume;

    double outflow_new = min_environmental_outflow;


    /// Check if spillage is needed and, if so, correct stored volume and
    /// calculate spillage.
    if (stored_volume_new > capacity) {
        outflow_new += stored_volume_new - capacity;
        stored_volume_new = capacity;
    } else if (stored_volume_new < 0) {
        outflow_new = max(outflow_new + stored_volume_new, 0.);
	    stored_volume_new = 0.;
    }

    /// Update data collection variables.
    this->total_demand = total_demand + policy_added_demand;
    policy_added_demand = 0;
    available_volume = stored_volume_new;
    total_outflow = outflow_new;
    upstream_catchment_inflow = catchment_inflow;
    this->upstream_source_inflow = upstream_source_inflow;
    this->wastewater_inflow = wastewater_inflow;
}

void Reservoir::setOnline() {
    WaterSource::setOnline();

    /// start empty and gradually fill as inflows start coming in.
    available_volume = NONE;
}

void
Reservoir::setRealization(unsigned long r, const vector<double> &rdm_factors) {
    WaterSource::setRealization(r, rdm_factors);

    evaporation_series.setRealization(r, rdm_factors);
}

double Reservoir::getArea() const {
    return area;
}

const DataSeries &Reservoir::getStorageAreaCurve() const {
    return storage_area_curve;
}

EvaporationSeries Reservoir::getEvaporationSeries() const {
    return evaporation_series;
}
