import numpy as np

##### SCALING CON SAMU


# We need an algorithm to perform belief propagation on our hmm
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

    for i in range(1, n_nodes):
        for j in range(n_states):
            for k in range(n_states):
                alpha[i, j] = (
                    alpha[i, j] + A[k, j] * B[j, observed[i]] * alpha[i - 1, k]
                )
        c[i] = np.sum(alpha[i]) / np.prod(c[0:i])
        alpha_hat[i] = alpha[i] / np.sum(alpha[i])

    return alpha, alpha_hat, c


# We need an algorithm to perform belief propagation on our hmm
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
            beta[-1, j] = beta[-1, j] + A[j, k] * B[k, observed[n_nodes - 1]]

    beta_hat[-1] = beta[-1] / c[-1]

    for i in range(n_nodes - 3, -1, -1):
        for j in range(n_states):
            for k in range(n_states):
                beta[i, j] = (
                    beta[i, j] + A[j, k] * B[k, observed[i + 1]] * beta[i + 1, k]
                )
        beta_hat[i] = beta[i] / np.prod(c[i + 1 :])

    return beta, beta_hat


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


def Baum_Welch(A, B_start, pi, observed, maxIter=100):
    B = np.copy(B_start)
    for it in range(maxIter):
        alpha, alpha_hat, c = forward_HMM(A, B, pi, observed)
        beta, beta_hat = backward_HMM(A, B, observed, c)
        gamma = compute_all_conditional(alpha_hat, beta_hat)
        B = update_B(gamma, observed)

        # following lines only for encryption
        B[-1, :] = np.zeros(27)
        B[-1, -1] = 1
    return B
