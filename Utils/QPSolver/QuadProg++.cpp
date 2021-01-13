/* 
File $Id: QuadProg++.cc 232 2007-06-21 12:29:00Z digasper $
 
 Author: Luca Di Gaspero
 DIEGM - University of Udine, Italy
 luca.digaspero@uniud.it
 http://www.diegm.uniud.it/digaspero/
 
 This software may be modified and distributed under the terms
 of the MIT license.  See the LICENSE file for details.

 Modified by Bernardo Trindade on 04/2017
 */

#include <iostream>
#include <algorithm>
#include <sstream>
#include "QuadProg++.h"

// Utility functions for updating some data needed by the solution method 
void compute_d(Vector<double> &d, const Matrix<double> &J, const Vector<double> &np);

void update_z(Vector<double> &z, const Matrix<double> &J, const Vector<double> &d, int iq);

void update_r(const Matrix<double> &R, Vector<double> &r, const Vector<double> &d, int iq);

bool add_constraint(Matrix<double> &R, Matrix<double> &J, Vector<double> &d, int &iq, double &rnorm);

void delete_constraint(Matrix<double> &R, Matrix<double> &J, Vector<int> &A, Vector<double> &u, int n, int p, int &iq,
                       int l);

// Utility functions for computing the Cholesky decomposition and solving
// linear systems
void cholesky_decomposition(Matrix<double> &A);

void cholesky_solve(const Matrix<double> &L, Vector<double> &x, const Vector<double> &b);

void forward_elimination(const Matrix<double> &L, Vector<double> &y, const Vector<double> &b);

void backward_elimination(const Matrix<double> &U, Vector<double> &x, const Vector<double> &y);

// Utility functions for computing the scalar product and the euclidean 
// distance between two numbers
double scalar_product(const Vector<double> &x, const Vector<double> &y);

double distance(double a, double b);

