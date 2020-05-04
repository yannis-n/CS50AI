import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):
                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    joint_probability = 1
    print(people)
    for person in people:
        if people[person]['mother'] is None and people[person]['father'] is None:
            print(person)
            if person in one_gene:
                joint_probability *= PROBS['gene'][1]
                gene = 1
            elif person in two_genes:
                joint_probability *= PROBS['gene'][2]
                gene = 2
            else:
                joint_probability *= PROBS['gene'][0]
                gene = 0
            if person in have_trait:
                joint_probability *= PROBOS['trait'][gene][True]
            else:
                joint_probability *= PROBOS['trait'][gene][False]
        else:
            print(person)
            print(1)

            parents = [people[person]['mother'], people[person]['father']]
            parent_passed = [0, 0]
            parent_not_passed = [0, 0]

            if person in one_gene:
                gene = 1
                for i in range(0,2):
                    if parents[i] in two_genes:
                        parent_passed[i] = 1 - PROBS['mutation']
                        parent_not_passed[i] = PROBS['mutation']
                    elif parents[i] in one_gene:
                        parent_passed[i] = 0.5
                        # * (1-PROBS['mutation']) + 0.5 * PROBS['mutation'] an einai me to apo pano
                        parent_not_passed[i] = 0.5
                        # * PROBS['mutation'] + 0.5 * (1-PROBS['mutation'])
                    else:
                        parent_passed[i] = PROBS['mutation']
                        parent_not_passed[i] = 1 - PROBS['mutation']
                parents_probability = parent_passed[0]*parent_not_passed[1] + parent_passed[1]*parent_not_passed[0]
            if person in two_genes:
                gene = 2
                for i in range(0, 2):
                    if parents[i] in two_genes:
                        parent_passed[i] = 1 - PROBS['mutation']
                    elif parents[i] in one_gene:
                        parent_passed[i] = 0.5
                    else:
                        parent_passed[i] = PROBS['mutation']
                parents_probability = parent_passed[0] + parent_passed[1]
            else:
                gene = 0
                for i in range(0, 2):
                    if parents[i] in two_genes:
                        parent_passed[i] = PROBS['mutation']
                    elif parents[i] in one_gene:
                        parent_passed[i] = 0.5
                    else:
                        parent_passed[i] = 1 - PROBS['mutation']
                    parents_probability = parent_passed[0]*parent_not_passed[1] + parent_passed[1]*parent_not_passed[0]

                joint_probability *= parents_probability

                if person in have_trait:
                    joint_probability *= PROBS['trait'][gene][True]
                else:
                    joint_probability *= PROBS['trait'][gene][False]
        return joint_probability

                #
                #
                #
                #
                #
                #
                #
                # if father in two_genes:1 - PROBS['mutation']
                #     if mother in two_genes:
                #         parents_probability = (1 - PROBS['mutation'])*PROBOS['mutation'] * 2
                #     if mother in one_gene =
                #         parents_probability = (1 - PROBS['mutation'])*0.5*(1 - PROBS['mutation']) + 0.5 * (1 - PROBS['mutation']) * PROBS['mutation']
                #     else:
                #         parents_probability = ((1 - PROBS['mutation']))*(1 - PROBS['mutation']) + PROBS['mutation']*PROBS['mutation']
                # if



def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    for person in probabilities:
        if person in one_gene:
            probabilities[person]['gene'][1] += p
        elif person in two_genes:
            probabilities[person]['gene'][2] += p
        else:
            probabilities[person]['gene'][0] += p
        if person in have_trait:
            probabilities[person]['trait'][True] += p
        else:
            probabilities[person]['trait'][False] += p


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    for person in probabilities:
        for gene in probabilities[person]['gene']:
            probabilities[person]['gene'][gene] = probabilities[person]['gene'][gene] / sum(probabilities[person]['gene'].values())
        sum_trait = probabilities[person]['trait'][True]
        for trait in probabilities[person]['trait']:
            probabilities[person]['trait'][trait] = probabilities[person]['trait'][trait] / sum(probabilities[person]['trait'].values())

if __name__ == "__main__":
    main()
