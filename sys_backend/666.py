from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import f1_score
import pandas as pd
import numpy as np

# 从 CSV 文件中读取数据
data = pd.read_csv('creditcard.csv')
data = pd.DataFrame(data)
X = data.iloc[:, :-1]
y = data.iloc[:, -1]

# 步骤1：准备数据集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


def fitness_function(X_train, X_test, y_train, y_test, selected_features):
    clf = DecisionTreeClassifier()
    selected_feature_indices = np.where(selected_features)[0]
    clf.fit(X_train.iloc[:, selected_feature_indices], y_train)
    y_pred = clf.predict(X_test.iloc[:, selected_feature_indices])
    return f1_score(y_test, y_pred)


def pso_feature_selection(X_train, y_train, num_particles=1, max_iter=10, w=0.5, c1=1.5, c2=1.5):
    D = X_train.shape[1]  # 特征数量
    best_features = np.random.randint(2, size=D)
    best_fitness = 0.0

    # 初始化粒子位置和速度
    particles_position = np.random.randint(2, size=(num_particles, D))
    particles_velocity = np.random.uniform(-1, 1, size=(num_particles, D))
    personal_best_position = particles_position.copy()
    personal_best_fitness = np.zeros(num_particles)

    for i in range(num_particles):
        personal_best_fitness[i] = fitness_function(X_train, X_test, y_train, y_test, particles_position[i])
        if personal_best_fitness[i] > best_fitness:
            best_features = particles_position[i]
            best_fitness = personal_best_fitness[i]

    # 开始迭代
    for iter in range(max_iter):
        for i in range(num_particles):
            # 更新粒子速度和位置
            particles_velocity[i] = w * particles_velocity[i] + \
                                    c1 * np.random.rand() * (personal_best_position[i] - particles_position[i]) + \
                                    c2 * np.random.rand() * (best_features - particles_position[i])
            particles_position[i] = np.round(particles_position[i] + particles_velocity[i])
            particles_position[i] = np.where(particles_position[i] > 0, 1, 0)
            # 更新个体最佳位置和全局最佳位置
            fitness_value = fitness_function(X_train, X_test, y_train, y_test, particles_position[i])
            if fitness_value > personal_best_fitness[i]:
                personal_best_fitness[i] = fitness_value
                personal_best_position[i] = particles_position[i]
                if personal_best_fitness[i] > best_fitness:
                    best_features = personal_best_position[i]
                    best_fitness = personal_best_fitness[i]
        print("Best Score:", best_fitness, "Best features:", best_features)
    return best_features


if __name__ == "__main__":
    selected_features = pso_feature_selection(X_train, y_train, num_particles=20, max_iter=10)
    print("Selected Features:", selected_features)