// The Solving function, implementing the Goldfarb-Idnani method
double solve_quadprog(Matrix<double> &G, Vector<double> &g0,
                      const Matrix<double> &CE, const Vector<double> &ce0,
                      const Matrix<double> &CI, const Vector<double> &ci0,
                      Vector<double> &x) {
    std::ostringstream msg;

    unsigned int n = G.ncols(), p = CE.ncols(), m = CI.ncols();
    if (G.nrows() != n) {
        msg << "The matrix H is not a squared matrix (" << G.nrows() << " allocations_aux " << G.ncols() << ")";
        throw std::logic_error(msg.str());
    }
    if (CE.nrows() != n) {
        msg << "The matrix Aeq is incompatible (incorrect number of rows " << CE.nrows() << " , expecting " << n << ")";
        throw std::logic_error(msg.str());
    }
    if (ce0.size() != p) {
        msg << "The vector beq is incompatible (incorrect dimension " << ce0.size() << ", expecting " << p << ")";
        throw std::logic_error(msg.str());
    }
    if (CI.nrows() != n) {
        msg << "The matrix A is incompatible (incorrect number of rows " << CI.nrows() << " , expecting " << n << ")";
        throw std::logic_error(msg.str());
    }
    if (ci0.size() != m) {
        msg << "The vector b is incompatible (incorrect dimension " << ci0.size() << ", expecting " << m << ")";
        throw std::logic_error(msg.str());
    }
    x.resize(n);
    register int i, j, k, l; /* indices */
    int ip; // this is the index of the constraint to be added to the active set
    Matrix<double> R(n, n);
    Matrix<double> J(n, n);
    Vector<double> s(m + p);
    Vector<double> z(n);
    Vector<double> r(m + p);
    Vector<double> d(n);
    Vector<double> np(n);
    Vector<double> u(m + p);
    Vector<double> x_old(n);
    Vector<double> u_old(m + p);
    double f_value, psi, c1, c2, sum, ss, R_norm;
    double inf;
    inf = std::numeric_limits<double>::infinity();
    double t, t1, t2; /* t is the step lenght, which is the minimum of the partial step length t1
    * and the full step length t2 */
    Vector<int> A(m + p), A_old(m + p), iai(m + p);
    int iq, iter = 0;
    Vector<bool> iaexcl(m + p);

    /* p is the number of equality constraints */
    /* m is the number of inequality constraints */
    /* size of the active set A (containing the indices of the active constraints) */
#ifdef TRACE_SOLVER
    std::cout << std::endl << "Starting solve_quadprog" << std::endl;
    print_matrix("H", H);
    print_vector("f", f);
    print_matrix("Aeq", Aeq);
    print_vector("beq", beq);
    print_matrix("A", A);
    print_vector("b", b);
#endif

    /*
     * Preprocessing phase
     */

    /* compute the trace of the original matrix H */
    c1 = 0.0;
    for (i = 0; i < (int) n; i++) {
        c1 += G[i][i];
    }
    /* decompose the matrix H in the form L^T L */
    cholesky_decomposition(G);
#ifdef TRACE_SOLVER
    print_matrix("H", H);
#endif
    /* initialize the matrix R */
    for (i = 0; i < (int) n; i++) {
        d[i] = 0.0;
        for (j = 0; j < (int) n; j++)
            R[i][j] = 0.0;
    }
    R_norm = 1.0; /* this variable will hold the norm of the matrix R */

    /* compute the inverse of the factorized matrix H^-1, this is the initial value for H */
    c2 = 0.0;
    for (i = 0; i < (int) n; i++) {
        d[i] = 1.0;
        forward_elimination(G, z, d);
        for (j = 0; j < (int) n; j++)
            J[i][j] = z[j];
        c2 += z[i];
        d[i] = 0.0;
    }
#ifdef TRACE_SOLVER
    print_matrix("J", J);
#endif

    /* c1 * c2 is an estimate for cond(H) */

    /*
      * Find the unconstrained minimizer of the quadratic form 0.5 * allocations_aux H allocations_aux + f allocations_aux
     * this is a feasible point in the dual space
     * allocations_aux = H^-1 * f
     */
    cholesky_solve(G, x, g0);
    for (i = 0; i < (int) n; i++)
        x[i] = -x[i];
    /* and compute the current solution value */
    f_value = 0.5 * scalar_product(g0, x);
#ifdef TRACE_SOLVER
    std::cout << "Unconstrained solution: " << f_value << std::endl;
    print_vector("allocations_aux", allocations_aux);
#endif

    /* Add equality constraints to the working set A */
    iq = 0;
    for (i = 0; i < (int) p; i++) {
        for (j = 0; j < (int) n; j++)
            np[j] = CE[j][i];
        compute_d(d, J, np);
        update_z(z, J, d, iq);
        update_r(R, r, d, iq);
#ifdef TRACE_SOLVER
        print_matrix("R", R, n, iq);
        print_vector("z", z);
        print_vector("r", r, iq);
        print_vector("d", d);
#endif

        /* compute full step length t2: i.e., the minimum step in primal space s.t. the contraint
          becomes feasible */
        t2 = 0.0;
        if (fabs(scalar_product(z, z)) > std::numeric_limits<double>::epsilon()) // i.e. z != 0
            t2 = (-scalar_product(np, x) - ce0[i]) / scalar_product(z, np);

        /* set allocations_aux = allocations_aux + t2 * z */
        for (k = 0; k < (int) n; k++)
            x[k] += t2 * z[k];

        /* set u = u+ */
        u[iq] = t2;
        for (k = 0; k < iq; k++)
            u[k] -= t2 * r[k];

        /* compute the new solution value */
        f_value += 0.5 * (t2 * t2) * scalar_product(z, np);
        A[i] = -i - 1;

        if (!add_constraint(R, J, d, iq, R_norm)) {
            // Equality constraints are linearly dependent
            throw std::runtime_error("Constraints are linearly dependent");
        }
    }

    /* set iai = K \ A */
    for (i = 0; i < (int) m; i++)
        iai[i] = i;

    l1:
    iter++;
#ifdef TRACE_SOLVER
    print_vector("allocations_aux", allocations_aux);
#endif
    /* step 1: choose a violated constraint */
    for (i = p; i < iq; i++) {
        ip = A[i];
        iai[ip] = -1;
    }

    /* compute s[allocations_aux] = ci^T * allocations_aux + b for all elements of K \ A */
    ss = 0.0;
    psi = 0.0; /* this value will contain the sum of all infeasibilities */
    ip = 0; /* ip will be the index of the chosen violated constraint */
    for (i = 0; i < (int) m; i++) {
        iaexcl[i] = true;
        sum = 0.0;
        for (j = 0; j < (int) n; j++)
            sum += CI[j][i] * x[j];
        sum += ci0[i];
        s[i] = sum;
        psi += std::min(0.0, sum);
    }
#ifdef TRACE_SOLVER
    print_vector("s", s, m);
#endif


    if (fabs(psi) <= m * std::numeric_limits<double>::epsilon() * c1 * c2 *
                             100.0) {
        /* numerically there are not infeasibilities anymore */
        return f_value;
    }

    /* save old values for u and A */
    for (i = 0; i < iq; i++) {
        u_old[i] = u[i];
        A_old[i] = A[i];
    }
    /* and for allocations_aux */
    for (i = 0; i < (int) n; i++)
        x_old[i] = x[i];

    l2: /* Step 2: check for feasibility and determine a new S-pair */
    for (i = 0; i < (int) m; i++) {
        if (s[i] < ss && iai[i] != -1 && iaexcl[i]) {
            ss = s[i];
            ip = i;
        }
    }
    if (ss >= 0.0) {
        return f_value;
    }

    /* set np = n[ip] */
    for (i = 0; i < (int) n; i++)
        np[i] = CI[i][ip];
    /* set u = [u 0]^T */
    u[iq] = 0.0;
    /* add ip to the active set A */
    A[iq] = ip;

#ifdef TRACE_SOLVER
    std::cout << "Trying with constraint " << ip << std::endl;
    print_vector("np", np);
#endif

    l2a:/* Step 2a: determine step direction */
    /* compute z = H np: the step direction in the primal space (through J, see the paper) */
    compute_d(d, J, np);
    update_z(z, J, d, iq);
    /* compute N* np (if q > 0): the negative of the step direction in the dual space */
    update_r(R, r, d, iq);
#ifdef TRACE_SOLVER
    std::cout << "Step direction z" << std::endl;
    print_vector("z", z);
    print_vector("r", r, iq + 1);
    print_vector("u", u, iq + 1);
    print_vector("d", d);
    print_vector("A", A, iq + 1);
#endif

    /* Step 2b: compute step length */
    l = 0;
    /* Compute t1: partial step length (maximum step in dual space without violating dual feasibility */
    t1 = inf; /* +inf */
    /* find the index l s.t. it reaches the minimum of u+[allocations_aux] / r */
    for (k = p; k < iq; k++) {
        if (r[k] > 0.0) {
            if (u[k] / r[k] < t1) {
                t1 = u[k] / r[k];
                l = A[k];
            }
        }
    }
    /* Compute t2: full step length (minimum step in primal space such that the constraint ip becomes feasible */
    if (fabs(scalar_product(z, z)) > std::numeric_limits<double>::epsilon()) // i.e. z != 0
    {
        t2 = -s[ip] / scalar_product(z, np);
        if (t2 < 0) // patch suggested by Takano Akio for handling numerical inconsistencies
            t2 = inf;
    } else
        t2 = inf; /* +inf */

    /* the step is chosen as the minimum of t1 and t2 */
    t = std::min(t1, t2);
#ifdef TRACE_SOLVER
    std::cout << "Step sizes: " << t << " (t1 = " << t1 << ", t2 = " << t2 << ") ";
#endif

    /* Step 2c: determine new S-pair and take step: */

    /* case (i): no step in primal or dual space */
    if (t >= inf) {
        /* QPP is infeasible */
        // FIXME: unbounded to raise
        return inf;
    }
    /* case (ii): step in dual space */
    if (t2 >= inf) {
        /* set u = u +  t * [-r 1] and drop constraint l from the active set A */
        for (k = 0; k < iq; k++)
            u[k] -= t * r[k];
        u[iq] += t;
        iai[l] = l;
        delete_constraint(R, J, A, u, n, p, iq, l);
#ifdef TRACE_SOLVER
        std::cout << " in dual space: "
          << f_value << std::endl;
        print_vector("allocations_aux", allocations_aux);
        print_vector("z", z);
        print_vector("A", A, iq + 1);
#endif
        goto l2a;
    }

    /* case (iii): step in primal and dual space */

    /* set allocations_aux = allocations_aux + t * z */
    for (k = 0; k < (int) n; k++)
        x[k] += t * z[k];
    /* update the solution value */
    f_value += t * scalar_product(z, np) * (0.5 * t + u[iq]);
    /* u = u + t * [-r 1] */
    for (k = 0; k < iq; k++)
        u[k] -= t * r[k];
    u[iq] += t;
#ifdef TRACE_SOLVER
    std::cout << " in both spaces: "
      << f_value << std::endl;
    print_vector("allocations_aux", allocations_aux);
    print_vector("u", u, iq + 1);
    print_vector("r", r, iq + 1);
    print_vector("A", A, iq + 1);
#endif

    if (fabs(t - t2) < std::numeric_limits<double>::epsilon()) {
#ifdef TRACE_SOLVER
        std::cout << "Full step has taken " << t << std::endl;
        print_vector("allocations_aux", allocations_aux);
#endif
        /* full step has taken */
        /* add constraint ip to the active set*/
        if (!add_constraint(R, J, d, iq, R_norm)) {
            iaexcl[ip] = false;
            delete_constraint(R, J, A, u, n, p, iq, ip);
#ifdef TRACE_SOLVER
            print_matrix("R", R);
            print_vector("A", A, iq);
                  print_vector("iai", iai);
#endif
            for (i = 0; i < (int) m; i++)
                iai[i] = i;
            for (i = p; i < iq; i++) {
                A[i] = A_old[i];
                u[i] = u_old[i];
                iai[A[i]] = -1;
            }
            for (i = 0; i < (int) n; i++)
                x[i] = x_old[i];
            goto l2; /* go to step 2 */
        } else
            iai[ip] = -1;
#ifdef TRACE_SOLVER
        print_matrix("R", R);
        print_vector("A", A, iq);
            print_vector("iai", iai);
#endif
        goto l1;
    }

    /* a patial step has taken */
#ifdef TRACE_SOLVER
    std::cout << "Partial step has taken " << t << std::endl;
    print_vector("allocations_aux", allocations_aux);
#endif
    /* drop constraint l */
    iai[l] = l;
    delete_constraint(R, J, A, u, n, p, iq, l);
#ifdef TRACE_SOLVER
    print_matrix("R", R);
    print_vector("A", A, iq);
#endif

    /* update s[ip] = A * allocations_aux + b */
    sum = 0.0;
    for (k = 0; k < (int) n; k++)
        sum += CI[k][ip] * x[k];
    s[ip] = sum + ci0[ip];

#ifdef TRACE_SOLVER
    print_vector("s", s, m);
#endif
    goto l2a;
}

