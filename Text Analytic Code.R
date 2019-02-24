library(textreadr)
library(dplyr)
data <- read_document(file = "/Users/pongtit/Desktop/Text_analytic/data.txt")

a <- 44
b <- 8
my_data <- as.data.frame(matrix(nrow=a, ncol=b))

for(z in 1:b){
  for(i in 1:a){
    my_data[i,z]<- data[i*b+z-b]
  }#closing z loop
}#closing i loop

my_df <- my_data[,-1]
colnames(my_df) <- c("Age", "First", "Favorite", "Reason", "Like_Remakes", "Which_Remake", "Expect")

newdf <- data_frame(text = data)


library(readr)
my_df$Age <- parse_number(my_df$Age)

boxplot(my_df$Age, outline = F)

my_df_no_age <- my_df[,-1]

############################# correlation of first, favorite, remake
#### first movie as a benchmark

my_fav <- data_frame(line=1:a, text=my_df$Favorite)
my_rem <- data_frame(line=1:a, text=my_df$Which_Remake)
my_first <- data_frame(line=1:a, text=my_df$First)

library(tidytext)

tidy_fav <- my_fav %>%
  unnest_tokens(word, text) %>%
  anti_join(stop_words)

tidy_rem <- my_rem %>%
  unnest_tokens(word, text) %>%
  anti_join(stop_words)

tidy_first <- my_first %>%
  unnest_tokens(word, text) %>%
  anti_join(stop_words)

library(tidyr)
library(stringr)
frequency <- bind_rows(mutate(tidy_fav, movie ="favorite"),
                       mutate(tidy_rem, movie = "remake"),
                       mutate(tidy_first, movie ="first")
  )%>%#closing bind_rows
  mutate(word=str_extract(word, "[a-z']+")) %>%
  count(movie, word) %>%
  group_by(movie) %>%
  mutate(proportion = n/sum(n))%>%
  select(-n) %>%
  spread(movie, proportion) %>%
  gather(movie, proportion, `favorite`, `remake`)

cor.test(data=frequency[frequency$movie == "favorite",],
         ~proportion + `first`)

cor.test(data=frequency[frequency$movie == "remake",],
         ~proportion + `first`)
####
frequency2 <- bind_rows(mutate(tidy_fav, movie ="favorite"),
                       mutate(tidy_rem, movie = "remake"),
                       mutate(tidy_first, movie ="first")
)%>%#closing bind_rows
  mutate(word=str_extract(word, "[a-z']+")) %>%
  count(movie, word) %>%
  group_by(movie) %>%
  mutate(proportion = n/sum(n))%>%
  select(-n) %>%
  spread(movie, proportion) %>%
  gather(movie, proportion, `favorite`, `first`)

cor.test(data=frequency2[frequency2$movie == "favorite",],
         ~proportion + `remake`)


frequency_3 <- bind_rows(mutate(tidy_fav, movie ="favorite"),
                       mutate(tidy_rem, movie = "first")
)%>%#closing bind_rows
  mutate(word=str_extract(word, "[a-z']+")) %>%
  count(movie, word) %>%
  group_by(movie) %>%
  mutate(proportion = n/sum(n))%>%
  select(-n) %>%
  spread(movie, proportion) %>%
  gather(movie, proportion, `favorite`)



####
library(ggplot2)
library(scales)
ggplot(frequency, aes(x=proportion, y=`first`, 
                      color = abs(`first`- proportion)))+
  geom_abline(color="blue", lty=2)+
  geom_jitter(alpha=.4, size=2.5, width=0.3, height=0.3)+
  geom_text(aes(label=word), check_overlap = TRUE, vjust=1) +
  scale_x_log10(labels = percent_format())+
  scale_y_log10(labels= percent_format())+
  scale_color_gradientn(colours = topo.colors(10))+
  theme_test() +
  facet_wrap(~movie, ncol=2)+
  theme(legend.position = "none")+
  labs(y= "first", x=NULL)



########################## bi/n grams
my_bigrams <- mydf %>%
  unnest_tokens(bigram, text, token = "ngrams", n=2)

my_bigrams %>%
  count(bigram, sort = TRUE)

#remove stop words
bigrams_separated <- my_bigrams %>%
  separate(bigram, c("word1", "word2"), sep = " ")

bigrams_filtered <- bigrams_separated %>%
  filter(!word1 %in% stop_words$word) %>%
  filter(!word2 %in% stop_words$word) %>%
  count(word1, word2, sort = TRUE)

two_word <- as.data.frame(matrix(nrow = nrow(bigrams_filtered)-1, ncol = 2))
  for (i in 1:nrow(bigrams_filtered)-1) {
    two_word[i,1] <- paste(bigrams_filtered[i+1,1], bigrams_filtered[i+1,2])
    two_word[i,2] <- bigrams_filtered[i+1, 3]
}

library(wordcloud)

two_word %>%
  with(wordcloud(V1, V2))


######################### word cloud and sentiment
#### create dataframe

my_txt_2 <- my_df$Age
mydf_2 <- data_frame(line=1:a, text=my_txt_2)

