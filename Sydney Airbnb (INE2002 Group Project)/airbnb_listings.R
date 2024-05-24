library(leaflet)
library(leaflet.providers)
library(dplyr)
library(tidyverse)
library(readr)
library(ggpubr)
library(car)
library(RColorBrewer)

setwd("/Users/burak/Desktop/airbnb")

listings <- read_csv("listings.csv", col_types = cols(id = col_character(), 
                                                      neighbourhood_group = col_skip(), latitude = col_number(), 
                                                      longitude = col_number(), last_review = col_skip(), 
                                                      license = col_skip()))
l_lng <- listings$longitude
l_lat <- listings$latitude

map <- leaflet() %>% addTiles() %>% addCircles(lng=l_lng, lat=l_lat, color="#f01212", radius=10,
                                               popup=listings$name, fillOpacity=0.5)

sampleListings <- sample_n(listings, 500, replace=F)

s_lng <- sampleListings$longitude
s_lat <- sampleListings$latitude
ms_lng <- mean(s_lng)
ms_lat <- mean(s_lat)

coord_func <- function(regg_line, n){
  as.numeric(coef(regg_line)[2])*n + as.numeric(coef(regg_line)[1])
}

regg_line <- lm(s_lat ~ s_lng)
lng_coord <- seq(from=min(s_lng)-0.025, to=max(s_lng)+0.025, by=((max(s_lng)-min(s_lng))/100))
lat_coord <- c()
for (lat in lng_coord) {
  coord <- coord_func(regg_line, lat)
  lat_coord <- c(lat_coord, coord)
}

coord_df <- data.frame("longitude" = c(lng_coord), "latitude" = c(lat_coord))

sampleMap <- leaflet() %>% addTiles() %>%
  addCircles(lng=s_lng, lat=s_lat, color="#f01212", radius=10,
             popup=sampleListings$name, fillOpacity=1) %>%
  addCircles(lng=ms_lng, lat=ms_lat, color="#161266", radius=750,
             popup="Mean Latitude and Longitude of Sample", fillOpacity=0.25) %>%
  addPolylines(lng=coord_df$longitude, lat=coord_df$latitude, color="#000", fillOpacity=1,
               popup="Best Fit of Longitude and Latitude of Sample")

sampleMap

# Regression line of coordinates shown in a more simple plot.
plot(s_lng, s_lat)
abline(lm(s_lat ~ s_lng), col="#f01212")


p_val <- function(p){
  case_when(
    p <= 0.01 ~ "Difference is Highly Significant; Reject H0",
    p > 0.01 & p <= 0.05 ~ "Difference is Significant; Reject H0",
    p > 0.05 & p <= 0.1 ~ "Difference is Weakly Significant; Reject or Do not Reject H0",
    p > 0.1 ~ "Difference is not Significant; Do not Reject H0",
  )
}

shaw_p_val <- function(p){
  case_when(
    p <= 0.01 ~ "Difference is Highly Significant; No Normality",
    p > 0.01 & p <= 0.05 ~ "Difference is Significant; No Normality",
    p > 0.05 & p <= 0.1 ~ "Difference is Weakly Significant; Not Significantly Normal",
    p > 0.1 ~ "Difference is not Significant; Normal Distribution",
  )
}

chisq_p_val <- function(p){
  case_when(
    p <= 0.01 ~ "Difference is Highly Significant; Independent",
    p > 0.01 & p <= 0.05 ~ "Difference is Significant; Independent",
    p > 0.05 & p <= 0.1 ~ "Difference is Weakly Significant; Not Significantly Dependent",
    p > 0.1 ~ "Difference is not Significant; Dependent",
  )
}


"#fff"
# Plotting Graphs

outlier_rm <- function(data){
  data <- data[!is.na(data)]
  qnt <- quantile(data, probs=c(.25, .75))
  iqr <- IQR(data)
  lower <- qnt[1] - 1.5*iqr
  upper <- qnt[2] + 1.5*iqr
  cleaned_data <- data[data > lower & data < upper]
  return(cleaned_data)
}

# Bar Plot of Population's Room Types:
barplot(table(listings$room_type), col=c("#06d0d0","#d322a7","#4ba137","#d1d85e"))

# Bar Plot of Sample's Room Types:
barplot(table(sampleListings$room_type), col=c("#06d0d0","#d322a7","#4ba137","#d1d85e"))

# Bar Plot of Population's Neighbourhood:
barplot(table(listings$neighbourhood), col=brewer.pal(7, "Set3"),
        cex.names=0.5, space=6, las=2)