/**
 * Wrapper for Matlab quadprog input format.
 * @param G
 * @param g0
 * @param CE
 * @param ce0
 * @param CI
 * @param ci0
 * @param lb
 * @param ub
 * @param x
 */
void solve_quadprog_matlab_syntax(Matrix<double> &G, Vector<double> &g0,
                                    const Matrix<double> &CE, const Vector<double> &ce0,
                                    const Matrix<double> &CI, const Vector<double> &ci0,
                                    const Vector<double> &lb, const Vector<double> &ub,
                                    Vector<double> &x) {
    Matrix<double> CE_T;
    Matrix<double> expanded_CI;
    CE_T.resize(0, CE.ncols(), CE.nrows());
    expanded_CI.resize(0, CI.nrows() + lb.size() + ub.size(), CI.ncols() + lb.size());

    /// Transpose CE.
    for (unsigned int i = 0; i < CE.nrows(); ++i) {
        for (unsigned int j = 0; j < CE.ncols(); ++j) {
            CE_T[j][i] = CE[i][j];
        }
    }

    /// Reverse signs of ce0 and ci0.
    Vector<double> ce0_inv;
    ce0_inv.resize(0, ce0.size());
    for (unsigned int i = 0; i < ce0.size(); ++i) {
        ce0_inv[i] = -ce0[i];
    }
    /// Expand ci0 to include the bounds.
    Vector<double> ci0_inv;
    ci0_inv.resize((0, ci0.size() + lb.size() + ub.size()));
    for (unsigned int i = 0; i < ci0.size(); ++i) {
        ci0_inv[i] = -ci0[i];
    }

    /// Expand CI so to include the bounds.
    for (unsigned int i = 0; i < CI.nrows(); ++i) {
        for (unsigned int j = 0; j < CI.ncols(); ++j) {
            expanded_CI[i][j] = CI[i][j];
        }
    }

    /// Including bounds in expanded_CI and ci_inv
    for (unsigned int i = CI.nrows(); i < CI.nrows() + lb.size(); ++i) {
        expanded_CI[i][i - CI.nrows()] = 1;
        expanded_CI[i+lb.size()][i - CI.nrows()] = -1;
    }

    /// Transpose expanded_CI
    Matrix<double> expanded_CI_inv;
    expanded_CI_inv.resize(0, expanded_CI.ncols(), expanded_CI.nrows());
    for (unsigned int i = 0; i < expanded_CI.nrows(); ++i) {
        for (unsigned int j = 0; j < expanded_CI.ncols(); ++j) {
            expanded_CI_inv[j][i] = expanded_CI[i][j];
        }
    }

    for (unsigned int i = CI.nrows(); i < CI.nrows() + lb.size(); ++i) {
        ci0_inv[i] = -lb[i - CI.nrows()];
        ci0_inv[i + lb.size()] = ub[i - CI.nrows()];
    }

//    print_matrix("H", G);
//    print_vector("f", g0);
//    print_matrix("Aeq", CE_T);
//    print_vector("beq", ce0_inv);
//    print_matrix("A", expanded_CI_inv);
//    print_vector("b", ci0_inv);

    solve_quadprog(G, g0, CE_T, ce0_inv, expanded_CI_inv, ci0_inv, x);

    for (unsigned int i = 0; i < x.size(); ++i) {
        if (std::abs(x[i]) < 1e-12) x[i] = 0;
    }
}


