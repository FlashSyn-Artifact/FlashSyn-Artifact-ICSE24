

# from scipy.optimize import shgo

# def main():
#     def F(paras):
#         return paras[0] + paras[1] + paras[2] + paras[3] * paras[2]  + paras[4] + paras[5] + paras[6] + paras[7]

#     bnds = [(500, 5000000), (20, 200), (50, 500), (40, 406), (500, 50000), (700, 70000), (700, 70000), (1200, 120000000)]
#     result3 = shgo(func=F, bounds=bnds, n=128, iters=1, sampling_method='sobol',
#                             minimizer_kwargs={"options": {"ftol": 1}},
#                             options={
#                                 "maxfev": 80, "f_tol": 100, "maxtime": 6}
#                             ) 
#     print("result3.success: ", result3.success)
#     print(result3.message)

# if __name__ == '__main__':
#     main()
    

import numpy as np
from scipy.optimize import shgo


def main():
    def F(paras, bnds):
        paras = bnds[:, 0] + paras * (bnds[:, 1] - bnds[:, 0])  # Rescaled parameters
        return paras[0] + paras[1] + paras[2] + paras[3] * paras[2]  + paras[4] + paras[5] + paras[6] + paras[7]

    bnds = [(500, 5000000), (20, 200), (50, 500), (40, 406), (500, 50000), (700, 70000), (700, 70000), (1200, 120000000)]
    bnds = np.array(bnds)
    bnds_normalised = [(0, 1),]*len(bnds)  # Normalise boundaries back to a simplex
    
    result3 = shgo(func=F, bounds=bnds_normalised, args= (bnds,), n=1280, iters=1, sampling_method='sobol',
                            minimizer_kwargs={"options": {"ftol": 1}},
                            options={
                                "maxfev": 80, "f_tol": 100, "maxtime": 6}
                            ) 
    print("result3.success: ", result3.success)
    print(result3.message)
    print(result3)
    
    # Rescale results
    result3.x = bnds[:, 0] + result3.x * (bnds[:, 1] - bnds[:, 0])  # Might be a mistake...late night at work for me.
    print(f'Rescaled results = {result3.x}')

if __name__ == '__main__':
    main() 