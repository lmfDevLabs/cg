class KochanekBartelsSpline:
    def __init__(self, control_points, T=0, C=0, B=0):
        self.control_points = control_points
        self.T = T
        self.C = C
        self.B = B

    def compute_tangent(self, pm1, p0, p1):
        d0 = ((1 - self.T) * (1 + self.C) * (1 + self.B)) / 2
        d1 = ((1 - self.T) * (1 - self.C) * (1 - self.B)) / 2
        return [d0 * (p1[i] - p0[i]) + d1 * (p0[i] - pm1[i]) for i in range(len(p0))]

    def interpolate(self, p0, p1, m0, m1, t):
        h00 = 2 * t**3 - 3 * t**2 + 1
        h10 = t**3 - 2 * t**2 + t
        h01 = -2 * t**3 + 3 * t**2
        h11 = t**3 - t**2
        return [h00 * p0[i] + h10 * m0[i] + h01 * p1[i] + h11 * m1[i] for i in range(len(p0))]

    def compute_curve(self, num_points=10):
        curve = []
        for i in range(len(self.control_points) - 1):
            p0 = self.control_points[i]
            p1 = self.control_points[i + 1]
            if i == 0:
                pm1 = p0
            else:
                pm1 = self.control_points[i - 1]
            if i + 2 >= len(self.control_points):
                p2 = p1
            else:
                p2 = self.control_points[i + 2]

            m0 = self.compute_tangent(pm1, p0, p1)
            m1 = self.compute_tangent(p0, p1, p2)

            for j in range(num_points):
                t = j / float(num_points - 1)
                curve.append(self.interpolate(p0, p1, m0, m1, t))
        return curve