inline void compute_d(Vector<double> &d, const Matrix<double> &J, const Vector<double> &np) {
    register int i, j, n = (int) d.size();
    register double sum;

    /* compute d = H^T * np */
    for (i = 0; i < n; i++) {
        sum = 0.0;
        for (j = 0; j < n; j++)
            sum += J[j][i] * np[j];
        d[i] = sum;
    }
}

inline void update_z(Vector<double> &z, const Matrix<double> &J, const Vector<double> &d, int iq) {
    register int i, j, n = (int) z.size();

    /* setting of z = H * d */
    for (i = 0; i < n; i++) {
        z[i] = 0.0;
        for (j = iq; j < n; j++)
            z[i] += J[i][j] * d[j];
    }
}

inline void update_r(const Matrix<double> &R, Vector<double> &r, const Vector<double> &d, int iq) {
    register int i, j;
    register double sum;

    /* setting of r = R^-1 d */
    for (i = iq - 1; i >= 0; i--) {
        sum = 0.0;
        for (j = i + 1; j < iq; j++)
            sum += R[i][j] * r[j];
        r[i] = (d[i] - sum) / R[i][i];
    }
}

bool add_constraint(Matrix<double> &R, Matrix<double> &J, Vector<double> &d, int &iq, double &R_norm) {
    int n = d.size();
#ifdef TRACE_SOLVER
    std::cout << "Add constraint " << iq << '/';
#endif
    register int i, j, k;
    double cc, ss, h, t1, t2, xny;

    /* we have to find the Givens rotation which will reduce the element
      d[j] to zero.
      if it is already zero we don't have to do anything, except of
      decreasing j */
    for (j = n - 1; j >= iq + 1; j--) {
        /* The Givens rotation is done with the matrix (cc cs, cs -cc).
        If cc is one, then element (j) of d is zero compared with element
        (j - 1). Hence we don't have to do anything.
        If cc is zero, then we just have to switch column (j) and column (j - 1)
        of J. Since we only switch columns in J, we have to be careful how we
        update d depending on the sign of gs.
        Otherwise we have to apply the Givens rotation to these columns.
        The i - 1 element of d has to be updated to h. */
        cc = d[j - 1];
        ss = d[j];
        h = distance(cc, ss);
        if (fabs(h) < std::numeric_limits<double>::epsilon()) // h == 0
            continue;
        d[j] = 0.0;
        ss = ss / h;
        cc = cc / h;
        if (cc < 0.0) {
            cc = -cc;
            ss = -ss;
            d[j - 1] = -h;
        } else
            d[j - 1] = h;
        xny = ss / (1.0 + cc);
        for (k = 0; k < n; k++) {
            t1 = J[k][j - 1];
            t2 = J[k][j];
            J[k][j - 1] = t1 * cc + t2 * ss;
            J[k][j] = xny * (t1 + J[k][j - 1]) - t2;
        }
    }
    /* update the number of constraints added*/
    iq++;
    /* To update R we have to put the iq components of the d vector
      into column iq - 1 of R
      */
    for (i = 0; i < iq; i++)
        R[i][iq - 1] = d[i];
#ifdef TRACE_SOLVER
    std::cout << iq << std::endl;
    print_matrix("R", R, iq, iq);
    print_matrix("J", J);
    print_vector("d", d, iq);
#endif

    if (fabs(d[iq - 1]) <= std::numeric_limits<double>::epsilon() * R_norm) {
        // problem degenerate
        return false;
    }
    R_norm = std::max<double>(R_norm, fabs(d[iq - 1]));
    return true;
}

