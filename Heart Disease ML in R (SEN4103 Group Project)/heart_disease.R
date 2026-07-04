library(tidyverse)
library(corrplot)
library(caret)
library(caTools)
library(cluster)
library(e1071)
library(scales)


set.seed(1352)


df <- read.csv("heart.csv")


# Data Analysis
summary(df)
str(df)
names(df)

head(df, 8)

colSums(is.na(df))


# Data Cleaning & Preprocessing
categoric_cols <- c("sex", "cp", "fbs", "restecg", "exang", "slope", "ca",
                    "thal", "target")
numeric_cols <- c("age", "trestbps", "chol", "thalach", "oldpeak")

clean_df <- df %>%
            mutate(across(all_of(categoric_cols), as.factor))

clean_df[numeric_cols] <- scale(clean_df[numeric_cols])

split <- sample.split(clean_df$target, SplitRatio=0.8)

train_set <- subset(clean_df, split == TRUE)
test_set <- subset(clean_df, split == FALSE)


# Exploratory Data Analysis (EDA)
cor_matrix <- cor(clean_df[, numeric_cols])
corrplot(cor_matrix, method = "color", type = "upper", tl.col = "black", addCoef.col = "black")


my_colors <- c("#1f77b4", "#d62728")

ggplot(clean_df, aes(x = target, fill = target)) +
        geom_bar(color = "white", width = 0.4) +
        scale_fill_manual(values = my_colors) +
        labs(title = "Target Distribution", x = "Target", y = "Count") +
        theme_minimal() +
        theme(legend.position = "none")

ggplot(clean_df, aes(x = age, fill = target)) +
        geom_histogram(bins = 20, alpha = 0.65, position = "identity", color = "white") +
        scale_fill_manual(values = my_colors) +
        labs(title = "Age Distribution by Target", x = "Age", y = "Count", fill = "Target") +
        theme_minimal()

ggplot(clean_df, aes(x = age, y = thalach, color = target)) +
        geom_point(alpha = 0.45, size = 2.5) +
        geom_smooth(method = "lm", se = FALSE, linewidth = 1.2) + 
        scale_color_manual(values = my_colors) +
        labs(title = "Age vs Max Heart Rate", x = "Age", y = "Max Heart Rate (bpm)", color = "Target") +
        theme_minimal()

clean_df %>% mutate(Sex = ifelse(sex == 1, "Male", "Female")) %>%
    ggplot(aes(x = Sex, fill = target)) +
    geom_bar(position = "fill", color = "white") +
    scale_fill_manual(values = my_colors) +
    scale_y_continuous(labels = percent_format()) +
    labs(title = "Sex vs Target (%)", x = "Sex", y = "Proportion", fill = "Target") +
    theme_minimal()

ggplot(clean_df, aes(x = cp, fill = target)) +
        geom_bar(position = "fill", color = "white") +
        scale_fill_manual(values = my_colors) +
        scale_y_continuous(labels = percent_format()) +
        labs(title = "Chest Pain Type vs Target (%)", x = "Chest Pain Type (0-3)", y = "Proportion", fill = "Target") +
        theme_minimal()


# K-Means
num_of_centers <- 15

elb_scores <- numeric(15)

kmeans_data <- clean_df[, numeric_cols]

for (i in 1:num_of_centers) {
  km_res <- kmeans(kmeans_data, centers=i, nstart=20)
  elb_scores[i] <- km_res$tot.withinss
}

elbow_df <- data.frame(
  K = 1:num_of_centers,
  WSS = elb_scores
)

ggplot(elbow_df, aes(x=K, y=WSS))+
  geom_point()+
  geom_line()+
  xlab("Number of Clusters")+
  ylab("Total Within-Cluster Sum of Squares Scores")


sil_scores <- numeric(num_of_centers)

for (i in 2:num_of_centers) {
  km_res <- kmeans(kmeans_data, centers = i, nstart = 20)
  ss <- silhouette(km_res$cluster, dist(kmeans_data))
  sil_scores[i] <- mean(ss[, 3])
}

sil_df <- data.frame(
  K = 2:num_of_centers,
  Silhouette_Score = sil_scores[2:num_of_centers]
)

ggplot(sil_df, aes(x=K, y=Silhouette_Score))+
  geom_point()+
  geom_line()+
  xlab("Number of Clusters")+
  ylab("Silhouette Scores")


# Support Vector Machine (SVM)
svm_model <- svm(target ~ ., 
                 data = train_set, 
                 kernel = "radial", 
                 cost = 1, 
                 scale = FALSE)

svm_predictions <- predict(svm_model, test_set)

conf_matrix <- confusionMatrix(svm_predictions, test_set$target, positive = "1")

TN <- conf_matrix$table[1, 1]
FN <- conf_matrix$table[1, 2]
FP <- conf_matrix$table[2, 1]
TP <- conf_matrix$table[2, 2]

recall <- TP / (TP + FN)
precision <- TP / (TP + FP)
F1_Score <- 2 * (precision * recall) / (precision + recall)

