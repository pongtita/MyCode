####################################################
# Create by Pongtit
# Date: 11/26/2018
# Purpose: Team Assignment
####################################################

library(readxl)
weekly_visit <- read_excel("~/Desktop/Class_R/Team project/Web Analytics Case Student Spreadsheet.xls", 
                           skip = 4, sheet = 2)
financials <- read_excel("~/Desktop/Class_R/Team project/Web Analytics Case Student Spreadsheet.xls", 
                         skip = 4, sheet = 3)
Lbs_sold <- read_excel("~/Desktop/Class_R/Team project/Web Analytics Case Student Spreadsheet.xls", 
                       skip = 4, sheet = 4)
daily_visit <- read_excel("~/Desktop/Class_R/Team project/Web Analytics Case Student Spreadsheet.xls", 
                          skip = 4, sheet = 5)
demographic <- read_excel("~/Desktop/Class_R/Team project/Web Analytics Case Student Spreadsheet.xls", 
                          skip = 5, sheet = 6)

merge1 <- merge(weekly_visit, financials, by = "Week (2008-2009)", sort = F)
merge1$period <- NA
merge1$period[1:14] <- "initial"
merge1$period[15:35] <- "prepromotion"
merge1$period[36:52] <- "promotion"
merge1$period[53:66] <- "postpromotion"

### Question 1
library(ggplot2)
Q_1 <- ggplot(weekly_visit, aes(x = weekly_visit$`Week (2008-2009)`, y = weekly_visit$`Unique Visits`))+ 
              geom_bar(stat = "identity", color = "black", fill = "blue") +
              xlab("Weeks") +
              ylab("No. of unique visit") + 
              ggtitle("Unique visit per week") +
              theme_classic() +
              theme(plot.title = element_text(hjust = 0.5),
                    axis.text.x = element_text(size = 4 ,angle = 90))
print(Q_1)

ggplot(financials, aes(x = Lbs_sold$Week, y = Lbs_sold$`Lbs. Sold`))+ 
  geom_bar(stat = "identity", color = "black", fill = "white") +
  xlab("Weeks") +
  ylab("Sold") + 
  ggtitle("Lbs Sold") +
  theme_classic() +
  theme(plot.title = element_text(hjust = 0.5),
        axis.text.x = element_text(size = 4 ,angle = 90))

### Question 2
Q_2_table <- subset(merge1, select = c(`Week (2008-2009)`, 
                                       Visits, `Unique Visits`,
                                       Revenue, Profit, `Lbs. Sold`))


initial_period <- Q_2_table[1:14,]
summary(initial_period)

pre_promotion <- Q_2_table[15:35,]
summary(pre_promotion)

promotion <- Q_2_table[36:52,]
summary(promotion)

post_promotion <- Q_2_table[53:66,]
summary(post_promotion)

# table 2
my_sum_function <- function(x){
  my_mean <- c()
  my_med <- c()
  my_sd <- c()
  my_min <- c()
  my_max <- c()
  for (i in 1:5) {
    my_mean[i] <- mean(x[,i+1])
    my_med[i] <- mean(x[,i+1])
    my_sd[i] <- sd(x[,i+1])
    my_min[i] <- min(x[,i+1])
    my_max[i] <- max(x[i+1])
  }
  y <- data.frame(my_mean, my_med, my_sd, my_min, my_max, row.names = c("Visits", "Unique Visits", "Revenue", "Profit", "Lbs. Sold"))
  yt <- t(y)
  return(yt)
}

ini_sum <- my_sum_function(initial_period)
pre_sum <- my_sum_function(pre_promotion)
pro_sum <- my_sum_function(promotion)
pos_sum <- my_sum_function(post_promotion)

print(ini_sum)
print(pre_sum)
print(pro_sum)
print(pos_sum)

# table 3
my_average_mat <- matrix(c(ini_sum[1,], pre_sum[1,], pro_sum[1,], pos_sum[1,]), nrow = 4, byrow = T)
my_average <- as.data.frame(my_average_mat, row.names = c("Initial", "Pre-Promo", "Promotion", "Post-Promo"))
colnames(my_average) <- c("Visits", "Unique Visits", "Revenue", "Profit", "Lbs. Sold")
print(my_average)

## Question 5 Revenue VS Lbs. Sold
corre1 <- data.frame(financials$Revenue, financials$`Lbs. Sold`)
plotcorre1 <- ggplot(corre1, aes(x = financials$`Lbs. Sold`, y = financials$Revenue)) + 
                     geom_point(color = "blue") +
                     theme_classic()
plot(plotcorre1)
cor(corre1)