void delete_constraint(Matrix<double> &R, Matrix<double> &J, Vector<int> &A, Vector<double> &u, int n, int p, int &iq,
                       int l) {
#ifdef TRACE_SOLVER
    std::cout << "Delete constraint " << l << ' ' << iq;
#endif
    register int i, j, k, qq = -1; // just to prevent warnings from smart compilers
    double cc, ss, h, xny, t1, t2;

    /* Find the index qq for active constraint l to be removed */
    for (i = p; i < iq; i++)
        if (A[i] == l) {
            qq = i;
            break;
        }

    /* remove the constraint from the active set and the duals */
    for (i = qq; i < iq - 1; i++) {
        A[i] = A[i + 1];
        u[i] = u[i + 1];
        for (j = 0; j < n; j++)
            R[j][i] = R[j][i + 1];
    }

    A[iq - 1] = A[iq];
    u[iq - 1] = u[iq];
    A[iq] = 0;
    u[iq] = 0.0;
    for (j = 0; j < iq; j++)
        R[j][iq - 1] = 0.0;
    /* constraint has been fully removed */
    iq--;
#ifdef TRACE_SOLVER
    std::cout << '/' << iq << std::endl;
#endif

    if (iq == 0)
        return;

    for (j = qq; j < iq; j++) {
        cc = R[j][j];
        ss = R[j + 1][j];
        h = distance(cc, ss);
        if (fabs(h) < std::numeric_limits<double>::epsilon()) // h == 0
            continue;
        cc = cc / h;
        ss = ss / h;
        R[j + 1][j] = 0.0;
        if (cc < 0.0) {
            R[j][j] = -h;
            cc = -cc;
            ss = -ss;
        } else
            R[j][j] = h;

        xny = ss / (1.0 + cc);
        for (k = j + 1; k < iq; k++) {
            t1 = R[j][k];
            t2 = R[j + 1][k];
            R[j][k] = t1 * cc + t2 * ss;
            R[j + 1][k] = xny * (t1 + R[j][k]) - t2;
        }
        for (k = 0; k < n; k++) {
            t1 = J[k][j];
            t2 = J[k][j + 1];
            J[k][j] = t1 * cc + t2 * ss;
            J[k][j + 1] = xny * (J[k][j] + t1) - t2;
        }
    }
}

