import numpy as np


def forward_HMM(A, B, pi, observed):
    """
    A: transition
    B: emission
    pi: initial
    n_nodes: number of nodes in the chain
    observed: list containing observed ones.
    """
    n_nodes = len(observed)
    n_states = A.shape[0]
    alpha = np.zeros((n_nodes, n_states))
    c = np.zeros(n_nodes)
    alpha_hat = np.zeros((n_nodes, n_states))

    for j in range(n_states):
        alpha[0, j] = pi[j] * B[j, observed[0]]

    c[0] = np.sum(alpha[0])
    alpha_hat[0] = alpha[0] / np.sum(alpha[0])
    # print("alpa[0]", alpha[0])

    for i in range(1, n_nodes):
        for j in range(n_states):
            for k in range(n_states):
                alpha[i, j] += A[k, j] * B[j, observed[i]] * alpha_hat[i - 1, k]
        c[i] = np.sum(alpha[i])
        alpha_hat[i] = alpha[i] / c[i]
    return alpha_hat, c


def backward_HMM(A, B, observed, c):
    """
    A: transition
    B: emission
    n_nodes: number of nodes in the chain
    observed: list containing observed ones.
    """
    n_nodes = len(observed)
    n_states = A.shape[0]
    beta = np.zeros((n_nodes - 1, n_states))
    beta_hat = np.zeros((n_nodes - 1, n_states))

    for j in range(n_states):
        for k in range(n_states):
            beta[-1, j] += A[j, k] * B[k, observed[n_nodes - 1]]

    beta_hat[-1] = beta[-1] / c[-1]

    for i in range(n_nodes - 3, -1, -1):
        for j in range(n_states):
            for k in range(n_states):
                beta[i, j] += A[j, k] * B[k, observed[i + 1]] * beta_hat[i + 1, k]
        beta_hat[i] = beta[i] / c[i + 1]

    return beta_hat


def compute_all_conditional(alpha, beta):
    """
    alpha: list containing forward messages
    beta: list containing backward messages
    """
    n_nodes = alpha.shape[0]
    n_states = alpha.shape[1]

    gamma = np.zeros((n_nodes, n_states))

    gamma[n_nodes - 1] = alpha[n_nodes - 1] / np.sum(alpha[n_nodes - 1])

    for i in range(n_nodes - 1):
        tmp = alpha[i] * beta[i]
        gamma[i] = tmp / np.sum(tmp)

    return gamma


def divide_row_by_sum(matrix):
    row_sums = np.sum(matrix, axis=1)  # Calculate the sum of each row
    divided_matrix = (
        matrix / row_sums[:, np.newaxis]
    )  # Divide each element by the corresponding row sum
    return divided_matrix


def update_B(gamma, observed):
    # n_nodes = gamma.shape[0]
    n_states = gamma.shape[1]

    B = np.zeros((n_states, n_states))

    for i in range(n_states):
        for j in range(n_states):
            for k in range(len(observed)):
                if observed[k] == j:
                    B[i, j] += gamma[k, i]

    return divide_row_by_sum(B)


def Baum_Welch(A, B_start, pi, observed, maxIter=100, tol = 1e-4):
    B = np.copy(B_start)
    changed = 0 # change is set to 1 whenever at least one coordinate increases by more than tol
    for it in range(maxIter):
        alpha_hat, c = forward_HMM(A, B, pi, observed)
        beta_hat = backward_HMM(A, B, observed, c)
        gamma = compute_all_conditional(alpha_hat, beta_hat)
        B_old = B
        B = update_B(gamma, observed)

        # Check if conerged or still changing
        change = np.abs(B - B_old)
        max_change = np.max(change)

        if(max_change < tol):
            print("Not updating anymore after iteration", it)
            break


        # following lines only for encryption
        B[-1, :] = np.zeros(27)
        B[:, -1] = np.zeros(27)
        B[-1, -1] = 1
    return B


import string


def solve_mapping_problem(L):
    alphabet = string.ascii_lowercase + " "
    mapping = {}
    for i, num in enumerate(L):
        mapping[alphabet[i]] = alphabet[num]
    return mapping


# Functions needed for the Viterbi code

def compute_f_log(A, B, observed):
    """
    It constructs the factors of the HMM which are needed to perform the forward pass of the message passing algorithm.
    Input:
        - A : the transition matrix
        - B : the emission matrix
        - observed: an array containing the observed values
    Output:
        - f0: the factor corresponding to the initial factor to first latent variable message
        - f: an array containig the all the other factors (n_states - 1)
    """
    pi = A[-1]
    n_nodes = len(observed)
    n_states = A.shape[0]
    f = np.zeros((n_nodes - 1, n_states, n_states))

    tmp = np.zeros((n_states, 1))
    for k in range(n_states):
        tmp[k] = np.log(pi[k]) + np.log(B[k, observed[0]])

    f0 = tmp

    for i in range(1, n_nodes):
        tmp = np.zeros((n_states, n_states))

        for j in range(n_states):  # over z1
            for k in range(n_states):  # over z2
                tmp[j, k] = np.log(A[j, k]) + np.log(B[k, observed[i]])

        f[i - 1] = tmp

    return f0, f


def Viterbi_log(f0, f):
    """
    Performs the forward pass of the max plus algorithm (known as Viterbi algorithm for Hidden-Markov models).
    Input: 
        - f0: the factor corresponding to the initial factor to first latent variable message
        - f: an array containig the all the other factors (n_states - 1)
    Output:
        - pmax: the array containing the messages of the forward pass
        - phi: the array storing the most probable preceding state stored during the forward pass
    """
    n_nodes = f.shape[0] + 1
    n_states = f.shape[1]

    pmax = np.zeros((n_nodes, n_states))  # Need one for every node
    phi = np.zeros(
        (n_nodes - 1, n_states)
    )  # Need one for every node other than the first one (no need to reconstruct it)

    pmax[0] = f0.flatten()

    for i in range(1, n_nodes):
        tmp = ((f[i - 1]).T + pmax[i - 1]).T

        pmax[i] = np.max(tmp, axis=0)  # by column

        phi[i - 1] = np.argmax(
            tmp, axis=0
        )  # i-1 cause this contains the reconstruction about the (i-1)th element

    return pmax, phi


def reconstruct(pmax, phi):
    """
    Given the output of a max-plus forward pass it returns the most probable hidden states.
    Input:
        - pmax: the array containing the messages of the forward pass
        - phi: the array storing the most probable preceding state stored during the forward pass
    Output:
        - An array of int that coincides with the most probable latent states
    """
    reconstruction = np.empty(len(phi) + 1)

    curr = np.argmax(pmax[-1])
    reconstruction[-1] = curr

    for i in range(len(phi) - 1, -1, -1):
        curr = int(phi[i, curr])
        reconstruction[i] = curr

    return reconstruction

