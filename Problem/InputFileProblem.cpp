//
// Created by Bernardo on 12/4/2019.
//

#include <omp.h>
#include <sys/stat.h>
#include <algorithm>
// for windows mkdir
#ifdef _WIN32
#include <direct.h>
#endif

#include "InputFileProblem.h"
#include "../Simulation/Simulation.h"

#ifdef PARALLEL
#include <mpi.h>

void InputFileProblem::setProblemDefinition(BORG_Problem &problem)
{
    // The parameter bounds are the same for all formulations
    auto dec_vars_bounds = parser.getDecVarsBounds();
    auto objs_epsilons = parser.getObjsEpsilons();
    if (dec_vars_bounds.empty() || objs_epsilons.empty()) {
        throw invalid_argument("To perform an optimization run, the bounds for "
                               "the decision variables and objectives epsilons "
                               "must be specified in the input file.");
    }

    for (int i = 0; i < dec_vars_bounds.size(); ++i) {
        BORG_Problem_set_bounds(problem, i, dec_vars_bounds[i][0], dec_vars_bounds[i][1]);
    }
    for (int j = 0; j < objs_epsilons.size(); ++j) {
        BORG_Problem_set_epsilon(problem, j, objs_epsilons[j]);
    }
}
#endif

InputFileProblem::InputFileProblem(string &system_input_file) : Problem() {
    parser.preloadAndCheckInputFile(system_input_file);
}

void InputFileProblem::setRofTablesAndRunParams() {
    realizations_to_run = parser.getRealizationsToRun();
    n_realizations = parser.getNRealizations();
    n_threads = parser.getNThreads();
    n_weeks = parser.getNWeeks();
    solutions_file = parser.getSolutionsFile();
    solutions_to_run = parser.getSolutionsToRun();
    setImport_export_rof_tables(parser.getUseRofTables(),
                                parser.getRofTablesDir());
}

int InputFileProblem::functionEvaluation(double *vars, double *objs,
                                         double *consts) {

    Simulation *s = nullptr;

    parser.createSystemObjects(vars);

    // Creates simulation object depending on use (or lack thereof) ROF tables
    printf("Starting Simulation\n");
    double start_time = omp_get_wtime();
    if (import_export_rof_tables == EXPORT_ROF_TABLES) {
        s = new Simulation(parser.getWaterSources(),
                            parser.getWaterSourcesGraph(),
                            parser.getReservoirUtilityConnectivityMatrix(),
                            parser.getUtilities(),
                            parser.getDroughtMitigationPolicy(),
                            parser.getReservoirControlRules(),
                            parser.getRdmUtilities(),
                            parser.getRdmWaterSources(),
                            parser.getRdmDmp(),
                            parser.getNWeeks(),
                            parser.getRealizationsToRun(),
                            parser.getRofTablesDir());
        this->master_data_collector = s->runFullSimulation(n_threads, vars);
    } else if (import_export_rof_tables == IMPORT_ROF_TABLES) {
        s = new Simulation(parser.getWaterSources(),
                            parser.getWaterSourcesGraph(),
                            parser.getReservoirUtilityConnectivityMatrix(),
                            parser.getUtilities(),
                            parser.getDroughtMitigationPolicy(),
                            parser.getReservoirControlRules(),
                            parser.getRdmUtilities(),
                            parser.getRdmWaterSources(),
                            parser.getRdmDmp(),
                            parser.getNWeeks(),
                            parser.getRealizationsToRun(),
                            rof_tables,
                            parser.getTableStorageShift(),
                            rof_tables_directory);
        this->master_data_collector = s->runFullSimulation(n_threads, vars);
    } else {
        s = new Simulation(parser.getWaterSources(),
                            parser.getWaterSourcesGraph(),
                            parser.getReservoirUtilityConnectivityMatrix(),
                            parser.getUtilities(),
                            parser.getDroughtMitigationPolicy(),
                            parser.getReservoirControlRules(),
                            parser.getRdmUtilities(),
                            parser.getRdmWaterSources(),
                            parser.getRdmDmp(),
                            parser.getNWeeks(),
                            parser.getRealizationsToRun());
        this->master_data_collector = s->runFullSimulation(n_threads, vars);
    }

    double end_time = omp_get_wtime();
    printf(" Function evaluation time: %f\n", end_time - start_time);

    // Calculate objectives and store them in Borg decision variables array.
    if (parser.isOptimize()) {
#ifdef  PARALLEL
        //    printf("Starting to calculate objectives.\n");
            if (import_export_rof_tables != EXPORT_ROF_TABLES) {
                objectives = calculateAndPrintObjectives(false);

            unsigned long n_utilities = parser.getUtilities().size();

            memcpy(objs, objectives.data(), sizeof(double) * 5);
            objs[0] = -objs[0];
            for (int i = 1; i < n_utilities; ++i) {
                    objs[0] = max(objs[0], - objectives[0 + 5 * i]);
                    objs[1] = max(objs[1], objectives[1 + 5 * i]);
                    objs[2] = max(objs[2], objectives[2 + 5 * i]);
                    objs[3] = max(objs[3], objectives[3 + 5 * i]);
                    objs[4] = max(objs[4], objectives[4 + 5 * i]);
                }

                for (int i = 0; i < parser.getNObjectives(); ++i) {
                    if (isnan(objs[i])) {
                        for (int j = 0; j < parser.getNObjectives(); ++j) {
                            objs[i] = 1e5;
                        }
                        break;
                    }
                }
                printf("Objectives calculated.\n");
            }

            delete s;
            s = nullptr;
#else
        throw runtime_error(
                "This version of WaterPaths was not compiled with Borg.\n");
//    } catch (const std::exception& e) {
//        simulationExceptionHander(e, s, objs, vars);
//	return 1;
//    }
#endif
    }
//    } else {
//        setSol_number(sol_number);
//        calculateAndPrintObjectives(true);
//    }

    parser.clearParsers();
    printf("Function evaluation complete\n");
    return 0;
}