inline double distance(double a, double b) {
    register double a1, b1, t;
    a1 = fabs(a);
    b1 = fabs(b);
    if (a1 > b1) {
        t = (b1 / a1);
        return a1 * sqrt(1.0 + t * t);
    } else if (b1 > a1) {
        t = (a1 / b1);
        return b1 * sqrt(1.0 + t * t);
    }
    return a1 * sqrt(2.0);
}


inline double scalar_product(const Vector<double> &x, const Vector<double> &y) {
    register int i, n = x.size();
    register double sum;

    sum = 0.0;
    for (i = 0; i < n; i++)
        sum += x[i] * y[i];
    return sum;
}

void cholesky_decomposition(Matrix<double> &A) {
    register int i, j, k, n = A.nrows();
    register double sum;

    for (i = 0; i < n; i++) {
        for (j = i; j < n; j++) {
            sum = A[i][j];
            for (k = i - 1; k >= 0; k--)
                sum -= A[i][k] * A[j][k];
            if (i == j) {
                if (sum <= 0.0) {
                    std::ostringstream os;
                    // raise error
                    print_matrix((char *) "A", A);
                    os << "Error in cholesky decomposition, sum: " << sum;
                    throw std::logic_error(os.str());
                }
                A[i][i] = sqrt(sum);
            } else
                A[j][i] = sum / A[i][i];
        }
        for (k = i + 1; k < n; k++)
            A[i][k] = A[k][i];
    }
}