my_txt_3 <- my_df$First
mydf_3 <- data_frame(line=1:a, text=my_txt_3)

my_txt_4 <- my_df$Favorite
mydf_4 <- data_frame(line=1:a, text=my_txt_4)

my_txt_5 <- my_df$Reason
mydf_5 <- data_frame(line=1:a, text=my_txt_5)

my_txt_6 <- my_df$Like_Remakes
mydf_6 <- data_frame(line=1:a, text=my_txt_6)

my_txt_7 <- my_df$Which_Remake
mydf_7 <- data_frame(line=1:a, text=my_txt_7)

my_txt_8 <- my_df$Expect
mydf_8 <- data_frame(line=1:a, text=my_txt_8)

#### frequency
frequencies_all <- newdf %>%
  unnest_tokens(word, text) %>%
  anti_join(stop_words) %>%
  count(word, sort=TRUE)


frequencies_2 <- mydf_2 %>%
  unnest_tokens(word, text) %>%
  anti_join(stop_words) %>%
  count(word, sort=TRUE)

frequencies_3 <- mydf_3 %>%
  unnest_tokens(word, text) %>%
  anti_join(stop_words) %>%
  count(word, sort=TRUE)

frequencies_4 <- mydf_4 %>%
  unnest_tokens(word, text) %>%
  anti_join(stop_words) %>%
  count(word, sort=TRUE)

frequencies_5 <- mydf_5 %>%
  unnest_tokens(word, text) %>%
  anti_join(stop_words) %>%
  count(word, sort=TRUE)

frequencies_6 <- mydf_6 %>%
  unnest_tokens(word, text) %>%
  anti_join(stop_words) %>%
  count(word, sort=TRUE)

frequencies_7 <- mydf_7 %>%
  unnest_tokens(word, text) %>%
  anti_join(stop_words) %>%
  count(word, sort=TRUE)

frequencies_8 <- mydf_8 %>%
  unnest_tokens(word, text) %>%
  anti_join(stop_words) %>%
  count(word, sort=TRUE)

#### word cloud
library(wordcloud)

pal <- brewer.pal(8, "Dark2")

frequencies_all %>%
  with(wordcloud(word, n, colors = pal))

frequencies_2 %>%
  with(wordcloud(word, n))

frequencies_3 %>%
  with(wordcloud(word, n))

frequencies_4 %>%
  with(wordcloud(word, n))

frequencies_5 %>%
  with(wordcloud(word, n))

frequencies_6 %>%
  with(wordcloud(word, n))

frequencies_7 %>%
  with(wordcloud(word, n))

frequencies_8 %>%
  with(wordcloud(word, n))

#### sentiment
library(reshape2)

frequencies_all %>%
  inner_join(get_sentiments("bing")) %>%
  count(word, sentiment, sort=TRUE) %>%
  acast(word ~sentiment, value.var="nn", fill=0) %>%
  comparison.cloud(colors = c("pink", "lightgreen"),
                   max.words=100)

frequencies_2 %>%
  inner_join(get_sentiments("bing")) %>%
  count(word, sentiment, sort=TRUE) %>%
  acast(word ~sentiment, value.var="nn", fill=0) %>%
  comparison.cloud(colors = c("pink", "lightgreen"),
                   max.words=100)
frequencies_3 %>%
  inner_join(get_sentiments("bing")) %>%
  count(word, sentiment, sort=TRUE) %>%
  acast(word ~sentiment, value.var="nn", fill=0) %>%
  comparison.cloud(colors = c("pink", "lightgreen"),
                   max.words=100)

frequencies_4 %>%
  inner_join(get_sentiments("bing")) %>%
  count(word, sentiment, sort=TRUE) %>%
  acast(word ~sentiment, value.var="nn", fill=0) %>%
  comparison.cloud(colors = c("pink", "lightgreen"),
                   max.words=100)

frequencies_5 %>%
  inner_join(get_sentiments("bing")) %>%
  count(word, sentiment, sort=TRUE) %>%
  acast(word ~sentiment, value.var="nn", fill=0) %>%
  comparison.cloud(colors = c("pink", "lightgreen"),
                   max.words=100)

frequencies_6 %>%
  inner_join(get_sentiments("bing")) %>%
  count(word, sentiment, sort=TRUE) %>%
  acast(word ~sentiment, value.var="nn", fill=0) %>%
  comparison.cloud(colors = c("pink", "lightgreen"),
                   max.words=100)

frequencies_7 %>%
  inner_join(get_sentiments("bing")) %>%
  count(word, sentiment, sort=TRUE) %>%
  acast(word ~sentiment, value.var="nn", fill=0) %>%
  comparison.cloud(colors = c("pink", "lightgreen"),
                   max.words=100)

frequencies_8 %>%
  inner_join(get_sentiments("bing")) %>%
  count(word, sentiment, sort=TRUE) %>%
  acast(word ~sentiment, value.var="nn", fill=0) %>%
  comparison.cloud(colors = c("pink", "lightgreen"),
                   max.words=100)