# Bar Plot of Sample's Neighbourhood:
barplot(table(sampleListings$neighbourhood), col=brewer.pal(7, "Set3"),
        cex.names=0.5, space=6, las=2)


# Pie Chart of Population's Room Types: 
pie(table(listings$room_type), col="#eaeaea", radius=0.8,
    main="Population's Room Type")

# Pie Chart of Sample's Room Types: 
pie(table(sampleListings$room_type), col="#eaeaea", radius=0.8,
    main="Sample's Room Type")


# Box Plot of 365 Day Availability:
boxplot(listings$availability_365,
        main="Availability for 365 Days", col="#fa1212")

# Box Plot of Number of Reviews (with outliers):
boxplot(listings$number_of_reviews,
        main="Number of Reviews", col="#2525de")

# Box Plot of Number of Reviews (without outliers):
boxplot(listings$number_of_reviews, outline=F,
        main="Number of Reviews", col="#2525de")

# Box Plot of Calculated Host Listings Count (with outliers):
boxplot(listings$calculated_host_listings_count,
        main="Airbnb Listings of a Host", col="#f9d1f9")

# Box Plot of Calculated Host Listings Count (without outliers):
boxplot(listings$calculated_host_listings_count, outline=F,
        main="Airbnb Listings of a Host", col="#f9d1f9")

# Box Plot of Number of Reviews in Last 12 Months (with outliers):
boxplot(listings$number_of_reviews_ltm,
        main="Number of Reviews in Last 12 Months", col="#9b27bd")

# Box Plot of Number of Reviews in Last 12 Months (without outliers):
boxplot(listings$number_of_reviews_ltm, outline=F,
        main="Number of Reviews in Last 12 Months", col="#9b27bd")

# Box Plot of Reviews per Month (with outliers):
boxplot(listings$reviews_per_month,
        main="Reviews per Month", col="#cfcd16")

# Box Plot of Reviews per Month (without outliers):
boxplot(listings$reviews_per_month, outline=F,
        main="Reviews per Month", col="#cfcd16")

# Box Plot of Price (with outliers):
boxplot(listings$price,
        main="Price", col="#1e9e20")

# Box Plot of Price (without outliers):
boxplot(listings$price, outline=F,
        main="Price", col="#1e9e20")


# Histogram of Availability on Year:
hist(listings$availability_365, col=brewer.pal(12, "Set3"),
     xlab="Availability for 365 Days", main="")

# Histogram of Price (with outliers):
hist(listings$price, breaks=500, col=brewer.pal(12, "Set3"),
     xlab="Price", main="")

# Histogram of Price (without outliers):
handled_prc <- outlier_rm(listings$price)
hist(handled_prc, col=brewer.pal(12, "Set3"), xlab="Price", main="")
rm(handled_prc)

# Histogram of Calculated Host Listings Count (with outliers):
hist(listings$calculated_host_listings_count, breaks=50, col=brewer.pal(12, "Set3"),
     xlab="Airbnb Listings of a Host", main="")

# Histogram of Calculated Host Listings Count (without outliers):
handled_chlc <- outlier_rm(listings$calculated_host_listings_count)
hist(handled_chlc, col=brewer.pal(12, "Set3"), xlab="Airbnb Listings of a Host", main="")
rm(handled_chlc)

# Histogram of Number of Reviews (with outliers):
hist(listings$number_of_reviews, breaks=20, col=brewer.pal(12, "Set3"),
     xlab="Number of Reviews", main="")

# Histogram of Number of Reviews (without outliers):
handled_nmrv <- outlier_rm(listings$number_of_reviews)
hist(handled_nmrv, col=brewer.pal(12, "Set3"), xlab="Number of Reviews", main="")
rm(handled_nmrv)


"#fff"
# Normality Tests

norm_test <- function(p){
  case_when(
    p <= 0.01 ~ "Difference is Highly Significant; No Normality",
    p > 0.01 & p <= 0.05 ~ "Difference is Significant; No Normality",
    p > 0.05 & p <= 0.1 ~ "Difference is Weakly Significant; Not Significantly Normal",
    p > 0.1 ~ "Difference is not Significant; Normal Distribution",
  )
}

# We have a graphical method for checking normality
# Q-Q Plot Method:
qqPlot(sampleListings$price)

# It looks like we have an outlier so let's just ignore the outlier.
reasonableSample <- sampleListings[sampleListings$price <= 2500, ]
reasonableSample <- reasonableSample %>% drop_na("price")

