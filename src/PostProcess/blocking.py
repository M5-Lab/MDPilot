'''
Nick Hattrup July 25, 2024
--- TO DO ---
* Going up to max power of 2 is dumb, should go up to where we have at least 8 blocks to average over
* Given this, 8+ blocks is decent for bootstrapping, can use these to better estimate block variance and average.
* But need to do some math for validation
'''

def blocking(samples):
    '''
    Calculates std_error  vs. block_size used via blocking method.

    Parameters:
    -----------
    samples (numpy array): array of data to be blocked. 

    Returns:
    --------
    powers (numpy array): powers of 2 used as block size.
    estimates (numpy array): estimate of true standard deviation
    errors (numpy array): error in the estimate of the true standard deviation
    '''

    tot_samples = len(samples)

    assert tot_samples > 0, "No samples provided"

    pow = int(np.log2(tot_samples))
    
    n_samples = 2**pow
    
    blocks = samples[:n_samples]
    powers = np.arange(pow)
    estimates = np.zeros((pow))
    errors = np.zeros((pow))

    block_size = 1
    num_blocks = n_samples
    
    estimates[0] = np.std(blocks)/np.sqrt(num_blocks-1)
    errors[0] = estimates[0]/np.sqrt(2*(num_blocks-1))

    for p in range(1, pow):
        block_size *= 2
        num_blocks /=2
        blocks = (blocks[::2] + blocks[1::2])/2 # (blocks[0] + blocks[1], blocks[2] + blocks[3], ...)/2
        estimates[p] = np.std(blocks)/np.sqrt(num_blocks-1)
        errors[p] = estimates[p]/np.sqrt(2*(num_blocks-1))
    
    # Now determine the optimal block size
    blocksize_opt = None 
    for i in range(1, pow):
        if np.abs(estimates[i] - estimates[i-1]) < errors[i-1]:
            blocksize_opt = 2**(i-1)
            break

    return powers, estimates, errors, blocksize_opt 


