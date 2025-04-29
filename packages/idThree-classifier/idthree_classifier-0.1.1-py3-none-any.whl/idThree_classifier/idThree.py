import pandas as pd
import numpy as np
import math
from graphviz import Digraph

class ID3Classifier:
    def __init__(self):
        self.tree = None
        self.target_attribute = None

    def entropy(self, target_col):
        elements, counts = np.unique(target_col, return_counts=True)
        entropy_val = 0
        for i in range(len(elements)):
            probability = counts[i] / np.sum(counts)
            entropy_val -= probability * math.log2(probability)
        return entropy_val

    def info_gain(self, data, split_attribute_name):
        total_entropy = self.entropy(data[self.target_attribute])

        vals, counts = np.unique(data[split_attribute_name], return_counts=True)
        weighted_entropy = 0
        for i in range(len(vals)):
            subset = data[data[split_attribute_name] == vals[i]]
            weighted_entropy += (counts[i] / np.sum(counts)) * self.entropy(subset[self.target_attribute])

        information_gain = total_entropy - weighted_entropy
        return information_gain

    def id3(self, data, features, parent_class=None):
        # If all examples have same label
        if len(np.unique(data[self.target_attribute])) <= 1:
            return np.unique(data[self.target_attribute])[0]

        # If no features left
        if len(features) == 0:
            return parent_class

        # Majority class at current node
        parent_class = np.unique(data[self.target_attribute])[np.argmax(
            np.unique(data[self.target_attribute], return_counts=True)[1])]

        # Select feature with highest Information Gain
        item_values = [self.info_gain(data, feature) for feature in features]
        best_feature_index = np.argmax(item_values)
        best_feature = features[best_feature_index]

        # Tree node
        tree = {best_feature: {}}

        # Remaining features
        features = [i for i in features if i != best_feature]

        for value in np.unique(data[best_feature]):
            subset = data[data[best_feature] == value]
            subtree = self.id3(subset, features, parent_class)
            tree[best_feature][value] = subtree

        return tree

    def fit(self, data, target_attribute_name):
        self.target_attribute = target_attribute_name
        features = list(data.columns)
        features.remove(target_attribute_name)
        self.tree = self.id3(data, features)

    def predict_instance(self, query, tree):
        if not isinstance(tree, dict):
            return tree
        attribute = next(iter(tree))
        if query[attribute] in tree[attribute]:
            result = tree[attribute][query[attribute]]
        else:
            return None  # if unseen attribute value
        if isinstance(result, dict):
            return self.predict_instance(query, result)
        else:
            return result

    def predict(self, data):
        predictions = []
        for _, row in data.iterrows():
            predictions.append(self.predict_instance(row, self.tree))
        return predictions

    def print_tree(self, tree=None, indent="  "):
        if tree is None:
            tree = self.tree
        if not isinstance(tree, dict):
            print(indent + str(tree))
            return
        for key, value in tree.items():
            print(indent + str(key))
            for sub_key, sub_tree in value.items():
                print(indent * 2 + str(sub_key))
                self.print_tree(sub_tree, indent * 3)

    def visualize_tree(self, filename='id3_tree'):
        def _visualize_tree(tree, parent_name='', graph=None, node_id=[0]):
            if graph is None:
                graph = Digraph()

            current_node = str(node_id[0])
            node_id[0] += 1

            if isinstance(tree, dict):
                feature = next(iter(tree))
                graph.node(current_node, feature)

                if parent_name:
                    graph.edge(parent_name, current_node)

                for value, subtree in tree[feature].items():
                    child_node = _visualize_tree(subtree, current_node, graph, node_id)
                    graph.edge(current_node, child_node, label=str(value))
            else:
                graph.node(current_node, str(tree))
                if parent_name:
                    graph.edge(parent_name, current_node)

            return current_node if graph else graph

        dot = Digraph()
        _visualize_tree(self.tree, graph=dot)
        dot.render(filename, format='png', cleanup=True)
        dot.view()

# Example usage
if __name__ == "__main__":
    # Load dataset
    dataset = pd.read_csv("weather.csv")

    # Create and train classifier
    clf = ID3Classifier()
    clf.fit(dataset, target_attribute_name="Play")

    # Print the tree
    print("\nDecision Tree (Text Visualization):\n")
    clf.print_tree()

    # Predict on training data
    print("\nPredictions on training data:")
    predictions = clf.predict(dataset.drop(columns=["Play"]))
    print(predictions)

    # Visualize the tree
    clf.visualize_tree('id3_tree')