qqPlot(reasonableSample$price)

# Let's check the reasonableListings' price distribution in other
# statistical methods and compare p-Values with Shapiro-Wilk Test.
prc_shaw <- shapiro.test(reasonableSample$price)
shaw_p <- prc_shaw$p.value
cat(norm_test(shaw_p), "in Price for Shapiro-Wilk Test")

# Method 1: Chi-Square Goodness-of-Fit Test:
prc_gof <- chisq.test(reasonableSample$price)
gof_p <- prc_gof$p.value
cat(norm_test(gof_p), "in Price for Chi-Square Goodness-of-Fit Test")

cat("Shapiro-Wilk Test, p-Value:", shaw_p, "\n",
    "Chi-Square Goodness-of-Fit Test, p-Value:", gof_p)

# Method 2: Kolmogorov-Smirnov Test:
prc_kolms <- ks.test(reasonableSample$price, 'pnorm')
kolms_p <- prc_kolms$p.value
cat(norm_test(kolms_p), "in Price for Kolmogorov-Smirnov Test")

cat("Shapiro-Wilk Test, p-Value:", shaw_p, "\n",
    "Kolmogorov-Smirnov Test, p-Value:", kolms_p)


"#fff"
# Point Estimate and Confidence Intervals

confidence_levels <- c(0.9, 0.95, 0.99)

conf_interval <- function(attr, z){
  point_est <- mean(sampleListings[[attr]], na.rm=T)
  std_err <- sd(sampleListings[[attr]], na.rm=T) / sqrt(length(sampleListings[[attr]]))
  
  margin_of_err <- z * std_err
  low_bound <- point_est - margin_of_err
  up_bound <- point_est + margin_of_err
  
  return(list(low_bound, point_est, up_bound))
}

# Confidence Interval of Prices:
# First, let's find point estimate of rental price.
mean_rent_prc <- conf_interval("price", confidence_levels[1])[[2]]
cat("Point Estimate of Rental Price ->", mean_rent_prc)

# Then for every confidence level (%90, %95, %99) of
# rental price let's find out confidence interval.
for (z in confidence_levels){
  conf_intv <- conf_interval("price", z)
  cat("%", 100*z, " Confidence Interval for Number of Reviews", " -> ", 
      round(conf_intv[[1]], 3), "$ and ", round(conf_intv[[3]], 3), "$",
      "\n", sep="")
}

# Confidence Interval of Review Numbers:
# First, let's find point estimate of review numbers.
mean_rev_num <- conf_interval("number_of_reviews", confidence_levels[1])[[2]]
cat("Point Estimate of Number of Reviews ->", round(mean_rev_num, 1))

# Then for every confidence level (%90, %95, %99) of
# review numbers let's find out confidence interval.
for (z in confidence_levels){
  conf_intv <- conf_interval("number_of_reviews", z)
  cat("%", 100*z, " Confidence Interval for Number of Reviews", " -> ",
      round(conf_intv[[1]], 1), " and ", round(conf_intv[[3]], 1),
      "\n", sep="")
}


"#fff"
# Hypothesis Testing
# Hypothesis 1: Accommodations listed by hosts with a higher number of reviews
# tend to have higher occupancy rates and command higher prices in Sydney:
# H0: ρ=0, H1: ρ≠0

sampleListings$occupancy <- 365-sampleListings$availability_365

pearson_corr_rel <- function(r){
  case_when(
    abs(r) >= 0 & abs(r) <= 0.19 ~ "Very Weak Correlation",
    abs(r) > 0.19 & abs(r) <= 0.39 ~ "Weak Correlation",
    abs(r) > 0.39 & abs(r) <= 0.59 ~ "Moderate Correlation",
    abs(r) > 0.59 & abs(r) <= 0.79 ~ "Strong Correlation",
    abs(r) > 0.79 & abs(r) <= 1 ~ "Very Strong Correlation",
  )
}

spearman_corr_rel <- function(rho){
  case_when(
    abs(rho) == 0 ~ "No Correlation",
    abs(rho) > 0 & abs(rho) <= 0.19 ~ "Very Weak Correlation",
    abs(rho) > 0.19 & abs(rho) <= 0.39 ~ "Weak Correlation",
    abs(rho) > 0.39 & abs(rho) <= 0.59 ~ "Moderate Correlation",
    abs(rho) > 0.59 & abs(rho) <= 0.79 ~ "Strong Correlation",
    abs(rho) > 0.79 & abs(rho) <= 0.99 ~ "Very Strong Correlation",
    abs(rho) == 1 ~ "Monotonic Correlation"
  )
}

