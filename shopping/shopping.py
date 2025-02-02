import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4
from collections import Counter

def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")

def monthToNum(shortMonth):

    return{
            'Jan' : 0,
            'Feb' : 1,
            'Mar' : 2,
            'Apr' : 3,
            'May' : 4,
            'June' : 5,
            'Jul' : 6,
            'Aug' : 7,
            'Sep' : 8,
            'Oct' : 9,
            'Nov' : 10,
            'Dec' : 11
    }[shortMonth]

def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    evidence = list()
    labels = list()
    with open(filename, newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            evidence_row = list()
            for col in row:
                if col == 'Month':
                    row[col]=monthToNum(row[col])
                if col =='VisitorType':
                    if row[col] == 'Returning_Visitor':
                        evidence_row.append(1)
                    else:
                        evidence_row.append(0)
                elif col == 'Administrative_Duration' or col == "Informational_Duration" or col == "ProductRelated_Duration" or col == "BounceRates" or col == "ExitRates" or col == "PageValues" or col == "SpecialDay":
                    evidence_row.append(float(row[col]))
                elif col == 'Revenue':
                    if row[col] == 'TRUE':
                        labels.append(1)
                    else:
                        labels.append(0)
                else:
                    if col == 'Weekend':
                        if row[col] == 'TRUE':

                            evidence_row.append(1)
                        else:

                            evidence_row.append(0)
                    else:
                        evidence_row.append(int(row[col]))


            evidence.append(evidence_row)

        return (evidence, labels)

def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    train = KNeighborsClassifier()
    return train.fit(evidence, labels)


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificty).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    sensitivity = 0
    specificity = 0

    total_positives = 0
    total_negatives = 0

    for label, prediction in zip(labels, predictions):
        if prediction == 1:
            total_positives += 1
        else:
            total_negatives += 1

        if label == prediction:
            if label == 1:
                sensitivity += 1
            else:
                specificity += 1
    total = total_negatives+total_positives
    return (sensitivity/total_positives, specificity/total_negatives)




if __name__ == "__main__":
    main()
