iris <- iris
a <- lm(iris$Sepal.Length~iris$Sepal.Width, data = iris)
b <- lm(iris$Sepal.Length~iris$Petal.Length, data = iris)
c <- lm(iris$Sepal.Length~iris$Petal.Width, data = iris)

plot(x = iris$Sepal.Width, y = iris$Sepal.Length, type = "p")
plot(x = iris$Petal.Length, y = iris$Sepal.Length, type = "p")
plot(x = iris$Petal.Width, y = iris$Sepal.Length, type = "p")


bptest(a) #Homos
bptest(b) #Homos
bptest(c) # alpha <= 0.05 Hetero






## 8.6

install.packages("plotly")
install.packages("magrittr")
library(plotly)
library(magrittr)

p <- plot_ly()
for (i in 1:30){
  p <- add_trace(p, x = 1:100, y = rnorm(100, 2000, 20), type = 'scatter', mode = 'markers+lines')
}

print(p)





## 8.8
horse_colic <- read.table("horse-colic.data", dec = ",")
names(horse_colic) <- c("Surgery?", "Age", "Hospital Number", "Rental temperature", "Pulse",
                        "Respiratory rate", "Temperature of extremities", "Peripheral pulse",
                        "Mucous membranes", "Capillary refill time", "Pain", "Peristalsis",
                        "Abdominal distension", "nasogastric tube", "Nasogastric reflux",
                        "Nasogastric reflux PH", "Rectal examination", "Abdomen", "Packed cell volume",
                        "Total protein", "Abdominocentesis appearance", "Abdomcentesis total protein",
                        "Outcome", "Surgical lesion?", "Type of lesion1", "Type of lesion2", "Type of lesion3",
                        "Cp_data")
horse_colic %>%
  gather() %>% 
  ggplot(aes(value)) +
  facet_wrap(~ key, scales = "free") +
  geom_bar()