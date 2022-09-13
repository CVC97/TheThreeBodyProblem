#include <math.h>
#include <stdio.h>
#include <stdlib.h>


// Distance calculation between ri and rj 
double r(double xi, double yi, double zi, double xj, double yj, double zj) {
    return pow(pow(xi-xj, 2) + pow(yi-yj, 2) + pow(zi-zj, 2) + pow(0.5, 2), 0.5);
}


// Gravitational acceleration forced by mj on mi 
double g(double posi, double posj, double mj, double r) {
    double G = 6.67259 * pow(10, -11);
    return -G*(posi-posj)*mj/pow(r, 3);
}


// Center of mass calculation
double com(double pos1, double m1, double pos2, double m2, double pos3, double m3) {
    return (pos1 * m1 + pos2 * m2 + pos3 * m3) / (m1 + m2 + m3);
}


// Numeriacal integration
double* thethreebodyproblem(
    double m1, double x1, double y1, double z1, double v_x1, double v_y1, double v_z1,
    double m2, double x2, double y2, double z2, double v_x2, double v_y2, double v_z2,
    double m3, double x3, double y3, double z3, double v_x3, double v_y3, double v_z3,
    int n, double T
    ) {
    // Integration parameters
    double dt = T / n;
    int i, dimsize = n + 1;

    // Initial center of mass
    double cox = com(x1, m1, x2, m2, x3, m3);
    double coy = com(y1, m1, y2, m2, y3, m3);
    double coz = com(z1, m1, z2, m2, z3, m3);

    // Allocating memory for the position array and adding initial positions
    double *TBP_pos = (double*) malloc (sizeof(double) * 3 * 3 * (n+1));

    TBP_pos[0*dimsize] = x1 - cox;
    TBP_pos[1*dimsize] = y1 - coy;
    TBP_pos[2*dimsize] = z1 - coz;

    TBP_pos[3*dimsize] = x2 - cox;
    TBP_pos[4*dimsize] = y2 - coy;
    TBP_pos[5*dimsize] = z2 - coz;

    TBP_pos[6*dimsize] = x3 - cox;
    TBP_pos[7*dimsize] = y3 - coy;
    TBP_pos[8*dimsize] = z3 - coz;

    for (i = 1; i < n+1; i++) {
        // Updating distances
        double r12 = r(x1, y1, z1, x2, y2, z2);
        double r23 = r(x2, y2, z2, x3, y3, z3);
        double r31 = r(x3, y3, z3, x1, y1, z1);

        // Updating gravitational accelerations
        double g_x1 = g(x1, x2, m2, r12) + g(x1, x3, m3, r31);
        double g_y1 = g(y1, y2, m2, r12) + g(y1, y3, m3, r31);
        double g_z1 = g(z1, z2, m2, r12) + g(z1, z3, m3, r31);

        double g_x2 = g(x2, x3, m3, r23) + g(x2, x1, m1, r12);
        double g_y2 = g(y2, y3, m3, r23) + g(y2, y1, m1, r12);
        double g_z2 = g(z2, z3, m3, r23) + g(z2, z1, m1, r12);

        double g_x3 = g(x3, x1, m1, r31) + g(x3, x2, m2, r23);
        double g_y3 = g(y3, y1, m1, r31) + g(y3, y2, m2, r23);
        double g_z3 = g(z3, z1, m1, r31) + g(z3, z2, m2, r23);

        // Updating velocities
        v_x1 += g_x1 * dt;
        v_y1 += g_y1 * dt;
        v_z1 += g_z1 * dt;

        v_x2 += g_x2 * dt;
        v_y2 += g_y2 * dt;
        v_z2 += g_z2 * dt;

        v_x3 += g_x3 * dt;
        v_y3 += g_y3 * dt;
        v_z3 += g_z3 * dt;

        // Updating positions
        x1 += v_x1 * dt;
        y1 += v_y1 * dt;
        z1 += v_z1 * dt;

        x2 += v_x2 * dt;
        y2 += v_y2 * dt;
        z2 += v_z2 * dt;

        x3 += v_x3 * dt;
        y3 += v_y3 * dt;
        z3 += v_z3 * dt;

        // Updating center of masses
        cox = com(x1, m1, x2, m2, x3, m3);
        coy = com(y1, m1, y2, m2, y3, m3);
        coz = com(z1, m1, z2, m2, z3, m3);

        // Adding updated positions to the position array
        TBP_pos[0*dimsize + i] = x1 - cox;
        TBP_pos[1*dimsize + i] = y1 - coy;
        TBP_pos[2*dimsize + i] = z1 - coz;

        TBP_pos[3*dimsize + i] = x2 - cox;
        TBP_pos[4*dimsize + i] = y2 - coy;
        TBP_pos[5*dimsize + i] = z2 - coz;

        TBP_pos[6*dimsize + i] = x3 - cox;
        TBP_pos[7*dimsize + i] = y3 - coy;
        TBP_pos[8*dimsize + i] = z3 - coz;
    }
    printf("\n+++ RETURN POINTER CHECK: %p +++\n", TBP_pos);
    return TBP_pos;
}


// Freeing reserved memory
void freemem(double *array) {
    printf("+++ FREE POINTER CHECK: %p +++\n\n", array);
    free(array);
}