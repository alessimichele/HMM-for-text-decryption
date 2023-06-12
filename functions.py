import numpy as np


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

    for j in range(n_states):
        alpha[0, j] = pi[j] * B[j, observed[0]]

    for i in range(1, n_nodes):
        for j in range(n_states):
            for k in range(n_states):
                alpha[i, j] = (
                    alpha[i, j] + A[k, j] * B[j, observed[i]] * alpha[i - 1, k]
                )

    return alpha


# We need an algorithm to perform belief propagation on our hmm
def backward_HMM(A, B, observed):
    """
    A: transition
    B: emission
    n_nodes: number of nodes in the chain
    observed: list containing observed ones.
    """
    n_nodes = len(observed)
    n_states = A.shape[0]
    beta = np.zeros((n_nodes - 1, n_states))

    for j in range(n_states):
        for k in range(n_states):
            beta[-1, j] = beta[-1, j] + A[j, k] * B[k, observed[n_nodes - 1]]

    for i in range(n_nodes - 3, -1, -1):
        for j in range(n_states):
            for k in range(n_states):
                beta[i, j] = (
                    beta[i, j] + A[j, k] * B[k, observed[i + 1]] * beta[i + 1, k]
                )

    return beta


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
        gamma[i] = alpha[i] * beta[i] / np.sum(alpha[i] * beta[i])

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
        alpha = forward_HMM(A, B, pi, observed)
        beta = backward_HMM(A, B, observed)
        gamma = compute_all_conditional(alpha, beta)
        B = update_B(gamma, observed)
    return B


def Baum_Welch_Spaces(A, B_start, pi, observed, maxIter=100):
    B = np.copy(B_start)
    for it in range(maxIter):
        alpha = forward_HMM(A, B, pi, observed)
        beta = backward_HMM(A, B, observed)
        gamma = compute_all_conditional(alpha, beta)
        B = update_B(gamma, observed)
        B[-1, :] = np.zeros(27)
        B[-1, -1] = 1
    return B


def baum_welch(A, B_start, pi, observed, maxiter=100):
    # gpt
    N = A.shape[0]  # Number of states
    M = A.shape[1]  # Number of possible emissions
    T = len(observed)  # Length of observed chain

    B = B_start.copy()  # Make a copy of initial emission probabilities

    for _ in range(maxiter):
        # Forward-Backward algorithm (Expectation step)
        alpha = np.zeros((T, N))
        beta = np.zeros((T, N))
        c = np.zeros(T)

        # Forward pass
        alpha[0] = pi * B[:, observed[0]]
        c[0] = 1.0 / np.sum(alpha[0])
        alpha[0] *= c[0]
        for t in range(1, T):
            alpha[t] = np.dot(alpha[t - 1], A) * B[:, observed[t]]
            c[t] = 1.0 / np.sum(alpha[t])
            alpha[t] *= c[t]

        # Backward pass
        beta[T - 1] = 1
        beta[T - 1] *= c[T - 1]
        for t in range(T - 2, -1, -1):
            beta[t] = np.dot(A, beta[t + 1] * B[:, observed[t + 1]])
            beta[t] *= c[t]

        # Compute gamma and xi matrices
        gamma = alpha * beta
        xi = np.zeros((T - 1, N, N))
        for t in range(T - 1):
            xi[t] = (
                alpha[t][:, np.newaxis] * A * B[:, observed[t + 1]] * beta[t + 1]
            ) * c[t]

        # Maximization step
        B_new = np.zeros((N, M))
        for i in range(N):
            for j in range(M):
                B_new[i, j] = np.sum(gamma[:, i] * (observed == j)) / np.sum(
                    gamma[:, i]
                )

        # Check for convergence
        if np.allclose(B, B_new):
            break

        B = B_new

    return B


def baum_welch_spaces(A, B_start, pi, observed, maxiter=100):
    # gpt con spazi
    N = A.shape[0]  # Number of states
    M = A.shape[1]  # Number of possible emissions
    T = len(observed)  # Length of observed chain

    B = B_start.copy()  # Make a copy of initial emission probabilities

    for _ in range(maxiter):
        # Forward-Backward algorithm (Expectation step)
        alpha = np.zeros((T, N))
        beta = np.zeros((T, N))
        c = np.zeros(T)

        # Forward pass
        alpha[0] = pi * B[:, observed[0]]
        c[0] = 1.0 / np.sum(alpha[0])
        alpha[0] *= c[0]
        for t in range(1, T):
            alpha[t] = np.dot(alpha[t - 1], A) * B[:, observed[t]]
            c[t] = 1.0 / np.sum(alpha[t])
            alpha[t] *= c[t]

        # Backward pass
        beta[T - 1] = 1
        beta[T - 1] *= c[T - 1]
        for t in range(T - 2, -1, -1):
            beta[t] = np.dot(A, beta[t + 1] * B[:, observed[t + 1]])
            beta[t] *= c[t]

        # Compute gamma and xi matrices
        gamma = alpha * beta
        xi = np.zeros((T - 1, N, N))
        for t in range(T - 1):
            xi[t] = (
                alpha[t][:, np.newaxis] * A * B[:, observed[t + 1]] * beta[t + 1]
            ) * c[t]

        # Maximization step
        B_new = np.zeros((N, M))
        for i in range(N):
            for j in range(M):
                B_new[i, j] = np.sum(gamma[:, i] * (observed == j)) / np.sum(
                    gamma[:, i]
                )

        # Check for convergence
        if np.allclose(B, B_new):
            break

        B = B_new
        B[-1, :] = np.zeros(27)
        B[-1, -1] = 1

    return B
