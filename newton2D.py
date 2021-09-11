# each body wil have to check the force of gravity from all other bodies
# should force be represented [fx, fy] or [phi, F]
# can either calculate the angle of gravity and transform acceleration
# or just calculate unit vector of distance and multiply by acceleration
# gravity is calculated assuming point mass
# gravity tells us which way matter accelerates in the absense of external forces
#   i.e, compute gravity-accel for each body and use this to compute next position
# what about the fact that if far away planet moves it's impact on other planets due to gravity is limited by speed of light

# F1 = F2 = G * (m1*m2) / r^2 
# F1 = m1*a1 = G*m1*m2 / r^2  |  a1 = G*m2 / r^2
# G = 6.674*10^-11 N (m/kg)^2

# s = ut + 0.5 at^2
# v = u + at
# a = a
# s_{n+1} = s_{n} + v_{n}*del_t + 1/2 a_{n} delt^2
# v_{n+1} = v_{n} + 1/2 (a_{n} + a_{n+1}) delt








class Body(object):
    def __init__(self, mass, volume):
        self.mass = mass
        self.volume = volume
        self.density = mass/volume

        self.position = np.array([0,0])
        self.velocity = np.array([0,0])
        self.acceleration = np.array([0,0])


class World(object):
    def __init__(self, n):
        # spawn bodies`
        self.bodies = []
        self.cameras = []
        self.G = 6.674e-11
        self.dt = 0.01 # seconds per step

    def simulate(self, steps=0):
        while True:

            self.step()
            self.render_cameras()
            
            steps -= 1
            if steps == 0:
                break

        
    def step(self):

        # compute acceleration due to gravity between each body
        gravity_accel = self.compute_gravity()

        # update state of each body
        for i, body in enumerate(self.bodies):

            # calculate new a/v/s
            acceleration = gravity_accel[i] # + internal acceleration
            velocity = body.velocity + 0.5 * (body.acceleration + acceleration) * self.dt
            position = body.position + body.velocity*self.dt + 0.5*body.acceleration*self.dt**2

            # update state 
            body.acceleration = acceleration
            body.velocity = velocity
            body.position = position

    def compute_gravity(self):

        # calculate dense accelerations caused by gravity 
        N = len(self.bodies)
        accelerations = np.zeros((N, N, 2)) # a[i,j] = acceleration for body i caused by j
        for i in range(N):
            for j in range(i, N):
                if i==j:
                    continue
                distance = self.bodies[j].position - self.bodies[i].position # distance vector from i->j
                length = np.linalg.norm(distance)
                aimag = self.G / length**2 * self.bodies[j].mass # magnitude of gravity-accel acting on I
                ajmag = self.G / length**2 * self.bodies[i].mass 
                accelerations[i, j]  = (distance / length) * aimag # vectory of acceleration acting on I
                accelerations[j, i]  = (-distance / length) * ajmag

        # add the accelerations for each body
        combined_accel = accelerations.sum(1) # acceleration for body i caused by sum(others)
        return combined_accel




class Camera(object):
    def __init__(self, cx, cy, width, height):
        self.position = [cx,cy]
        self.dimensions = [width,height]
        self.image_size = [640,640]

    def render(self, bodies):

        for body in bodies:
            uv = body.position