void cholesky_solve(const Matrix<double> &L, Vector<double> &x, const Vector<double> &b) {
    int n = L.nrows();
    Vector<double> y((unsigned int) n);

    /* Solve L * y = b */
    forward_elimination(L, y, b);
    /* Solve L^T * allocations_aux = y */
    backward_elimination(L, x, y);
}

inline void forward_elimination(const Matrix<double> &L, Vector<double> &y, const Vector<double> &b) {
    register int i, j, n = L.nrows();

    y[0] = b[0] / L[0][0];
    for (i = 1; i < n; i++) {
        y[i] = b[i];
        for (j = 0; j < i; j++)
            y[i] -= L[i][j] * y[j];
        y[i] = y[i] / L[i][i];
    }
}

inline void backward_elimination(const Matrix<double> &U, Vector<double> &x, const Vector<double> &y) {
    register int i, j, n = U.nrows();

    x[n - 1] = y[n - 1] / U[n - 1][n - 1];
    for (i = n - 2; i >= 0; i--) {
        x[i] = y[i];
        for (j = i + 1; j < n; j++)
            x[i] -= U[i][j] * x[j];
        x[i] = x[i] / U[i][i];
    }
}

void print_matrix(char *name, const Matrix<double> &A, int n, int m) {
    std::ostringstream s;
    std::string t;
    if (n == -1)
        n = A.nrows();
    if (m == -1)
        m = A.ncols();

    s << name << ": " << std::endl;
    for (int i = 0; i < n; i++) {
        s << " ";
        for (int j = 0; j < m; j++)
            s << A[i][j] << ", ";
        s << std::endl;
    }
    t = s.str();
    t = t.substr(0, t.size() - 3); // To remove the trailing space, comma and newline

    std::cout << t << std::endl;
}

void print_vector(char *name, const Vector<double> &v, int n) {
    std::ostringstream s;
    std::string t;
    if (n == -1)
        n = v.size();

    s << name << ": " << std::endl << " ";
    for (int i = 0; i < n; i++) {
        s << v[i] << ", ";
    }
    t = s.str();
    t = t.substr(0, t.size() - 2); // To remove the trailing space and comma

    std::cout << t << std::endl;
}