# Let's do Pearson Correlation Coefficient (with assuming normality).
rho_occ_norm <- cor(sampleListings$number_of_reviews, sampleListings$occupancy, method="pearson")
cat("Pearson Correlation Coefficient:", rho_occ_norm, "->",
    pearson_corr_rel(rho_occ_norm), "between Number of Reviews and Occupancy (assuming normality)")

rho_prc_norm <- cor(sampleListings$number_of_reviews, sampleListings$price, method="pearson")
cat("Pearson Correlation Coefficient:", rho_prc_norm, "->",
    pearson_corr_rel(rho_prc_norm), "between Number of Reviews and Price (assuming normality)")

# Check the normality for more accurate results.
rew_shaw <- shapiro.test(sampleListings$number_of_reviews)
cat(shaw_p_val(rew_shaw$p), "in Number of Reviews")
occ_shaw <- shapiro.test(sampleListings$occupancy)
cat(shaw_p_val(occ_shaw$p), "in Occupancy")
prc_shaw <- shapiro.test(sampleListings$price)
cat(shaw_p_val(prc_shaw$p), "in Price")

# 1st Way: Finding the Spearman's correlation coefficient.
rho_occ <- cor(sampleListings$number_of_reviews, sampleListings$occupancy, method="spearman")
cat("Spearman Correlation Coefficient:", rho_occ, "->",
    spearman_corr_rel(rho_occ), "between Number of Reviews and Occupancy")

rho_prc <- cor(sampleListings$number_of_reviews, sampleListings$price, method="spearman")
cat("Spearman Correlation Coefficient:", rho_prc, "->",
    spearman_corr_rel(rho_prc), "between Number of Reviews and Price")

# 2nd Way: Comparing test value and critical (t) value but with Spearman's rho cor.test().
cor.test(sampleListings$number_of_reviews, sampleListings$occupancy, method="spearman")
cor.test(sampleListings$number_of_reviews, sampleListings$price, method="spearman")

# 3rd Way: Checking the scatter graph to see any relation.
plot(sampleListings$number_of_reviews, sampleListings$occupancy, xlab="Number of Reviews", ylab="Occupancy")
plot(sampleListings$number_of_reviews, sampleListings$price, xlab="Number of Reviews", ylab="Price")


# Hypothesis 2: A person is curios whether his/her region's mean price
# is significantly greater than his/her friend's region:
# H0: μ1=μ2, H1: μ1>μ2

person1 <- sample_n(listings, 1)
p1_nbhd <- person1$neighbourhood
p1_nbhd_df <- head(listings[listings$neighbourhood == p1_nbhd, ], 10)
p1_varprc <- var(p1_nbhd_df$price)

nbhd_without1 <- listings[listings$neighbourhood != p1_nbhd, ]

person2 <- sample_n(nbhd_without1, 1)
p2_nbhd <- person2$neighbourhood
p2_nbhd_df <- head(listings[listings$neighbourhood == p2_nbhd, ], 10)
p2_varprc <- var(p2_nbhd_df$price)

rm(nbhd_without1)

normality_method <- function(p1, p2){
  case_when(
    p1 <= 0.1 | p2 <= 0.1 ~ "spearman",
    p1 > 0.1 & p2 > 0.1 ~ "pearson",
  )
}

mean_p_val <- function(p){
  case_when(
    p <= 0.01 ~ "Difference is Highly Significant; Region of 1st Person's Mean Price is Higher",
    p > 0.01 & p <= 0.05 ~ "Difference is Significant; Region of 1st Person's Mean Price is Higher",
    p > 0.05 & p <= 0.1 ~ "Difference is Weakly Significant; Region of 1st Person's Mean Price is Higher",
    p > 0.1 ~ "Difference is not Significant; Region of 1st Person's Mean Price is not Higher",
  )
}

# Let's do two-sample t Test (with assuming normality).
t <- t.test(p1_nbhd_df$price, p2_nbhd_df$price,
       var.equal=(p1_varprc == p2_varprc), alternative="greater")
t_mean_diff <- t$p.value

cat("p-Value:", t_mean_diff, "->", mean_p_val(t_mean_diff), "(with assuming independence and normality)")

# Check the normality and independence(correlation) for more accurate results.
p1_shaw <- shapiro.test(p1_nbhd_df$price)
cat(shaw_p_val(p1_shaw$p), "in 1st Person's Neighbourhood Prices")
p2_shaw <- shapiro.test(p2_nbhd_df$price)
cat(shaw_p_val(p2_shaw$p), "in 2nd Person's Neighbourhood Prices")

