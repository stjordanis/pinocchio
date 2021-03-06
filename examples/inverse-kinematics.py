from __future__ import print_function

import numpy as np
import pinocchio
pinocchio.switchToNumpyMatrix()

model = pinocchio.buildSampleModelManipulator()
data  = model.createData()

JOINT_ID = 6
oMdes = pinocchio.SE3(pinocchio.utils.eye(3), np.matrix([1., 0., 1.]).T)

q      = pinocchio.neutral(model)
eps    = 1e-4
IT_MAX = 1000
DT     = 1e-1

i=0
while True:
    pinocchio.forwardKinematics(model,data,q)
    dMi = oMdes.actInv(data.oMi[JOINT_ID])
    err = pinocchio.log(dMi).vector
    if np.linalg.norm(err) < eps:
        print("Convergence achieved!")
        break
    if i >= IT_MAX:
        print("\nWarning: the iterative algorithm has not reached convergence to the desired precision")
        break
    J   = pinocchio.Jlog6(dMi) * pinocchio.computeJointJacobian(model,data,q,JOINT_ID)
    v   = - np.linalg.pinv(J)*err
    q   = pinocchio.integrate(model,q,v*DT)
    if not i % 10:        print('error = %s' % err.T)
    i += 1

print('\nresult: %s' % q.flatten().tolist())
print('\nfinal error: %s' % err.T)
