import math


class NaiveBayes:
    def fit(self, X, y):
        self.classes = list(set(y))
        self.priors = {}
        self.means = {}
        self.vars = {}
        n = len(y)
        for c in self.classes:
            # create classes
            X_c = [X[i] for i in range(n) if y[i] == c]
            print(X_c)
            self.priors[c] = len(X_c) / n
            self.means[c] = [sum(x[f] for x in X_c) / len(X_c) for f in range(len(X[0]))]
            self.vars[c] = [sum((x[f] - self.means[c][f]) ** 2 for x in X_c) / len(X_c) for f in range(len(X[0]))]
        print("priors:", self.priors)
        print("means:", self.means)
        print("vars:", self.vars)

    def gaussian(self, x, mean, var):
        eps = 1e-9
        return (1 / math.sqrt(2 * math.pi * (var + eps))) * math.exp(-((x - mean) ** 2) / (2 * (var + eps)))

    def predict(self, X, threshold=0.5):
        preds = []
        for x in X:
            scores = {}
            for c in self.classes:
                log_prob = math.log(self.priors[c])
                for f in range(len(x)):
                    log_prob += math.log(self.gaussian(x[f], self.means[c][f], self.vars[c][f]) + 1e-9)
                scores[c] = log_prob
            preds.append(max(scores, key=scores.get))
        return preds


if __name__ == "__main__":
    # features: [word_count, exclamation_marks]
    X_nb = [[10, 1], [12, 0], [9, 1], [11, 2], [50, 5], [60, 8], [55, 6], [58, 7]]
    y_nb = [0, 0, 0, 0, 1, 1, 1, 1]  # 0=ham, 1=spam
    X_test = [[11, 1], [55, 5]]
    nb = NaiveBayes()
    print(nb.fit(X_nb, y_nb))
    print('NB train:', nb.predict(X_nb))
    print('NB train:', nb.predict(X_test))