prc_diff_rel <- cor(p1_nbhd_df$price, p2_nbhd_df$price,
                    method=normality_method(p1_shaw$p, p2_shaw$p))

if (normality_method(p1_shaw$p, p2_shaw$p) == "spearman"){
  cat("Spearman Correlation Coefficient:", prc_diff_rel, "->",
      spearman_corr_rel(prc_diff_rel), "in 1st and 2nd Person's Neighbourhood Prices")
} else {
  cat("Pearson Correlation Coefficient:", prc_diff_rel, "->",
      pearson_corr_rel(prc_diff_rel), "in 1st and 2nd Person's Neighbourhood Prices")
}

# Using Mann-Whitney U Test to compare two sample means
# which are not normally distributed and independent.
u <- wilcox.test(p1_nbhd_df$price, p2_nbhd_df$price, alternative="greater", conf.int=T)
u_mean_diff <- u$p.value

cat("Mann Whitney p-Value:", u_mean_diff, "->", mean_p_val(u_mean_diff))


# Hypothesis 3: Same person also wonders whether his/her region's variance of price
# is significantly smaller than his/her friend's region:
# H0: σ²=σ², H1: σ²<σ²

var_p_val <- function(p){
  case_when(
    p <= 0.01 ~ "Difference is Highly Significant; Region of 1st Person's Variance is Smaller",
    p > 0.01 & p <= 0.05 ~ "Difference is Significant; Region of 1st Person's Variance is Smaller",
    p > 0.05 & p <= 0.1 ~ "Difference is Weakly Significant; Region of 1st Person's Variance is Smaller",
    p > 0.1 ~ "Difference is not Significant; Region of 1st Person's Variance is not Smaller",
  )
}

# Let's do F-Test (with assuming normality).
f <- var.test(p1_nbhd_df$price, p2_nbhd_df$price, alternative="less")
f_var_diff <- f$p.value

cat("p-Value:", f_var_diff, "->", var_p_val(f_var_diff))

# From the last example (Hypothesis 2) we computed the
# normality and independence so we don't have to use it again.
cat(shaw_p_val(p1_shaw$p), "in 1st Person's Neighbourhood Prices")
cat(shaw_p_val(p2_shaw$p), "in 2nd Person's Neighbourhood Prices")

# Using Fligner-Killeen Test to compare two sample variances
# which are not normally distributed.
combined_price <- rbind(data.frame(price = p1_nbhd_df$price, group = "p1"),
                     data.frame(price = p2_nbhd_df$price, group = "p2"))

lev <- leveneTest(price ~ group, data=combined_price, center=median)
lev_var_diff <- lev$`Pr(>F)`[1]

cat("Fligner-Killeen p-Value:", lev_var_diff, "->", var_p_val(lev_var_diff))


"#fff"
# Goodness-of-Fit Test for Expected and Observed Values

fit_test <- function(p){
  case_when(
    p <= 0.01 ~ "Difference is Highly Significant; Expected and Observed is Significantly Different",
    p > 0.01 & p <= 0.05 ~ "Difference is Significant; Expected and Observed is Significantly Different",
    p > 0.05 & p <= 0.1 ~ "Difference is Weakly Significant; Expected and Observed is not too Significantly Different",
    p > 0.1 ~ "Difference is not Significant; Expected and Observed is not Different",
  )
}

# Let's check the difference of observed frequencies of sampleListings
# and expected probabilities of Listings.
freq5listings <- sampleListings %>%
              group_by(neighbourhood) %>%
              filter(n() > 5)

freq5_nbhd <- c()

for (nbhd in freq5listings$neighbourhood) {
  if (!(nbhd %in% freq5_nbhd)) {
    freq5_nbhd <- c(freq5_nbhd, nbhd)
  }
}

listings5 <- data.frame()

for (i in 1:nrow(listings)) {
  if (listings$neighbourhood[i] %in% freq5_nbhd) {
    listings5 <- rbind(listings5, listings[i, ])
  }
}

sample_nbhd_freq <- data.frame(table(sampleListings$neighbourhood))
names(sample_nbhd_freq) <- c("neighbourhood", "frequency")
sample_nbhd_freq <- sample_nbhd_freq[(sample_nbhd_freq$neighbourhood %in% freq5_nbhd), ]