## Question 6 Revenue VS visit
corre2 <- data.frame(financials$Revenue, weekly_visit$Visits)
plotcorre2 <- ggplot(corre1, aes(x = weekly_visit$Visits, y = financials$Revenue)) + 
                     geom_point(color = "blue") +
                     theme_classic()
plot(plotcorre2)
cor(corre2)

## Question 8. a) summary of Lbs. Sold
summary(Lbs_sold)
L <- ggplot(Lbs_sold, aes(x= Lbs_sold$`Lbs. Sold`)) + 
            geom_histogram(aes(y = ..density..),color = "black", fill = "blue") +
            geom_density(alpha = .2, fill = "#FF6666") +
            labs(title = "Pounds of material sold", x = "Pounds Sold", y = "Count")
plot(L)

## Question 8. d) table
Theo_sd1 <- nrow(Lbs_sold) * .68
Theo_sd2 <- nrow(Lbs_sold) * .95
Theo_sd3 <- nrow(Lbs_sold) * .99

Lbs_sold$my_z[i] <- NA
for (i in 1:length(Lbs_sold$`Lbs. Sold`)) {
  Lbs_sold$my_z[i] <- (Lbs_sold$`Lbs. Sold`[i] - mean(Lbs_sold$`Lbs. Sold`))/sd(Lbs_sold$`Lbs. Sold`)
}

Actual_sd1 <- sum(Lbs_sold$my_z >= -1 & Lbs_sold$my_z <= 1)
Actual_sd2 <- sum(Lbs_sold$my_z >= -2 & Lbs_sold$my_z <= 2)
Actual_sd3 <- sum(Lbs_sold$my_z >= -3 & Lbs_sold$my_z <= 3)

Interval = c("mean +-1 std. dev.", "mean +-2 std. dev.", "mean +-3 std. dev.")
Theoretical_Data = c('68%', '95%', '99%')
Theoretical_No_Obs = c(round(Theo_sd1), round(Theo_sd2), round(Theo_sd3))
Actual_no_Obs = c(Actual_sd1, Actual_sd2, Actual_sd3)

my_ta1 <- data.frame(Interval, Theoretical_Data, Theoretical_No_Obs, Actual_no_Obs)

## Question 8. e)
plus_one <- .34
minus_one <- .34
plus_onetwo <- (.95/2) - .34
minus_onetwo <- (.95/2) - .34
plus_twothree <- (.99/2) - (.95/2)
minus_twothree <- (.99/2) - (.95/2)

The1 <- plus_one * nrow(Lbs_sold)
The2 <- minus_one * nrow(Lbs_sold)
The3 <- plus_onetwo * nrow(Lbs_sold)
The4 <- minus_onetwo * nrow(Lbs_sold)
The5 <- plus_twothree * nrow(Lbs_sold)
The6 <- minus_twothree * nrow(Lbs_sold)

Act1 <- sum(Lbs_sold$my_z >= 0 & Lbs_sold$my_z <= 1)
Act2 <- sum(Lbs_sold$my_z >= -1 & Lbs_sold$my_z <= 0)
Act3 <- sum(Lbs_sold$my_z >= 1 & Lbs_sold$my_z <= 2)
Act4 <- sum(Lbs_sold$my_z >= -2 & Lbs_sold$my_z <= -1)
Act5 <- sum(Lbs_sold$my_z >= 2 & Lbs_sold$my_z <= 3)
Act6 <- sum(Lbs_sold$my_z >= -3 & Lbs_sold$my_z <= -2)

Interval_e = c("mean +1 std. dev.", "mean -1 std. dev.", "", "1 std. dev. to 2 std.dev.", "-1 std.dev. to -2 std.dev.", "", "2 std. dev. to 3 std.dev.", "-2 std. dev. to -2 std. dev.")
Theoretical_Data_e = c(plus_one, minus_one, "", plus_onetwo, minus_onetwo, "", plus_twothree, minus_twothree)
Theoretical_No_Obs_e = c(round(The1), round(The2), "", round(The3), round(The4), "", round(The5), round(The6))
Actual_no_Obs_e = c(Act1, Act2,"", Act3, Act4, "", Act5, Act6)

my_ta2 <- data.frame(Interval_e, Theoretical_Data_e, Theoretical_No_Obs_e, Actual_no_Obs_e)

## Question 8. g)
install.packages("timeDate")
library(timeDate)
skewness(Lbs_sold$`Lbs. Sold`) # method = moment, compare to 0 (normal)
kurtosis(Lbs_sold$`Lbs. Sold`) # method = excess, compare to 0 (normal)



