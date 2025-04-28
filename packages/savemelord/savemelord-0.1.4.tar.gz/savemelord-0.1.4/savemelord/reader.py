import pkgutil

def exp1():
    data = pkgutil.get_data(__package__, 'gridworld.txt')
    print(data.decode('utf-8'))

def sarsa_v_q():
    data = pkgutil.get_data(__package__, 'sarsavq.txt')
    print(data.decode('utf-8'))

def bandit_problem():
    data = pkgutil.get_data(__package__, 'banditproblem.txt')
    print(data.decode('utf-8'))

def sampleAverage():
    data = pkgutil.get_data(__package__, 'sampleaverage.txt')
    print(data.decode('utf-8'))

def ucb_and_optimal_val():
    data = pkgutil.get_data(__package__, 'ucb_and_optimal_val.txt')
    print(data.decode('utf-8'))

def policyiter_policyeval():
    data = pkgutil.get_data(__package__, 'policyiter_policyeval.txt')
    print(data.decode('utf-8'))

def value_iteration_gridworld():
    data = pkgutil.get_data(__package__, 'value_iteration_gridworld.txt')
    print(data.decode('utf-8'))

def doubleQL():
    data = pkgutil.get_data(__package__, 'doubleQL.txt')
    print(data.decode('utf-8'))

def montecarlo():
    data = pkgutil.get_data(__package__, 'montecarlo.txt')
    print(data.decode('utf-8'))

def temporal():
    data = pkgutil.get_data(__package__, 'temporal.txt')
    print(data.decode('utf-8'))


def helpme():
    data = pkgutil.get_data(__package__, 'help.txt')
    print(data.decode('utf-8'))