freq_listings <- data.frame(table(listings5$neighbourhood))
names(freq_listings) <- c("neighbourhood", "frequency")
total_freq_nbhd_listings <- sum(freq_listings$frequency)
freq_listings$probability_frequency <- freq_listings$frequency / total_freq_nbhd_listings

chi2_test <- chisq.test(sample_nbhd_freq$frequency, p=freq_listings$probability_frequency)
chi2_p <- chi2_test$p.value

cat("χ² Value",chi2_p, "->", fit_test(chi2_p), "in Neigbourhoods")


"#fff"
# Correlation and Regression

# Let's find the correlation between Number of Reviews and Price.

plot(sampleListings$number_of_reviews, sampleListings$price, col="#2525de")

rew_prc_corr <- cor(sampleListings$number_of_reviews, sampleListings$price, method="spearman")
cat("Spearman Correlation Coefficient:", rew_prc_corr, "->",
    spearman_corr_rel(rew_prc_corr), "between Number of Reviews and Price")

abline(lm(sampleListings$price ~ sampleListings$number_of_reviews), col="#f01212")

# Or we can easily draw with scatterplot().
scatterplot(sampleListings$number_of_reviews, sampleListings$price)


"#fff"
# One-Way Analysis of Variance (ANOVA)

anova_p_val <- function(p){
  case_when(
    p <= 0.01 ~ "Very Significant Mean Differences between All the Room Types",
    p > 0.01 & p <= 0.05 ~ "Significant Mean Differences between All the Room Types",
    p > 0.05 & p <= 0.1 ~ "Weakly Significant Mean Differences between All the Room Types",
    p > 0.1 ~ "Not Significant Mean Differences between All the Room Types",
  )
}

# Let's check the mean differences of 4 room types (private, entire home, 
# shared, hotel) with 25 elements of each of room type.
reasonableListings <- listings[listings$price <= 2500, ]

private_room <- reasonableListings[reasonableListings$room_type == "Private room", ]
private_room <- na.omit(private_room$price)
private_room_price <- sample(private_room, 16, replace=F)
rm(private_room)
entire_room <- reasonableListings[reasonableListings$room_type == "Entire home/apt", ]
entire_room <- na.omit(entire_room$price)
entire_room_price <- sample(entire_room, 16, replace=F)
rm(entire_room)
shared_room <- reasonableListings[reasonableListings$room_type == "Shared room", ]
shared_room <- na.omit(shared_room$price)
shared_room_price <- sample(shared_room, 16, replace=F)
rm(shared_room)
hotel_room <- reasonableListings[reasonableListings$room_type == "Hotel room", ]
hotel_room <- na.omit(hotel_room$price)
hotel_room_price <- sample(hotel_room, 16, replace=F)
rm(hotel_room)

roomListings <- data.frame("private_room_price" = private_room_price,
                           "entire_home_price" = entire_room_price,
                           "shared_room_price" = shared_room_price,
                           "hotel_room_price" = hotel_room_price)

roomListings <- roomListings %>% pivot_longer(cols = everything(),
                                              names_to = "room_type",
                                              values_to = "prices")

anova_res <- summary(aov(prices ~ room_type, data = roomListings))
anova_p <- anova_res[[1]][["Pr(>F)"]][1]

cat("p-Value:", anova_p, "->", anova_p_val(anova_p))

ggboxplot(roomListings, x="room_type", y="prices", xlab="Rooms", ylab="Prices",
          order=c("private_room_price", "entire_home_price",
                  "shared_room_price", "hotel_room_price")) +
  theme(axis.text.x = element_text(angle=22.5, vjust=0.6, hjust=0.6))


"#fff"
# Kruskal-Wallis Test 

kw_h_val <- function(h){
  case_when(
    h <= 0.01 ~ "Very Significant Median Differences between All the Neighbourhoods",
    h > 0.01 & h <= 0.05 ~ "Significant Median Differences between All the Neighbourhoods",
    h > 0.05 & h <= 0.1 ~ "Weakly Significant Median Differences between All the Neighbourhoods",
    h > 0.1 ~ "Not Significant Median Differences between All the Neighbourhoods",
  )
}

kw_test <- kruskal.test(price ~ neighbourhood, data=reasonableSample)
kw_h <- kw_test$p.value
cat("Kruskal-Wallis p-value:", kw_h, "->", kw_h_val(kw_h))

ggplot(reasonableListings, aes(x=reorder(neighbourhood, price), y=price)) +
  geom_boxplot() +
  theme(axis.text.x=element_text(angle=90, vjust=0.5, hjust=1))