# demographic
all_traffic_sources <- demographic[2:5, 2:3]
colnames(all_traffic_sources) <- c("All Traffic Sources", "Visits")

top_ten_referring_sites <- demographic[9:18, 2:3]
colnames(top_ten_referring_sites) <- c("Top ten referring sites", "Visits")

top_ten_search_engine <- demographic[22:31, 2:3]
colnames(top_ten_search_engine) <- c("Top ten search engine", "Visits")


top_ten_geographic_sources <- demographic[35:44, 2:3]
colnames(top_ten_geographic_sources) <- c("Top ten geographic sources", "Visits")

top_ten_browsers_used <- demographic[49:58, 2:3]
colnames(top_ten_browsers_used) <- c("Top ten browsers used", "Visits")

top_ten_operating_systems <- demographic[63:72, 2:3]
colnames(top_ten_operating_systems) <- c("Top ten operating systems", "Visits")

top_ten_browsers_used$Visits <- as.numeric(top_ten_browsers_used$Visits)
top_ten_geographic_sources$Visits <- as.numeric(top_ten_geographic_sources$Visits)
top_ten_operating_systems$Visits <- as.numeric(top_ten_operating_systems$Visits)
top_ten_referring_sites$Visits <- as.numeric(top_ten_referring_sites$Visits)
top_ten_search_engine$Visits <- as.numeric(top_ten_search_engine$Visits)

##### Analysis Part
## Run correlation in total and for each period
cor(merge1[,2:12])
pairs(merge1[,2:12], pch = 19)

initial <- merge1[1:14,]
pre_pro <- merge1[15:35,]
pro <- merge1[36:52,]
pos_pro <- merge1[53:66,]

cor(initial[,2:12])
cor(pre_pro[,2:12])
cor(pro[,2:12])
cor(pos_pro[,2:12])

pageview / revenue
ggplot(merge1, aes(x = merge1$Pageviews, y = merge1$Revenue, color = merge1$period)) +
       geom_point()

install.packages("forcats")
library(forcats)

ggplot(top_ten_browsers_used, aes(x= reorder(top_ten_browsers_used$`Top ten browsers used`, top_ten_browsers_used$Visits), 
                                  y= top_ten_browsers_used$Visits, fill = variable)) + 
  geom_bar(stat = "identity",color = "black", fill = "blue") +
  labs(title = "Browsers Used", x = "Browsers", y = "Visits") + 
  theme_classic() +
  theme(plot.title = element_text(hjust = 0.5),
        axis.text.x = element_text(size = 8)) + coord_flip()

ggplot(top_ten_geographic_sources, aes(x= reorder(top_ten_geographic_sources$`Top ten geographic sources`, top_ten_geographic_sources$Visits), 
                                  y= top_ten_geographic_sources$Visits, fill = variable)) + 
  geom_bar(stat = "identity",color = "black", fill = "blue") +
  labs(title = "Region", x = "Regions", y = "Visits") + 
  theme_classic() +
  theme(plot.title = element_text(hjust = 0.5),
        axis.text.x = element_text(size = 8)) + coord_flip()

ggplot(top_ten_operating_systems, aes(x= reorder(top_ten_operating_systems$`Top ten operating systems`, top_ten_operating_systems$Visits), 
                                  y= top_ten_operating_systems$Visits, fill = variable)) + 
  geom_bar(stat = "identity",color = "black", fill = "blue") +
  labs(title = "Operating System", x = "OS", y = "Visits") + 
  theme_classic() +
  theme(plot.title = element_text(hjust = 0.5),
        axis.text.x = element_text(size = 8)) + coord_flip()

ggplot(top_ten_referring_sites, aes(x= reorder(top_ten_referring_sites$`Top ten referring sites`, top_ten_referring_sites$Visits), 
                                  y= top_ten_referring_sites$Visits, fill = variable)) + 
  geom_bar(stat = "identity",color = "black", fill = "blue") +
  labs(title = "Reffering Sits", x = "Sites", y = "Visits") + 
  theme_classic() +
  theme(plot.title = element_text(hjust = 0.5),
        axis.text.x = element_text(size = 8)) + coord_flip()

ggplot(top_ten_search_engine, aes(x= reorder(top_ten_search_engine$`Top ten search engine`, top_ten_search_engine$Visits), 
                                  y= top_ten_search_engine$Visits, fill = variable)) + 
  geom_bar(stat = "identity",color = "black", fill = "blue") +
  labs(title = "Search Engines", x = "Search Engines", y = "Visits") + 
  theme_classic() +
  theme(plot.title = element_text(hjust = 0.5),
        axis.text.x = element_text(size = 8)) + coord_flip()
