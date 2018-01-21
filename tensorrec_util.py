import random
import scipy.sparse as sp


def generate_dummy_project_data(num_investors=15000, num_projects=30000, interaction_density=.00045, pos_int_ratio=.5, n_features=17):

    #n_investor_features = int(num_investors * 1.2)
    n_investor_features = n_features
    n_investor_tags = num_investors * 3
    #n_project_features = int(num_projects * 1.2)
    n_project_features = n_features
    n_project_tags = num_projects * 3
    n_interactions = (num_investors * num_projects) * interaction_density

    investor_features = sp.lil_matrix((num_investors, n_investor_features))
    for i in range(num_investors):
        for j in range(n_investor_features):
            if (i+1)%(j+1) == j:
                investor_features[i, j] = 1

    for i in range(n_investor_tags):
        investor_features[random.randrange(num_investors), random.randrange(n_investor_features)] = 1

    project_features = sp.lil_matrix((num_projects, n_project_features))
    for i in range(num_projects):
        for j in range(n_project_features):
            if (i+1)%(j+1) == j:
                project_features[i, j] = 1

    for i in range(n_project_tags):
        project_features[random.randrange(num_projects), random.randrange(n_project_features)] = 1

    interactions = sp.lil_matrix((num_investors, num_projects))
    for i in range(int(n_interactions * pos_int_ratio)):
        interactions[random.randrange(num_investors), random.randrange(num_projects)] = 1

    for i in range(int(n_interactions * (1 - pos_int_ratio))):
        interactions[random.randrange(num_investors), random.randrange(num_projects)] = -1

    return interactions, investor_features, project_features