const vector<vector<double>> &InputFileProblem::getSolutionsDecvars() const {
    return parser.getSolutionsDecvars();
}

void InputFileProblem::runSimulation() {
    n_sets = parser.getNBootstrapSamples();
    n_bs_samples = parser.getBootstrapSampleSize();
    plotting = parser.isPrintTimeSeries();
    solutions_decvars = parser.getSolutionsDecvars();
    setIODirectory(parser.getOutputDir());

    if (solutions_decvars.size() > 1) {
        ofstream objs_file = createOutputFile();
        for (int s = 0; s < solutions_to_run.size(); ++s) {
            auto dvs = solutions_decvars[s];
            functionEvaluation(dvs.data(), nullptr, nullptr);
            setSol_number(solutions_to_run[s]);
            vector<double> objectives = calculateAndPrintObjectives(true);
            printTimeSeriesAndPathways(plotting);
            destroyDataCollector();
            printObjsInLineInFile(objs_file, objectives);

            if (n_sets != NON_INITIALIZED && n_bs_samples != NON_INITIALIZED) {
                auto sols = parser.getSolutionsToRun();
                runBootstrapRealizationThinning(
                        (sols.empty() ? -1 : (int) sols[0]), n_sets, n_bs_samples,
                        (int) n_threads, bs_realizations);
            }
        }
        objs_file.close();
    } else {
        if (solutions_decvars.size() == 1) {
            functionEvaluation(solutions_decvars[0].data(), nullptr, nullptr);
        } else {
            functionEvaluation(nullptr, nullptr, nullptr);
        }

        setSol_number(NONE);
        calculateAndPrintObjectives(true);
        printTimeSeriesAndPathways(plotting);
        if (n_sets != NON_INITIALIZED && n_bs_samples != NON_INITIALIZED) {
            auto sols = parser.getSolutionsToRun();
            runBootstrapRealizationThinning(
                    (sols.empty() ? -1 : (int) sols[0]), n_sets, n_bs_samples,
                    (int) n_threads, bs_realizations);
        }
        destroyDataCollector();
    }
}

#pragma GCC optimize("O0")
ofstream InputFileProblem::createOutputFile() const {
    string output_dir = system_io + "output" + BAR;
    if (mkdir(output_dir.c_str(), 700) != 0) {
        ofstream objs_file;
        string sol_numbers;
        string rdm_name = (rdm_no == NON_INITIALIZED ? "" : "_RDM" + to_string(rdm_no));

        if (solutions_to_run.empty()) {
            throw invalid_argument("Solutions file was specified in the input "
                                   "file but no solution number was. Values "
                                   "need to be provided to either "
                                   "solutions_to_run or "
                                   "solutions_to_run_range.");
        } else if(solutions_to_run.size() > 1) {
                sol_numbers = to_string(solutions_to_run[0]);
        } else if (is_sorted(solutions_to_run.begin(), solutions_to_run.end()) &&
                solutions_to_run[0] - solutions_to_run.back() ==
                solutions_to_run.size()) {
            sol_numbers = to_string(solutions_to_run[0]) +
            "_to_" + to_string(solutions_to_run.back());
        } else {
            for (auto s : solutions_to_run) {
                sol_numbers += to_string(s) + "_";
            }
            sol_numbers.pop_back();
        }
        string file_name = system_io + "output" + BAR + "Objectives" +
                rdm_name + "_sols" + sol_numbers + ".csv";
        objs_file.open(file_name);
        printf("Objectives will be printed to file %s\n",
               file_name.c_str());
        return objs_file;
    } else {
        throw runtime_error("Cannot create directory " + output_dir);
    }
}

void InputFileProblem::printObjsInLineInFile(ofstream &objs_file,
                                             const vector<double> &objectives) const {
    string line;
    for (const double &o : objectives) {
        line += to_string(o) + ",";
    }
    line.pop_back();
    objs_file << line << endl;
}

bool InputFileProblem::isOptimize() const {
    return parser.isOptimize();
}

int InputFileProblem::getNFunctionEvals() const {
    return parser.getNFunctionEvals();
}

int InputFileProblem::getRuntimeOutputInterval() const {
    return parser.getRuntimeOutputInterval();
}

unsigned long InputFileProblem::getNDecVars() const {
    return parser.getNDecVars();
}

unsigned long InputFileProblem::getNObjectives() const {
    return parser.getNObjectives();
}

int InputFileProblem::getSeed() const {
    return parser.getSeed();
}

string InputFileProblem::getOutputDir() const {
    return parser.getOutputDir();
}
